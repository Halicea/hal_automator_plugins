import os
import plistlib
def parseProfile(p):
  f = isinstance(p, str) and open(p, 'r') or p
  k = f.read()
  f.close()
  pli = k[k.find('<?xml'):k.find('</plist>')+9]
  newf = open('tmp.plist','w')
  newf.write(pli)
  newf.close()
  v = plistlib.readPlist('tmp.plist')
  return (v['AppIDName'], v['Entitlements']['application-identifier'], v['UUID'])

def list_profiles_in_dir(d):
  for root, dirs, files in os.walk(d):
    for p in files:
      if p.endswith('mobileprovision'):
        yield os.path.join(root, p)

def main():
  f = open('./profiles.csv', 'w')
  for k in list_profiles_in_dir('/Users/kostamihajlov/Downloads'):
    f.write(', '.join(parseProfile(k)))
    f.write('\n')
  f.close()

if __name__=='__main__':
  main()