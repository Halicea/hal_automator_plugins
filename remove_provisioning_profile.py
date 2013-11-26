from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
from urllib2 import Request, urlopen
from ios_deployment_utils import rm_profile, add_profile
import os

__author__ = 'Costa Halicea'

class RemoveIOSProvisioningProfile(OperationBase):
  def __init__(self,*args, **kwargs):
    super(RemoveIOSProvisioningProfile, self).__init__(*args, **kwargs)
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Resource", "The provistioning profile resource", "text")
           ]
  def set_args(self, Resource):
    self.kwargs["Resource"]=self.provistioning_profile = Resource
  
  def run(self):
    rm_profile(self.provistioning_profile)
    self.result =  True


__plugin__ = RemoveIOSProvisioningProfile

