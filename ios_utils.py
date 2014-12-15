from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
from ios_deployment_utils import add_cert, rm_cert, ls_certs, get_cert_sha1
from ios_deployment_utils import add_profile, rm_profile, CommandArgsProxy
from replace_from_url import ReplaceFromUrl
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
    self.kwargs["SearchString"]=self.search_string = self.value_substitutor.substitute(self.search_string)
    items = ls_certs(CommandArgsProxy())
    certs_to_delete = []
    for cert_name in items:
      print "Found Cert:{} matching with:{}".format(cert_name, self.search_string)
      if self.search_string in cert_name:
        certs_to_delete.append(cert_name)
    args = CommandArgsProxy()
    for cert_name in certs_to_delete:
      print 'Deleting: {}'.format(cert_name)
      sha1s = get_cert_sha1(cert_name, args=args)
      for sha in sha1s:
          rm_cert(sha1=sha, args=args)

class ListIOSCertificates(OperationBase):
  '''
  Lists all the certificates it can match
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
    self.search_string = self.value_substitutor.substitute(self.search_string)
    results = ls_certs(CommandArgsProxy())
    filtered = [x for x in results if self.search_string in results]
    self.log.write('\n'.join(filtered))
    return results


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
    self.result = True

__plugins__ = [InstallIOSCertificate, RemoveIOSCertificates, ListIOSCertificates, AddIOSProvisioningProfile, RemoveIOSProvisioningProfile]
