from cdn_managers.rackspace_manager import RackspaceManager
from cdn_managers.aws_manager import AWSManager

class CdnFactory:
    managers = {
        'rackspace': RackspaceManager,
        'aws': AWSManager
    }

    @classmethod
    def get_cdn_manager(cls, server_type):
        return cls.managers[server_type]()
