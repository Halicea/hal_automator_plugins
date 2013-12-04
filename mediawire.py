
from jenkinsapi.jenkins import Jenkins
from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
import json

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

__plugins__ = [JenkinsBuild]