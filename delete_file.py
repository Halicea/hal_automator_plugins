import os
from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
class DeleteFile(OperationBase):
  code = "delete_file"
  def __init__(self, *args, **kwargs):
    super(DeleteFile, self).__init__(*args, **kwargs)

  @classmethod
  def get_arg_descriptors(cls):
    return [
      ArgumentDescriptor("FilePath", "The absolute file path of the file to be deleted", "text", os.path.exists)
    ]
  def run(self, **kwargs):
    os.remove(kwargs["FilePath"])

__plugin__ = DeleteFile

