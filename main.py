# Import all needed libraries
import webapp2  # Python web framework compatible with Google app engine
import jinja2  # Python templating framework
from google.appengine.api import users  # users interface from the Google App Engine
from google.appengine.ext import ndb  # Cloud Datastore interface for Python
from google.appengine.ext import blobstore  # Cloud interface for store files
import os

# Import some classes
from create_folder import CreateFolder
from delete_file import DeleteFile
from delete_folder import DeleteFolder
from download_file import DownloadFile
from folder_page import FolderPage

# Import all needed models
from file import File
from myuser import MyUser
from folder import Folder
from upload_file import UploadFile

# Set up the templating environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):

    """
    This method is call when the user go on the index page
    It sends all needed information to the HTML File (user, files or folders)
    """
    def get(self):

        # Set the response type (here html)
        self.response.headers['Content-Type'] = 'text/html'

        # Set a url and url_string for login / logout
        url = ''
        url_string = ''

        # Get the connected user
        user = users.get_current_user()

        # If the user is connected
        if user:

            # Create the logout url and the appropriate label
            url = users.create_logout_url(self.request.uri)
            url_string = 'Logout'

            # Retrieves the linked MyUser object
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            # If the myuser exists, get all folders and files of the root folder
            if myuser is not None:
                folders = Folder.query(Folder.parent_folder_path == "/", ancestor=myuser.key).order(Folder.path).fetch()
                files = File.query(File.linked_folder_path == "/", ancestor=myuser.key).order(File.created_at).fetch()

            # Set these values to empty
            else:
                folders = []
                files = []

            # If the myuser does not exist, create one and the root folder
            if myuser is None:
                myuser = MyUser(id=user.user_id(), user_key=myuser_key, email=str(user.email()))
                root_folder = Folder(parent=myuser.key, path="/", parent_folder_path="")
                root_folder.put()
                myuser.put()

        # If the user does not exist, set variables to a default value
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'
            myuser = None
            folders = None
            files = None

        # Create the template object send to the view
        template_values = {
            'url': url,
            'url_string': url_string,
            'my_user': myuser,
            'upload_url': blobstore.create_upload_url('/upload'),
            'folders': folders,
            'files': files,
        }

        # Get the view template, fill it with the above object and send to the response
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# Declare the Web APplication with all needed routes
app = webapp2.WSGIApplication([
    ('/create_folder', CreateFolder),  # Route to create a new folder
    ('/delete_folder', DeleteFolder),  # Route to delete a folder
    ('/upload', UploadFile),  # Route to upload a file in a folder
    ('/download', DownloadFile),  # Route to download a file
    ('/delete_file', DeleteFile),  # Route to delete a file
    ('/', MainPage),  # Route to the index page (root folder)
    ('/(.*)', FolderPage)  # Route to other pages (all sub_folders)
], debug=True)
