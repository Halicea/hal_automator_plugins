from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor, InvalidCommandArgumentsError
from replace_from_url import ReplaceFromUrl as replace_from_url
from replace_text import ReplaceText as replace_text
from urllib2 import Request, urlopen, URLError, HTTPError
import os

__author__ = 'Costa Halicea'

class AddDeveloperCertificate(OperationBase):
  def __init__(self,*args, **kwargs):
    super(AddProvisioningProfile, self).__init__(*args, **kwargs)
    self.result = ''
    home = os.path.expanduser("~")
    self.profiles_dir = os.path.join(home, 'Library/MobileDevice/Provisioning Profiles/')
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Resource", "The Developer Certificate resource", "text"),
            ArgumentDescriptor("Password", "Password to unlock the certificate", "text")
           ]
  def set_args(self, Resource):
    self.kwargs["Resource"]=self.provistioning_profile = Resource
  
  def run(self):
    rurl = replace_from_url(\
      executor = self.executor,
      resources = self.resources,
      variables = self.variables,
      verbose=self.verbose)
    app_name, entitlements, appid, uuid = self.get_profile_data()
    dest = os.path.join(self.profiles_dir, uuid+'.mobileprovision')
    rurl.set_args(self.Resource, dest)
    
  def get_profile_data(url):
    import read_profiles
    req = Request(url)
    f = urlopen(req)
    return read_profiles.parseProfile(f)


__plugin__ = AddDeveloperCertificate