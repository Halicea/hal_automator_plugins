if __name__ =='__main__':
  import sys
  sys.path.append('../src/')

from jenkinsapi.jenkins import Jenkins
from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
import json
import requests
__author__ = 'Costa Halicea'

class JenkinsBuild(OperationBase):
  def __init__(self,*args, **kwargs):
    super(JenkinsBuild, self).__init__(*args, **kwargs)
    self.result = ''
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("JobName", "jenkins job name", "text"),
            ArgumentDescriptor("Parameters", "JSON Parameters for the job", "text"),
            ArgumentDescriptor("JenkinsUrl", "the jenkins server url", "url"),
            ArgumentDescriptor("Username", "Jenkins Username", "text"),
            ArgumentDescriptor("Password", "Jenkins Password", "text")
           ]
  def set_args(self, JobName, JenkinsUrl, Username, Password, Parameters):
    self.kwargs["JobName"] = JobName
    self.kwargs["JenkinsUrl"] = JenkinsUrl
    self.kwargs["Username"] = Username
    self.kwargs["Password"] = Password
    self.kwargs["Parameters"] = json.loads(Parameters)
  def run(self):
    j = Jenkins(self.kwargs["JenkinsUrl"], self.kwargs["Username"], self.kwargs["Password"])
    j.build_job(self.kwargs["JobName"], params = self.kwargs["Parameters"])

class RegisterCertificate(OperationBase):

  def __init__(self,*args, **kwargs):
    super(RegisterCertificate, self).__init__(*args, **kwargs)
    self.result = ''

  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("ServerUrl", "Server Url", "url"),
            ArgumentDescriptor("PostUrl", "PostResource", "url"),
            ArgumentDescriptor("AuthUsername", "Authentication Username", "text"),
            ArgumentDescriptor("AuthPassword", "Authentication Password", "password"),
            ArgumentDescriptor("Target", "Target", "text"),
            ArgumentDescriptor("P12Resource", "The Certificate File", "text"),
            ArgumentDescriptor("Password", "Certificate Password", "password")
           ]
  def set_args(self, **kwargs):
    self.kwargs = kwargs
  def login(self):
    u = self.kwargs['AuthUsername']
    p = self.kwargs['AuthPassword']
    url = self.kwargs['ServerUrl']
    res = requests.post(url = url+'/svc/login/mediawire', data = json.dumps({
      'Email':u,
      'Password':p
      }), headers ={'ClientVersion':'30.00.00', 'Content-Type':'application/json'})
    if res.status_code!=200:
      self.log.write('Invalid Status Code returned #'+str(res.status_code))
      raise Exception('Invalid Status Code returned #'+str(res.status_code))
    self.log.write(str(res.json()))
    if 'data' in res.json():
      self.token = res.json()['data']
    else:
      self.token = None

  def run(self):
    self.login()
    if self.token:
      fpath = self.kwargs['P12Resource']
      if fpath.startswith('file://'):
        fpath = fpath[7:]
      f = open(fpath, 'rb')
      files = {'CertFile':f}
      headers = {'ClientVersion':'27.00.00'}
      headers['Cookie'] = 'mwr.sid='+self.token
      data = {
        'Target':self.kwargs['Target'],
        'Password':self.kwargs['Password']
      }
      res = requests.post(self.kwargs["PostUrl"], files=files, headers=headers, data = data)
      if res.status_code != 200:
        self.log.write('Invalid Status Code returned #'+str(res.status_code))
        raise Exception('Invalid Status Code returned #'+str(res.status_code))
      self.log.write(res.text)
    else:
      raise Exception('Not Loged in to save the certificate')

__plugins__ = [JenkinsBuild, RegisterCertificate]

def test_RegisterCertificate():
  class RegisterCertificateTest(RegisterCertificate):
    def __init__(self):
      self.log = sys.stdout
      pass
  #def __init__(self, executor, resources, variables, log=sys.stdout, verbose= False, *args, **kwargs):
  a = RegisterCertificateTest()
  a.set_args(**{'ServerUrl':'http://svc.mediawiremobile.com',
    'PostUrl':'http://mediawiremobile.com/branded_apps/52f91f409a6470754a00284f/certificates/save',
    'AuthUsername':'costa@halicea.com',
    'AuthPassword':'demo12345',
    'Target':'Development',
    'Password':'Mwr12345',
    'P12Resource':'/Users/kostamihajlov/Desktop/CWTPushCertificateDevelopment.p12'
  })
  a.run()

if __name__ == '__main__':
  test_RegisterCertificate()
