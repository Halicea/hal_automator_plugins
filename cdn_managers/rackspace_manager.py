from cdn_manager import CdnManager
import cloudfiles
import os

class RackspaceManager(CdnManager):
    def __init__(self):
        self.conn = None
        self.container = None

    def authenticate(self, user, password):
        self.conn = cloudfiles.get_connection(user, password)

    def set_container(self, cont_name):
        self.container = self.conn.get_container(cont_name)

    def upload_file(self, object_name, file_path):
        for x in xrange(1, 5):
            try:
                obj = self.get_container().create_object(object_name)
                obj.load_from_filename(file_path)
                break
            except Exception, ex:
                print "Got an error", ex.message
                print "tries left:", 5-x
        return object_name

    def download_file(self, object_name, out_file):
        img = self.get_container().get_object(object_name)
        img.save_to_filename(out_file)
        return out_file

    def download_all_file_in_container(self, out_path):
        container_files = self.get_container_data()
        for x in container_files:
            print 'Downloading file ',x.name
            file_out_path = os.path.join(out_path, x.name)
            self.download_file(x.name, file_out_path)

    def get_container_data(self):
        return self.get_container().get_objects()

    def get_container(self):
        if not self.container:
            raise Exception('Container is not set. Please set it first')
        else:
            return self.container
