from hal_configurator.lib.command_base import OperationBase, \
  InvalidCommandArgumentsError, ArgumentDescriptor

class Print(OperationBase):
  code = "print_to_console"
  def __init__(self,*args, **kwargs):
    super(Print, self).__init__(*args, **kwargs)
    self.result = ''

  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("TextToPrint", "The text to be printed in the console", "text"),
            ]
  def set_args(self, TextToPrint):
    self.kwargs["TextToPrint"]= self.texttoprint = TextToPrint

  def run(self):
    is_valid, errors = self.validate_args()
    if is_valid:
      self.log.write(self.value_substitutor.substitute(self.texttoprint))
    else:
      raise InvalidCommandArgumentsError(str(errors))
__plugin__ = Print