# Import all needed libraries
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.blobstore import BlobInfo

# Import File and Folder Model
from file import File
from folder import Folder


# This class will handle the deletion of the files
class DeleteFile(webapp2.RequestHandler):

    """
    Permit the deletion of the file parameter and in the files array contained in the folder parameter
    """
    def delFile(self, folder, file):

        # Get the key of the file
        key = file.key

        # Delete the file from the array of files from the folder
        delattr(file, 'key')
        idx = folder.files.index(file)
        del folder.files[idx]

        # Update the folder object
        folder.put()

        # Delete the linked BlobInfo from the Datastore
        blob_info = BlobInfo.get(file.blob)
        blob_info.delete()

        # Delete the File Entity
        key.delete()

    """
    Handle the '/delete_file' request
    It will retrieve the File from the Datastore and delete it
    """
    def post(self):

        # Retrieve the connected user
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        # Get the file name and the folder from the request
        filename = self.request.get('file_name')
        folder_path = self.request.get('folder_path')

        # Retrieve the File from the Datastore
        file_obj = File.query(ndb.AND(File.filename == filename, File.linked_folder_path == folder_path), ancestor=myuser.key).fetch()

        if file_obj:

            # If the file exists, get the linked Folder
            if file_obj[0]:
                folder_obj = Folder.query(ndb.AND(Folder.path == file_obj[0].linked_folder_path), ancestor=myuser.key).fetch()

                # If the folder exist, call the 'delFile' method
                if folder_obj[0]:
                    self.delFile(folder_obj[0], file_obj[0])

        # Redirect to the current folder page
        self.redirect(folder_path)
