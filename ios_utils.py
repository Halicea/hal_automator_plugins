from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
from ios_deployment_utils import add_cert, rm_cert
from ios_deployment_utils import add_profile, rm_profile, CommandArgsProxy
from replace_from_url import ReplaceFromUrl
from replace_text import ReplaceText
import os

__author__ = 'Costa Halicea'

class InstallIOSCertificate(OperationBase):
  def __init__(self,*args, **kwargs):
    super(InstallIOSCertificate, self).__init__(*args, **kwargs)
    self.result = ''
    self.downloader = ReplaceFromUrl(*args, **kwargs)
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
    self.downloader.set_args(self.cert, '/tmp/temp.p12')
    self.downloader.run()
    add_cert('/tmp/temp.p12', CommandArgsProxy(passwd=self.password))
    os.unlink('/tmp/temp.p12')

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
    rm_cert(self.search_string, CommandArgsProxy())

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
    rm_cert(self.search_string, CommandArgsProxy())


class AddIOSProvisioningProfile(OperationBase):
  def __init__(self,*args, **kwargs):
    super(AddIOSProvisioningProfile, self).__init__(*args, **kwargs)
    self.provistioning_profile = None
    self.downloader = ReplaceFromUrl(*args, **kwargs)
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Resource", "The provisioning profile resource", "text")
           ]
  def set_args(self, Resource):
    self.kwargs["Resource"]=self.provistioning_profile = Resource

  def run(self):
    self.downloader.set_args(self.provistioning_profile, '/tmp/temp.mobileprovision')
    self.downloader.run()
    add_profile('/tmp/temp.mobileprovision', CommandArgsProxy())
    os.unlink('/tmp/temp.mobileprovision')
    self.result =  True

class RemoveIOSProvisioningProfile(OperationBase):
  def __init__(self,*args, **kwargs):
    super(RemoveIOSProvisioningProfile, self).__init__(*args, **kwargs)
    self.downloader = ReplaceFromUrl(*args, **kwargs)
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Resource", "The provistioning profile resource", "text")
           ]
  def set_args(self, Resource):

    self.kwargs["Resource"]=self.provistioning_profile = Resource

  def run(self):
    self.downloader.set_args(self.provistioning_profile, '/tmp/temp.mobileprovision')
    self.downloader.run()
    rm_profile('/tmp/temp.mobileprovision', CommandArgsProxy())
    os.unlink('/tmp/temp.mobileprovision')
    self.result =  True
# class IncreaseBundleVersion(OperationBase):
#   def __init__(self, *args, **kwargs):
#     super(IncreaseBundleVersion, self).__init__(*args, **kwargs)
#     self.replace_text = ReplaceText(*args, **kwargs)
#
#   @classmethod
#   def get_arg_descriptors(cls):
#     return [
#             ArgumentDescriptor("Info.plist", "the path of the info.plist file", "text")
#            ]
#   def set_args(self, InfoPlist):
#     self.kwargs["Info.plist"]=self.infoplist = InfoPlist
#
#   def run(self):
#     vc = "\\<CodesignKey\\>.*\\</CodesignKey\\>"
#     vc2 = "\\<CodesignKey\\>.*\\</CodesignKey\\>"
#     self.replace_text.run()


__plugins__ = [InstallIOSCertificate, RemoveIOSCertificates, ListIOSCertificates, AddIOSProvisioningProfile, RemoveIOSProvisioningProfile]
