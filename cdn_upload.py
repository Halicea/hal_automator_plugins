from hal_configurator.lib.command_base import OperationBase, ArgumentDescriptor
from cdn_factory import CdnFactory


class CdnUpload(OperationBase):
    code = "cdn_upload"

    def __init__(self, *args, **kwargs):
        super(CdnUpload, self).__init__(*args, **kwargs)

    @classmethod
    def get_arg_descriptors(cls):
        return [
            ArgumentDescriptor(
                "FilePath",
                "The absolute file path of the file to be uploaded", "text"),
            ArgumentDescriptor("UploadName", "The name of the upload", "text"),
            ArgumentDescriptor("BucketName", "The name of the bucket", "text"),
            ArgumentDescriptor("User", "UserName", "text"),

            ArgumentDescriptor("ApiToken", "the api token", "text"),
            ArgumentDescriptor("CdnProvider", "Rackspace or Amazon", "text")
        ]

    def run(self):
        kwargs = self.kwargs
        file_path = kwargs["FilePath"]
        upload_name = kwargs["UploadName"]
        token = kwargs["ApiToken"]
        user = kwargs["User"]
        bucket = kwargs["BucketName"]
        server_type = kwargs["CdnProvider"]
        if file_path.startswith('file://'):
            file_path = file_path[len('file://'):]

        import pdb; pdb.set_trace();
        manager = CdnFactory.get_cdn_manager(server_type)
        manager.authenticate(user, token)
        manager.set_container(bucket)
        manager.upload_file(upload_name, file_path)


__plugin__ = CdnUpload
