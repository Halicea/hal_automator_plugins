import os
from hal_configurator.lib.config_loaders import FileConfigLoader
from hal_configurator.lib.command_base import \
    OperationBase, InvalidCommandArgumentsError, ArgumentDescriptor
from hal_configurator.lib.models.build_filter import ConfigBuildFilter
from hal_configurator.lib.configurator_console import main as console_main

class ExecuteHalConfig(OperationBase):

    """Replaces File(Destination) from a resource file supplied by URI"""

    def __init__(self, *args, **kwargs):
        super(ExecuteHalConfig, self).__init__(*args, **kwargs)
        self.result = ''
    
    @classmethod
    def get_arg_descriptors(cls):
        return [
            ArgumentDescriptor(
                "ConfigPath", "External Configuration Directory", "text"),
			ArgumentDescriptor(
				"CustomVars", "Custom Variables array", "json", is_optional=True),
            ArgumentDescriptor(
				"ExcludedBundles", "Excluded Bundles array", "json", is_optional=True)
        ]
        
    def set_args(self, ConfigPath, CustomVars, ExcludedBundles):
        """
        :param ConfigPath:
        :type ConfigPath: str
        """
        self.kwargs["ConfigPath"] = self.ConfigPath = ConfigPath
        self.kwargs["CustomVars"] = self.CustomVars = CustomVars
        self.kwargs["ExcludedBundles"] = self.ExcludedBundles = ExcludedBundles

    def run(self):
        loger = self.executor.log
        exec_dir = os.getcwd()
        is_valid, errors = self.validate_args()
        res = None
        if is_valid:
            res = self.value_substitutor.substitute(self.ConfigPath)
        else:
            raise InvalidCommandArgumentsError(str(errors))

        if not os.path.isabs(res):
            config_loader = self.executor.parent.config_loader
            dr = os.path.dirname(config_loader.config_file)
            res = os.path.join(dr, res)
        arguments = ["ExecuteHalConfig", "-from", "fs", res]
        arguments.append("-dir");arguments.append(exec_dir)
        if self.CustomVars:
            arguments.append("-custom-vars");arguments.append(self.CustomVars)
        if self.ExcludedBundles:
            arguments.append("-excluded-bundles");arguments.append(self.ExcludedBundles)
        if self.executor.verbose:
            arguments.append("-v")
        console_main(arguments, loger)


 
    @classmethod
    def get_name(cls):
        return "Execute Hal confguration"

__plugin__ = ExecuteHalConfig
