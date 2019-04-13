import webapp2
from google.appengine.api.blobstore import blobstore

import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from folder import Folder

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class FolderPage(webapp2.RequestHandler):
    def get(self, folder):

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        folder_obj = Folder.query(Folder.path == str("/" + folder), ancestor=myuser.key).fetch()

        if folder_obj:
            send_folder_obj = folder_obj[0]
        else:
            send_folder_obj = []

        template_values = {
            'url': folder,
            'upload_url': blobstore.create_upload_url('/upload'),
            'folder': send_folder_obj
        }

        template = JINJA_ENVIRONMENT.get_template('folder_page.html')
        self.response.write(template.render(template_values))
