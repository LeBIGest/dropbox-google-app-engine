import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from create_folder import CreateFolder
from folder_page import FolderPage
from myuser import MyUser
from folder import Folder


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'Logout'
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            if myuser is not None:
                folders = Folder.query(Folder.parent_folder_path == "/", ancestor=myuser.key).order(Folder.path).fetch()
            else:
                folders = []

            if myuser is None:
                myuser = MyUser(id=user.user_id(), user_key=myuser_key, email=str(user.email()))
                root_folder = Folder(parent=myuser.key, path="/", parent_folder_path="")
                root_folder.put()
                myuser.put()
                folders.append(root_folder)
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'
            myuser = None
            folders = None

        template_values = {
            'url': url,
            'url_string': url_string,
            'my_user': myuser,
            'folders': folders
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if action == 'Delete Folder':
            cur_folder = self.request.get('folder_path')

            cur_fold = Folder.query(Folder.path == cur_folder, ancestor=myuser.key).fetch()
            if cur_fold[0].path is "/":
                self.redirect('/')
                return
            else:
                parent_folder = Folder.query(Folder.path == cur_fold[0].parent_folder_path, ancestor=myuser.key).fetch()
                idx = parent_folder[0].inner_folders.index(cur_fold[0].path)
                del parent_folder[0].inner_folders[idx]
                cur_fold[0].key.delete()
                parent_folder[0].put()
                self.redirect('/')


app = webapp2.WSGIApplication([
    ('/create_folder', CreateFolder),
    ('/', MainPage),
    ('/(.*)', FolderPage)
], debug=True)
