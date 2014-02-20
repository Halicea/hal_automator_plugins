from PIL import Image #@UnresolvedImport


__author__ = 'Costa Halicea'

from hal_configurator.lib.command_base import \
  OperationBase, InvalidCommandArgumentsError, ArgumentDescriptor

class ConvertImageToFormat(OperationBase):
  """Replaces File(Destination) from a resource file supplied by URI"""

  def __init__(self,*args, **kwargs):
    super(ConvertImageToFormat, self).__init__(*args, **kwargs)
    self.result = ''

  def set_args(self, ImageResource, Destination, Format, Resolution=None):
    """
    :param ConfigPath:
    :type ConfigPath: str
    """
    self.kwargs["ImageResource"] = self.img_res = ImageResource
    self.kwargs["Destination"] = self.dest = Destination
    self.kwargs["Format"] = self.format = Format
    self.kwargs["Resolution"] = self.resolution = Resolution

  def get_resolution_set(self):
    print "Resolution:",self.resolution

    if 'x' in self.resolution:
      return tuple([int(x) for x in self.resolution.split('x')])
    elif 'X' in self.resolution:
      return tuple([int(x.strip()) for x in self.resolution.split('X')])
    elif ',' in self.resolution:
      return tuple([int(x.strip()) for x in self.resolution.split(',')])
    else:
      raise Exception('Invalid resolution: %s'%self.resolution)

  def run(self):
    is_valid, errors = self.validate_args()
    if is_valid:
      self.img_res = self.value_substitutor.substitute(self.img_res)
      if self.img_res.startswith('file://'):
        self.img_res = self.img_res[7:]

      self.dest = self.value_substitutor.substitute(self.dest)

      self.img_res = self.img_res.replace('./', '')
      self.format = self.value_substitutor.substitute(self.format)

      if self.resolution:
        self.resolution = self.value_substitutor.substitute(self.resolution)
      self.log.write('\n'.join([self.img_res, self.dest, self.format, self.resolution or '?X?']))
      img = Image.open(self.img_res);
      if self.resolution:
        print self.get_resolution_set()
        img = img.resize(self.get_resolution_set(), Image.ANTIALIAS)
      img.save(self.dest, self.format)
    else:
      raise InvalidCommandArgumentsError(str(errors))
      #

  @classmethod
  def get_arg_descriptors(cls):
    return [
      ArgumentDescriptor("ImageResource", "External Configuration Directory", "text"),
      ArgumentDescriptor("Destination", "External Configuration Directory", "text"),
      ArgumentDescriptor("Format", "External Configuration Directory", "text"),
      ArgumentDescriptor("Resolution", "The required resolution", "text", default_value_lambda=lambda x:None)
    ]
  @classmethod
  def get_name(cls):
    return "Convert Image to Format"

__plugin__ = ConvertImageToFormat