from hal_configurator.lib.command_base import OperationBase, \
  InvalidCommandArgumentsError, ArgumentDescriptor
FORLOOP_BUNDLE = 'InForLoop'
OperationBase.register_bundle(FORLOOP_BUNDLE)

class ForLoop(OperationBase):
  """Create a condition"""
  code = "condition"
  def __init__(self,*args, **kwargs):
    super(ForLoop, self).__init__(*args, **kwargs)
    self.result = ''

  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Array", "Comma separated array", "list"),
            ArgumentDescriptor("Bundle", "Operations Bundle", "OperationsBundle"),
           ]

  @classmethod
  def get_empty_dict(cls):
    return{
            "Code":cls.get_code(),
            "Type":cls.get_name(),
            "Arguments":{
              "Array":"[1,2,3]",
              "Bundle":{
                "Name": FORLOOP_BUNDLE,
                "Operations": []
              }
            }
          }
  def set_args(self, Array, Bundle):
    self.kwargs["Array"]= self.array = Array
    self.kwargs["Bundle"]=self.bundle = Bundle

  def run(self):
    is_valid, errors = self.validate_args()
    if is_valid:
      if not self.array.startswith('[') or not self.array.endswith(']'):
        self.array='['+self.array+']'
      result = eval(self.array)
      index = 0
      for k in result:
        self.bundle["Variables"] = [{'name':'item', 'value':str(k)}, {'name':'index', 'value':str(index)}]
        self.executor.execute_bundle_within_current_scope(self.bundle)
        index+=1
    else:
      raise InvalidCommandArgumentsError(str(errors))

__plugin__ = ForLoop
