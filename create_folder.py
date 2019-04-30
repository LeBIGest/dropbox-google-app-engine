# Import all needed libraries
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

# Import the Folder Model
from folder import Folder


# This class handle the '/create_folder' request
# It will create a folder Entity and add the path in the sub folders of the parent directory
class CreateFolder(webapp2.RequestHandler):

    """
    Method to handle the POST request
    """
    def post(self):

        # Get the action of the request
        action = self.request.get('button')

        # Retrieve the connected user
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        # Check if it is the right action
        if action == 'Add Folder':

            # Get the name of the new folder and the current folder path
            new_folder = self.request.get('new_folder')
            cur_folder = self.request.get('current_folder')

            # If the name of the new folder is empty, it redirects to the current folder page
            if len(new_folder) <= 0:
                self.redirect(str(cur_folder))
                return

            # Otherwise
            else:

                # Get the current folder object from the Datastore
                cur_folder_obj = ndb.get_multi(
                    set(Folder.query(Folder.path == cur_folder).fetch(keys_only=True)).intersection(
                        Folder.query(ancestor=myuser.key).fetch(keys_only=True)))

                # Check if the potential new folder does not already exist in the Datastore
                if ndb.get_multi(set(Folder.query(Folder.path == str(cur_folder_obj[0].path + new_folder + "/")).fetch(
                        keys_only=True)).intersection(Folder.query(ancestor=myuser.key).fetch(keys_only=True))):

                    # If true, redirect to the current folder page
                    self.redirect(str(cur_folder))

                # Otherwise
                else:

                    # Create the new folder Entity
                    new_folder_obj = Folder(parent=myuser.key, path=str(cur_folder_obj[0].path + new_folder + "/"),
                                            parent_folder_path=cur_folder_obj[0].path)

                    # Save the creation
                    new_folder_obj.put()

                    # Add the path of the new folder in the array of sub folders of the parent folder
                    cur_folder_obj[0].inner_folders.append(new_folder_obj.path)
                    cur_folder_obj[0].put()

                    # Redirect to the current folder page
                    self.redirect(str(cur_folder))
