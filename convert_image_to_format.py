from PIL import Image
import os

__author__ = 'Costa Halicea'

from hal_configurator.lib.command_base import \
  OperationBase, InvalidCommandArgumentsError, ArgumentDescriptor

class ConvertImageToFormat(OperationBase):
  """Replaces File(Destination) from a resource file supplied by URI"""

  def __init__(self,*args, **kwargs):
    super(ConvertImageToFormat, self).__init__(*args, **kwargs)
    self.result = ''

  def set_args(self, ImageResource, Destination, Format):
    """
    :param ConfigPath:
    :type ConfigPath: str
    """
    self.kwargs["ImageResource"] = self.img_res = ImageResource
    self.kwargs["Destination"] = self.dest = Destination
    self.kwargs["Format"] = self.format = Format

  def run(self):
    is_valid, errors = self.validate_args()
    if is_valid:
      self.img_res = self.value_substitutor.substitute(self.img_res)
      self.dest = self.value_substitutor.substitute(self.dest)
      self.format = self.value_substitutor.substitute(self.format)
      img = Image.open(self.img_res);
      img.save(self.dest, self.format);
    else:
      raise InvalidCommandArgumentsError(str(errors))

  @classmethod
  def get_arg_descriptors(cls):
    return [
      ArgumentDescriptor("ImageResource", "External Configuration Directory", "text"),
      ArgumentDescriptor("Destination", "External Configuration Directory", "text"),
      ArgumentDescriptor("Format", "External Configuration Directory", "text")
    ]
  @classmethod
  def get_name(cls):
    return "Convert Image to Format"

__plugin__ = ConvertImageToFormat