from os.path import expanduser
import argparse
import os
import shutil
import subprocess
import tempfile
import sys
profiles_dir = expanduser("~/Library/MobileDevice/Provisioning Profiles")
default_keychain = expanduser('~/Library/Keychains/login.keychain')
class CommandArgsProxy(object):
  def __init__(self, **kwargs):
    self.command = kwargs.has_key('command') and kwargs['command'] or None
    self.command_type = kwargs.has_key('command_type') and kwargs['command_type'] or None
    self.passwd = kwargs.has_key('passwd') and kwargs['passwd'] or None
    self.match = kwargs.has_key('match') and kwargs['match'] or ''
    self.keychain = kwargs.has_key('keychain') and kwargs['keychain'] or default_keychain

def get_info(path, args=None):
  def parse_uuid(prof_str):
    ind = prof_str.index('<key>UUID</key>\n')+len('<key>UUID</key>\n')
    l = prof_str.index('<string>', ind)+len('<string>')
    r = prof_str.index('</string>', ind)
    return prof_str[l:r]
  def parse_name(prof_str):
    try:
      ind = prof_str.index('<key>AppIDName</key>\n')+len('<key>AppIDName</key>\n')
      l = prof_str.index('<string>', ind)+len('<string>')
      r = prof_str.index('</string>', ind)
      return prof_str[l:r]
    except:

      ind = prof_str.index('<key>Name</key>\n')+len('<key>Name</key>\n')
      l = prof_str.index('<string>', ind)+len('<string>')
      r = prof_str.index('</string>', ind)
      return prof_str[l:r]
  def parse_target(prof_str):
    ind = prof_str.index('<key>application-identifier</key>\n')+len('<key>application-identifier</key>\n')
    l = prof_str.index('<string>', ind)+len('<string>')
    r = prof_str.index('</string>', ind)
    return prof_str[l:r]
  with open(path, 'r') as f:
    t = f.read()
    res = {}
    res['uuid']=parse_uuid(t)
    res['name']=parse_name(t)
    res['target']=parse_target(t)
    return res

def add_profile(path, args=None):
  info = get_info(path)
  shutil.copy(path, os.path.join(profiles_dir, '%s.mobileprovision'%info['uuid']))

def rm_profile(path, args=None):
  info = get_info(path)
  os.remove(os.path.join(profiles_dir, '%s.mobileprovision'%info['uuid']))

def ls_profiles(path=None, args=None):
  infos = []
  for p in os.listdir(profiles_dir):
    if p.endswith('.mobileprovision'):
      pfile = os.path.join(profiles_dir, p)
      info = get_info(pfile)
      infos.append(info)
  counter=1
  infos = sorted(infos, key=lambda x: x['name'], reverse=False)
  for info in infos:
    print '*'*20
    print str(counter)+".", info['name'], info['target'], info['uuid']
    print '*'*20
    counter+=1
  return infos

def call(cmd):
  output = []
  error = []
  code = 1
  with tempfile.TemporaryFile() as output_f:
    with tempfile.TemporaryFile() as error_f:
      p = subprocess.Popen(cmd, stderr=error_f, stdout=output_f,
                         close_fds=True, env=os.environ)
      code = p.wait()
      output_f.seek(0)
      error_f.seek(0)
      error = error_f.read().split('\n')
      output = output_f.read().split('\n')
  if code>0:
    raise Exception('\n'.join(output)+'\n'.join(error)+'\nShell process exited with error code %s\n cmd: %s'%(code, cmd))
  return '\n'.join(output)

def add_cert(path, args=None):
  cmd='/usr/bin/security import %s -k %s -P %s -T  -A /usr/bin/codesign'%(path, args.keychain, args.passwd)
  print cmd
  call(cmd.split(' '))

def ls_certs(args):
  command = "/usr/bin/security dump-keychain {} |grep \"labl\"".format(args.keychain)
  cmd = [x for x in command.split(' ') if x]
  output = call(cmd).split('\n')
  prefix = "\"labl\"<blob>=\""
  result = []
  for line in output:
      if prefix in line:
          prefix_end = line.index(prefix)+len(prefix)
          result.append(line[prefix_end:-1])
  return result

def get_cert_sha1(common_name, args):
  #call(["/usr/bin/security", "find-certificate", "-a", "-Z", "-c", "\"iPhone Distribution: Entreprises Kastoff Inc.\"", "/Users/halicea/Library/Keychains/login.keychain"])
    #/usr/bin/security find-certificate -a -Z -c "iPhone Distribution: Entreprises Kastoff Inc." /Users/halicea/Library/Keychains/login.keychain
  cmd = ['/usr/bin/security','find-certificate','-a','-Z','-c',common_name, args.keychain]
  output = call(cmd).split('\n')
  prefix = "SHA-1 hash:"
  result = []
  for line in output:
    if prefix in line:
      result.append(line.strip()[len(prefix):].strip())
  return result

def rm_cert(cert_name=None, sha1=None, args=None):
  cmd = None
  if cert_name:
    cmd = ['/usr/bin/security', 'delete-certificate', '-c', '%s'%cert_name, args.keychain]
  if sha1:
    cmd = ['/usr/bin/security', 'delete-certificate', '-Z', sha1, args.keychain]
  if cmd:
    print cmd
    call(cmd)

command_dict={
  "cert":{
    "add":add_cert,
    "rm":rm_cert,
    "list":ls_certs
  },
  "profile":{
    "add":add_profile,
    "rm":rm_profile,
    "list": ls_profiles
  }
}

if __name__=='__main__':
  #"Apple Production IOS Push Services:"
  #"Apple Developer IOS Push Services:"
  parser = argparse.ArgumentParser(prog="iOS Provisioning Profiles and Keychain Utility")
  parser.add_argument('command', choices=['add', 'rm', 'list'])
  parser.add_argument('command_type', choices=['cert', 'profile', 'list'])
  parser.add_argument('--passwd', '-p', help='Password of the Certificate file')
  parser.add_argument('--match', '-m', help='Match for certificate', default='')
  parser.add_argument('--keychain', '-k', help='Keychain', default=default_keychain)
  parser.add_argument('--file')
  args = parser.parse_args(sys.argv[1:])

  command_dict[args.command_type][args.command](args.file, args)
#security find-certificate -a -p -c "com.turn-page.CampCalifornia" /Users/kostamihajlov/Library/Keychains/login.keychain"
#security find-certificate -a -p -Z -c "com.turn-page.CampCalifornia" /Users/kostamihajlov/Library/Keychains/login.keychain"
#"security delete-certificate -a -c "Apple Development IOS Push Services: com.turn-page.CampCalifornia" /Users/kostamihajlov/Library/Keychains/login.keychain"
#security delete-certificate -Z E6A44C7CEF6ED79709107C5EF9AE88986F01AFC8 /Users/kostamihajlov/Library/Keychains/login.keychain
  #install_profile(sys.argv[1])
