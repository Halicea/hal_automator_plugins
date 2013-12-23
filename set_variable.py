from hal_configurator.lib.command_base import \
  OperationBase, InvalidCommandArgumentsError, ArgumentDescriptor

class SetVariable(OperationBase):
  def __init__(self,*args, **kwargs):
    super(SetVariable, self).__init__(*args, **kwargs)


  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Variable", "", "text"),
            ArgumentDescriptor("NewValue", "", "text"),
            ]
  def run(self):
    is_valid, errors = self.validate_args()
    su = self.value_substitutor.substitute
    if is_valid:
      r = filter(lambda x: x['name']==su(self.kwargs['Variable']), self.executor.bundle_vars)
      if r:
        r[0]['value'] = su(self.kwargs["NewValue"])
      else:
        self.executor.bundle_vars.append({'name':su(self.kwargs['Variable']), 'value':su(self.kwargs["NewValue"])})
    else:
      raise InvalidCommandArgumentsError(str(errors))

__plugin__ = SetVariable