import os
import subprocess
import shlex
from hal_configurator.lib.command_base import OperationBase, InvalidCommandArgumentsError,\
  ArgumentDescriptor
class ShellScriptError(Exception):
  def __init__(self, message):
    super(ShellScriptError, self).__init__(message)

class ShellScript(OperationBase):

  def __init__(self, *args, **kwargs):
    super(ShellScript, self).__init__(*args, **kwargs)

  def get_result(self):
    return OperationBase.get_result(self)

  @classmethod
  def get_name(cls):
    return "Execute Shell Script"

  @classmethod
  def get_arg_descriptors(cls):
    return [
            ArgumentDescriptor("working directory", "relative or absolute path where the command will be executed", "text"),
            ArgumentDescriptor("command", "shell command that will be executed", "text"),
            ArgumentDescriptor("is sudo", "Whether to execute with sudo privileges", "boolean"),
            ArgumentDescriptor("catch shell output", "Whether the result should be the shell output", "boolean")
           ]

  def set_args(self, **kwargs):
    self.kwargs = kwargs
    is_valid, errors = self.validate_args()
    if is_valid:
      self.command = self.kwargs["command"]
      self.is_sudo = self.kwargs["is sudo"]
      self.catch_shell_output = bool(kwargs["catch shell output"])
      self.working_dir = self.kwargs["working directory"].startswith("/") and self.kwargs["working directory"] or \
                         os.path.join(os.getcwd(), self.kwargs["working directory"])
    else:
      raise InvalidCommandArgumentsError(str(errors))

  def run(self):
    print os.getcwd()
    
    cmd_str = self.value_substitutor.substitute(self.command)
    arg_list = args = shlex.split(cmd_str)
    cmd = arg_list
    p = None
    print cmd
    if os.name != 'nt':
      p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           close_fds=True, cwd=self.working_dir, env=os.environ)
    else:
      p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=self.working_dir, env=os.environ) 

    for line in iter(p.stdout.readline, b''):
      self.log.write("\t%s"%line[:-1])

    for line in iter(p.stderr.readline, b''):
      self.log.write("\t%s"%line[:-1])
    code = p.wait()
    for line in iter(p.stderr.readline, b''):
      self.log.write("\t!%s"%line[:-1])
    self.log.write('\tExit code:%s'%code)
    if code>0:
      self.log.write(cmd_str)
      raise ShellScriptError('Shell command returned an error code different than 0')

__plugin__ = ShellScript
