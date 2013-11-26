from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
from ios_deployment_utils import add_profile, rm_profile

class AddIOSProvisioningProfile(OperationBase):
  def __init__(self,*args, **kwargs):
    super(AddIOSProvisioningProfile, self).__init__(*args, **kwargs)
    self.provistioning_profile = None
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Resource", "The provisioning profile resource", "text")
           ]
  def set_args(self, Resource):
    self.kwargs["Resource"]=self.provistioning_profile = Resource
  
  def run(self):
    add_profile(self.provistioning_profile)
    self.result =  True

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


__plugins__ = [AddIOSProvisioningProfile, RemoveIOSProvisioningProfile]

