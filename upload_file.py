# Import all needed libraries
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.blobstore import BlobInfo
from google.appengine.ext.webapp import blobstore_handlers

# Import File and Folder models
from file import File
from folder import Folder


# This class will handle the upload request ('/upload')
# ANd create a File entity in the Datastore
class UploadFile(blobstore_handlers.BlobstoreUploadHandler):

    """
    This method will check if the file already exist in the current folder
    """
    def _check_if_file_exists(self, folder, file_obj):

        # Browse all files in the current folder
        # Return True if the file already exist and False if not
        for file in folder.files:
            if file.filename == file_obj[0] and file.type == file_obj[1]:
                return True
        return False

    """
    Handle the '/upload' request and create or not the File Entity
    """
    def post(self):

        # Get the path of the current folder in the request body
        cur_folder_path = self.request.get('cur_folder_path')

        # Retrieve the user in the Datastore
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        # Check if a file is uploaded
        if not self.get_uploads():
            self.redirect(cur_folder_path)
            return

        # Get the uploaded file from the request
        upload = self.get_uploads()[0]

        # Create a blobInfo Entity linked to the new File
        blobinfo = blobstore.BlobInfo(upload.key())

        # Create the new File with all needed information
        new_file = File(parent=myuser.key, linked_folder_path=cur_folder_path, filename=blobinfo.filename, size=blobinfo.size,
                        created_at=blobinfo.creation, type=blobinfo.content_type, md5_hash=blobinfo.md5_hash, blob=upload.key())

        # Retrieve the current folder where the new file will be
        current_folder_obj = Folder.query(Folder.path == cur_folder_path, ancestor=myuser.key).fetch()

        # Create a temporary file with needed information to check if it already exists in the current folder
        file = [new_file.filename, new_file.type]

        # If the file does not already exist in the folder, save it and add it to the folder files array
        if self._check_if_file_exists(current_folder_obj[0], file) is False:
            new_file.put()
            current_folder_obj[0].files.append(new_file)
            current_folder_obj[0].put()

        # Otherwise, delete the new BlobInfo created
        else:
            blob_info = BlobInfo.get(new_file.blob)
            blob_info.delete()

        # Redirect to the current folder page
        self.redirect(cur_folder_path)
