from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
from ios_deployment_utils import add_cert, rm_cert
import os

__author__ = 'Costa Halicea'

class InstallIOSCertificate(OperationBase):
  def __init__(self,*args, **kwargs):
    super(InstallIOSCertificate, self).__init__(*args, **kwargs)
    self.result = ''
    home = os.path.expanduser("~")
    self.profiles_dir = os.path.join(home, 'Library/MobileDevice/Provisioning Profiles/')
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Resource", "The Developer Certificate resource", "text"),
            ArgumentDescriptor("Password", "Password to unlock the certificate", "text")
           ]
  def set_args(self, Resource, Password):
    self.kwargs["Resource"]=self.cert = Resource
    self.kwargs["Password"]=self.password = Password
  
  def run(self):
    add_cert(self.cert, self.password)

  
class RemoveIOSCertificates(OperationBase):
  '''
  Removes a certificate from the current system based on the match string providede
  '''
  def __init__(self,*args, **kwargs):
    super(RemoveIOSCertificates, self).__init__(*args, **kwargs)
    self.result = ''
    home = os.path.expanduser("~")
    self.profiles_dir = os.path.join(home, 'Library/MobileDevice/Provisioning Profiles/')
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("SearchString", "The Certificates match pattern", "text"),
           ]
  def set_args(self, SearchString):
    self.kwargs["SearchString"]=self.search_string = SearchString
  
  def run(self):
    rm_cert(self.search_string)

class ListIOSCertificates(OperationBase):
  '''
  Removes a certificate from the current system based on the match string providede
  '''
  def __init__(self,*args, **kwargs):
    super(ListIOSCertificates, self).__init__(*args, **kwargs)
    self.result = ''
    home = os.path.expanduser("~")
    self.profiles_dir = os.path.join(home, 'Library/MobileDevice/Provisioning Profiles/')
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("SearchString", "The Certificates match pattern", "text"),
           ]
  def set_args(self, SearchString):
    self.kwargs["SearchString"]=self.search_string = SearchString
  
  def run(self):
    rm_cert(self.search_string)
    
__plugins__ = [InstallIOSCertificate, RemoveIOSCertificates, ListIOSCertificates]
