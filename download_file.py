from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

from file import File


class DownloadFile(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        filename = self.request.get('file_name')
        folder_path = self.request.get('folder_path')

        file_obj = File.query(ndb.AND(File.filename == filename, File.linked_folder_path == folder_path), ancestor=myuser.key).fetch()

        if file_obj[0]:
            self.send_blob(file_obj[0].blob)
