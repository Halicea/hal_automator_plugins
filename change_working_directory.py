from hal_configurator.lib.command_base import OperationBase, \
  InvalidCommandArgumentsError, ArgumentDescriptor


class SetWorkingDirectory(OperationBase):
  """Create a condition"""
  code = "set_working_directory"
  name = "Set Working Directory"
  group = "Basic"
  def __init__(self,*args, **kwargs):
    super(Condition, self).__init__(*args, **kwargs)
    self.result = ''

  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("WorkingDirectory", "Working directory", "text", is_optional=False)
           ]
  def set_args(self, WorkingDirectory):
    self.kwargs["WorkingDirectory"]= self.WorkingDirectory = WorkingDirectory

  def run(self):
    is_valid, errors = self.validate_args()
    if not is_valid:
      self.executor.log.write(errors)
      raise Exception(str(errors))
    else:
      self.executor.working_directory = self.WorkingDirectory
      os.chdir(self.WorkingDirectory)
      self.result = self.WorkingDirectory
      
__plugin__ = SetWorkingDirectory