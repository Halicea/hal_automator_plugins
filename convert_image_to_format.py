import urllib2
from PIL import Image
from hal_configurator.lib.command_base import \
  OperationBase, InvalidCommandArgumentsError, ArgumentDescriptor
class ConvertImageToFormat(OperationBase):
  """Replaces File(Destination) from a resource file supplied by URI"""
  code = "convert_image_to_format"
  def __init__(self,*args, **kwargs):
    super(ConvertImageToFormat, self).__init__(*args, **kwargs)
    self.result = ''
  
  @classmethod  
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("ImageResource", "The Resource to use", "text"),
            ArgumentDescriptor("Destination", "Where to put the file(relative to the working dir or absolute)", "text")
            ArgumentDescriptor("Format", "Where to put the file(relative to the working dir or absolute)", "text")
          ]
  
  def set_args(self, ImageResource, Destination, Format):
    self.kwargs["ImageResource"]= self.resource = ImageResource
    self.kwargs["Destination"]= self.destination = Destination
    self.kwargs["Format"]= self.format = Format
  
  def run(self):
    is_valid, errors = self.validate_args()
    if is_valid:
      img = Image(self.resource)
      img.save(self.destination, self.format)
    else:
      raise InvalidCommandArgumentsError(str(errors))

__plugin__ = ConvertImageToFormat

def test_replace_from_url():
  rfu = ConvertImageToFormat(verbose=True)
  rfu.set_args()
