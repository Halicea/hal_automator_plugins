import urllib2
from hal_configurator.lib.command_base import \
  OperationBase, InvalidCommandArgumentsError, ArgumentDescriptor
import os
class ReplaceFromUrl(OperationBase):
  """Replaces File(Destination) from a resource file supplied by URI"""
  code = "replace_from_url"
  def __init__(self,*args, **kwargs):
    super(ReplaceFromUrl, self).__init__(*args, **kwargs)
    self.result = ''

  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Resource", "The Resource to use", "text"),
            ArgumentDescriptor("Destination", "Where to put the file(relative to the working dir or absolute)", "text")
            ]
  def set_args(self, Resource, Destination):
    self.kwargs["Resource"]= self.resource = Resource
    self.kwargs["Destination"]= self.destination = Destination

  def run(self):
    is_valid, errors = self.validate_args()
    if is_valid:
      res = self.resource.replace('\\', '/')
      print res
      if res.startswith('file://'):
        temp_path = res[len("file://"):]
        normalized_temp_path = os.path.normpath(temp_path)
        res = "file://"+normalized_temp_path
        print "new res:", res
      if not ("://" in res):
        res = self.executor.resources_root+"/"+res

      f = urllib2.urlopen(res)
      dest = self.destination
      if not dest.startswith('/'):
        if not dest.startswith('./'):
          dest = './'+dest
      dest = os.path.abspath(dest)
      fh = None
      ex_raised = None
      try:
        if not os.path.exists(dest):
          open(dest, 'a').close()
        fh = open(dest, 'wb')
        fh.write(f.read())
      except Exception, ex:
        ex_raised = ex
      finally:
        if fh:
          fh.close()
        if ex_raised:
          raise ex_raised
      print 'Downloaded the file to ', self.destination
    else:
      raise InvalidCommandArgumentsError(str(errors))


__plugin__ = ReplaceFromUrl

def test_replace_from_url():
  rfu = ReplaceFromUrl(verbose=True)
  rfu.set_args()
