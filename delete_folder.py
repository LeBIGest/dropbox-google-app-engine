# Import all needed libraries
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

# Import File and Folder Model
from file import File
from folder import Folder

# Import the DeleteFile object to permit to delete files in a folder
from delete_file import DeleteFile


# Class to handle the deletion of the folders
class DeleteFolder(webapp2.RequestHandler):
    """
    Delete all inner folders and files in the future deleted folder
    """

    def delete_inner_folders(self, folder, origin_folder, my_user):

        # Call the DeleteFile Object
        deleteFile = DeleteFile()

        # Get all inner folders of the future deleted folder
        folders_found = Folder.query(Folder.parent_folder_path == folder.path, ancestor=my_user.key).fetch()

        # Browse all folders
        for sub_folder in folders_found:
            # Call the recursively the function to get all inner folders of the inner folders
            self.delete_inner_folders(sub_folder, origin_folder, my_user)

        # If the folder has not inner folders
        if len(folders_found) <= 0:

            # Retrieve all files contained in the folder
            files_found = File.query(ndb.AND(File.linked_folder_path == folder.path), ancestor=my_user.key).fetch()

            # Delete all files using the DeleteFile method ('delFile')
            for inner_file in files_found:
                deleteFile.delFile(folder, inner_file)

            # Create a stop condition, if the folder path is a future deleted folder, return
            if folder.path == origin_folder:
                return

            # Delete the folder
            folder.key.delete()

            # Repeat the function with the parent folder
            parent_folder = Folder.query(Folder.path == folder.parent_folder_path, ancestor=my_user.key).fetch()
            if len(parent_folder) > 0:
                self.delete_inner_folders(parent_folder[0], origin_folder, my_user)

    """
    Handle the 'delete_folder' request
    It will retrieve the folder in the Datastore and delete all its content
    """

    def post(self):

        # Get the called action
        action = self.request.get('button')

        # Get the connected user
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        # Check if the action is the right action
        if action == 'Delete Folder':

            # Get the future deleted folder path and the current folder
            del_folder = self.request.get('folder_path')
            cur_folder = self.request.get('cur_folder_path')

            # Retrieve the folder from the Datastore
            del_fold = Folder.query(ndb.AND(Folder.path == del_folder, Folder.parent_folder_path == cur_folder),
                                    ancestor=myuser.key).fetch()

            if del_fold:

                # We cannot delete the root folder (with the '/' path)
                if del_fold[0].path is "/":

                    # Redirect to the current folder page
                    self.redirect(cur_folder)
                    return

                # Otherwise
                else:

                    # Get the parent folder
                    parent_folder = Folder.query(Folder.path == del_fold[0].parent_folder_path, ancestor=myuser.key).fetch()

                    # Find the index of the deleted folder and delete it from the array
                    idx = parent_folder[0].inner_folders.index(del_fold[0].path)

                    # Delete all inner foldes and files from this folder
                    self.delete_inner_folders(del_fold[0], del_fold[0].path, myuser)
                    del parent_folder[0].inner_folders[idx]

                    # Delete the folder Entity
                    del_fold[0].key.delete()

                    # Update the parent folder
                    parent_folder[0].put()

            # Redirect to the current folder page
            self.redirect(cur_folder)
