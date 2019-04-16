from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.blobstore import BlobInfo
from google.appengine.ext.webapp import blobstore_handlers

from file import File
from folder import Folder


class UploadFile(blobstore_handlers.BlobstoreUploadHandler):

    def _check_if_file_exists(self, folder, file_obj):

        for file in folder.files:
            if file.filename == file_obj[0] and file.type == file_obj[1]:
                return True
        return False

    def post(self):

        cur_folder_path = self.request.get('cur_folder_path')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if not self.get_uploads():
            self.redirect(cur_folder_path)
            return

        upload = self.get_uploads()[0]

        blobinfo = blobstore.BlobInfo(upload.key())

        new_file = File(parent=myuser.key, linked_folder_path=cur_folder_path, filename=blobinfo.filename, size=blobinfo.size,
                        created_at=blobinfo.creation, type=blobinfo.content_type, blob=upload.key())

        current_folder_obj = Folder.query(Folder.path == cur_folder_path, ancestor=myuser.key).fetch()

        file = [new_file.filename, new_file.type]

        if self._check_if_file_exists(current_folder_obj[0], file) is False:
            new_file.put()
            current_folder_obj[0].files.append(new_file)
            current_folder_obj[0].put()
        else:
            blob_info = BlobInfo.get(new_file.blob)
            blob_info.delete()

        self.redirect(cur_folder_path)
