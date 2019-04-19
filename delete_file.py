import webapp2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.blobstore import BlobInfo

from file import File
from folder import Folder


class DeleteFile(webapp2.RequestHandler):

    def delFile(self, folder, file):
        key = file.key
        delattr(file, 'key')
        idx = folder.files.index(file)
        del folder.files[idx]
        folder.put()
        blob_info = BlobInfo.get(file.blob)
        blob_info.delete()
        key.delete()

    def post(self):

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        filename = self.request.get('file_name')
        folder_path = self.request.get('folder_path')

        file_obj = File.query(ndb.AND(File.filename == filename, File.linked_folder_path == folder_path), ancestor=myuser.key).fetch()

        if file_obj[0]:
            folder_obj = Folder.query(ndb.AND(Folder.path == file_obj[0].linked_folder_path), ancestor=myuser.key).fetch()
            # print(file_obj[0])
            if folder_obj[0]:
                self.delFile(folder_obj[0], file_obj[0])
        self.redirect(folder_path)
