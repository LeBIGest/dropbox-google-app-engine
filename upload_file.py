from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

from file import File
from folder import Folder


class UploadFile(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):

        cur_folder_path = self.request.get('cur_folder_path')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        upload = self.get_uploads()[0]

        blobinfo = blobstore.BlobInfo(upload.key())

        new_file = File(parent=myuser.key, linked_folder_path=cur_folder_path, filename=blobinfo.filename, size=blobinfo.size,
                        created_at=blobinfo.creation, type=blobinfo.content_type, blob=upload.key())
        new_file.put()

        current_folder_obj = Folder.query(Folder.path == cur_folder_path, ancestor=myuser.key).fetch()

        current_folder_obj[0].files.append(new_file)
        current_folder_obj[0].put()

        print("________________________")
        print(new_file)
        print(current_folder_obj[0].files[0])
        print("________________________")

        self.redirect(cur_folder_path)
