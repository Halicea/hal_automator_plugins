import json
import codecs
from hal_configurator.lib.command_base import \
  OperationBase, InvalidCommandArgumentsError, ArgumentDescriptor

class SetJsonValueInFile(OperationBase):
  def __init__(self,*args, **kwargs):
    super(SetJsonValueInFile, self).__init__(*args, **kwargs)
    self.self_managed_variables = True
    self.self_managed_resources = True

  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("Value", "The actual Value", "text"),
            ArgumentDescriptor("ValueIsJson", "Value is Json", "bool", default_value_lambda=lambda:False),
            ArgumentDescriptor("PathToSet", "To Which key to set the value", "text"),
            ArgumentDescriptor("File", "The Json file", "text"),
            ArgumentDescriptor("Destination", "Where to save the Json file", "text")
            ]

  def run(self):
    su = self.value_substitutor.substitute
    path_to_set = su(self.kwargs['PathToSet'])
    is_json = su(self.kwargs["ValueIsJson"]) in ['true', 'True', '1', 'Yes', 'yes', 'YES']
    json_file = su(self.kwargs['File'])
    value = su(self.kwargs['Value'])
    destination_json = su(self.kwargs['Destination'])
    is_valid, errors = self.validate_args()
    if is_valid:
      to_repl = value
      if is_json:
        to_repl = json.loads(to_repl)
      j = json.loads(codecs.open(json_file, 'r', 'utf-8').read())
      if path_to_set in j:
        j[path_to_set] = to_repl
      elif '=>' in path_to_set:
        elements = path_to_set.split('=>')
        subel = j
        for i in range(0,len(elements)):
          el = elements[i]
          if isinstance(subel, list):
            el = int(elements[i])
          if i+1 == len(elements):
            subel[el]=to_repl
          else:
            subel = subel[el]

      with codecs.open(destination_json, 'w', 'utf-8') as f:
        f.write(json.dumps(j, indent=2, sort_keys=True))
        f.close()
    else:
      raise InvalidCommandArgumentsError(str(errors))

__plugin__ = SetJsonValueInFile