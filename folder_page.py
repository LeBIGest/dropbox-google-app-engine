# Import all needed libraries
import webapp2
from google.appengine.api.blobstore import blobstore
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

# Import the folder Model
from folder import Folder

# Set up the templating environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


# This class will handle all sub folder pages (except the root folder)
class FolderPage(webapp2.RequestHandler):

    """
    This method is call when the user go on each folder page
    It sends all needed information to the HTML File (user, files or folders)

    It takes one parameter corresponding to the folder path passed in the url (ex: /test)
    """
    def get(self, folder):

        # Get the connected user
        user = users.get_current_user()

        # If the user is connected
        if user:

            # Create the logout url and the appropriate label
            url = users.create_logout_url('/')
            url_string = 'Logout'

            # Retrieves the linked MyUser object
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            # If the myuser exists, get the current folder Entity
            if myuser:
                folder_obj = Folder.query(Folder.path == str("/" + folder), ancestor=myuser.key).fetch()

                if folder_obj:
                    send_folder_obj = folder_obj[0]
                else:
                    send_folder_obj = []

        # If the user is not connected, Send default values
        else:
            url = users.create_login_url('/')
            url_string = 'Login'
            myuser = None
            folder = folder
            send_folder_obj = None

        # Build the template values object to send to the view
        template_values = {
            'my_user': myuser,
            'url_string': url_string,
            'url': url,
            'upload_url': blobstore.create_upload_url('/upload'),
            'folder': send_folder_obj
        }

        # Get the view template, fill it with the above object and send to the response
        template = JINJA_ENVIRONMENT.get_template('folder_page.html')
        self.response.write(template.render(template_values))
