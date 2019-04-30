# Import all needed libraries
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers # Import blobstore handler class

# Import File model
from file import File


# Class which handle the file download
class DownloadFile(blobstore_handlers.BlobstoreDownloadHandler):

    """
    This method is call when the user will download a file
    It will display the file on the screen or download it directly
    """
    def get(self):

        # Gets the connected user
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        # Retrieve the filename thanks to the request
        filename = self.request.get('file_name')

        # Retrieve the folder path thanks to the request
        folder_path = self.request.get('folder_path')

        # Retrieve the File from the Datastore
        file_obj = File.query(ndb.AND(File.filename == filename, File.linked_folder_path == folder_path), ancestor=myuser.key).fetch()

        # If the file exists, send the file blob to download it
        if file_obj[0]:
            self.send_blob(file_obj[0].blob)
