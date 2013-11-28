from hal_configurator.lib.command_base import OperationBase, \
  InvalidCommandArgumentsError, ArgumentDescriptor


class Condition(OperationBase):
  """Create a condition"""
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
  
  @classmethod
  def get_empty_dict(cls):
    return{
            "Code":cls.get_code(),
            "Type":cls.get_name(), 
            "Arguments":{
              "Expression":"\"true\"==\"true\"",
              "Bundle":{
                "Name": "Incondition", 
                "Operations": []
              }
            }
          }
  def set_args(self, Expression, Bundle):
    self.kwargs["Expression"]= self.expression = Expression
    self.kwargs["Bundle"]=self.bundle = Bundle
    
  def run(self):  
    is_valid, errors = self.validate_args()
    if is_valid:
      print self.expression
      result = eval(self.expression)
      if result:
        self.executor.execute_bundle_within_current_scope(self.bundle)
    else:
      raise InvalidCommandArgumentsError(str(errors))

__plugin__ = Condition
