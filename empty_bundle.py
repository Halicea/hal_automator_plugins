from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
EMPTY_BUNDLE = 'InForLoop'
OperationBase.register_bundle(EMPTY_BUNDLE)

class EmptyBundle(OperationBase):
  def __init__(self,*args, **kwargs):
    super(EmptyBundle, self).__init__(*args, **kwargs)
    self.result = ''

  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Bundle", "Operations Bundle", "OperationsBundle"),
           ]
  @classmethod
  def get_empty_dict(cls):
    return{
            "Code":cls.get_code(),
            "Type":cls.get_name(),
            "Arguments":{
              "Bundle":{
                "Name": EMPTY_BUNDLE,
                "Operations": []
              }
            }
          }
  def run(self):
    self.executor.execute_bundle_within_current_scope(self.kwargs["Bundle"])
__plugin__ = EmptyBundle
