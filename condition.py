import urllib2
from PIL import Image
from hal_configurator.lib.command_base import \
  OperationBase, InvalidCommandArgumentsError, ArgumentDescriptor

class Condition(OperationBase):
  """Convert an Image to a different format"""
  code = "condition"
  def __init__(self,*args, **kwargs):
    super(Condition, self).__init__(*args, **kwargs)
    self.result = ''
  
  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Expression", "Python Expression", "text"),
            ArgumentDescriptor("Bundle", "Operations Bundle", "OperationsBundle"),
           ]
  
  def set_args(self, Expression, Bundle):
    self.kwargs["Expression"]= self.expression = Expression
    self.kwargs["Bundle"]=self.bundle = Bundle
    
  def run(self):  
    is_valid, errors = self.validate_args()
    if is_valid:
      result = eval(self.expression)
      if result:
        self.executor.execute_bundle_within_current_scope(self.bundle)
    else:
      raise InvalidCommandArgumentsError(str(errors))

__plugin__ = Condition