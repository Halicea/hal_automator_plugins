from os.path import expanduser
import re
import datetime
import os
import shutil
import subprocess
import tempfile
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
    key = '<key>application-identifier</key>\n'
    ind = prof_str.index(key)+len(key)
    l = prof_str.index('<string>', ind)+len('<string>')
    r = prof_str.index('</string>', ind)
    return prof_str[l:r]

  def parse_type(prof_str):
    key = '<key>aps-environment</key>\n'
    try:
        ind = prof_str.index(key)+len(key)
        l = prof_str.index('<string>', ind)+len('<string>')
        r = prof_str.index('</string>', ind)
        return prof_str[l:r]
    except:
      if '<key>DeveloperCertificates</key>' in prof_str:
        return 'development'
      else:
        raise

  def parse_profile_name(prof_str):
    key = '<key>Name</key>'
    ind = prof_str.index(key)+len(key)
    l = prof_str.index('<string>', ind)+len('<string>')
    r = prof_str.index('</string>', ind)
    return prof_str[l:r]

  def parse_exp_date(prof_str):
    key = '<key>ExpirationDate</key>'
    ind = prof_str.index(key)+len(key)
    l = prof_str.index('<date>', ind)+len('<date>')
    r = prof_str.index('</date>', ind)
    s = prof_str[l:r]
    d = datetime.datetime(*map(int, re.split('[^\d]', s)[:-1]))
    return d

  with open(path, 'r') as f:
    t = f.read()
    res = {}
    res['path'] = os.path.abspath(path)
    res['uuid'] = parse_uuid(t)
    res['name'] = parse_name(t)
    res['profile_name'] = parse_profile_name(t)
    res['expiration_date'] = parse_exp_date(t)
    res['target'] = parse_target(t)
    res['type'] = parse_type(t)
    return res


def add_profile(path, args=None):
  info = get_info(path)
  j = os.path.join
  shutil.copy(path, j(profiles_dir, '%s.mobileprovision' % info['uuid']))


def rm_profile_by_app_id(target=None, profile_type=None):
  infos = ls_profiles(profiles_dir, target, profile_type)
  for info in infos:
    os.remove(info['path'])
  return infos

def rm_profile_like_on_path(path=None, args=None):
  info = get_info(path)
  profile_path = os.path.join(profiles_dir, '%s.mobileprovision' % info['uuid'])
  os.remove(profile_path)
  return profile_path

def ls_profiles(path=None, target=None, profile_type='production'):
  infos = []
  _pdir = path
  if path is None:
    _pdir = profiles_dir
  for root, dirs, files in os.walk(_pdir):
    for f in files:
      if f.endswith('.mobileprovision'):
        pfile = os.path.join(root, f)
        info = get_info(pfile)
        if target:
          if target in info['target']:
            if profile_type:
              if 'type' in info and info['type'] == profile_type:
                infos.append(info)
            else:
              infos.append(info)
        else:
          infos.append(info)
  counter = 1
  infos = sorted(infos, key=lambda x: x['expiration_date'], reverse=False)
  for info in infos:
    print '*'*20
    print str(counter)+".", info['name'], info['target'], info['uuid'], info["type"]
    print '*'*20
    counter += 1
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
  if code > 0:
    raise Exception('\n'.join(output)+'\n'.join(error) +
                    '\nShell process exited with error code %s' % code +
                    '\n cmd: %s' % cmd)
  return '\n'.join(output)

def add_cert(path, args=None):
  cmd = '/usr/bin/security import %s -k %s -P %s -T  -A /usr/bin/codesign'
  cmd = cmd % (path, args.keychain, args.passwd)
  print cmd
  call(cmd.split(' '))

def ls_certs(args):
  command = "/usr/bin/security dump-keychain {} |grep \"labl\""
  command = command.format(args.keychain)
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
  cmd = ['/usr/bin/security', 'find-certificate', '-a', '-Z', '-c',
         common_name, args.keychain]
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
    cmd = ['/usr/bin/security', 'delete-certificate', '-c', cert_name, args.keychain]
  if sha1:
    cmd = ['/usr/bin/security', 'delete-certificate', '-Z', sha1, args.keychain]
  if cmd:
    print cmd
    call(cmd)

command_dict = {
    'cert': {
        'add': add_cert,
        'rm': rm_cert,
        'list': ls_certs
    },
    'profile': {
        'add': add_profile,
        'rm': rm_profile,
        'list': ls_profiles
    }
}
