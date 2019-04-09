import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from folder import Folder
from myuser import MyUser


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
            # unsorted_folders = []
            # for elem in myuser.root_folder.inner_folders:
            #     unsorted_folders.append(elem)
            # folders = unsorted_folders.sort()

            if myuser is None:
                myuser = MyUser(id=user.user_id(), email=str(user.email()))
                root_folder = Folder(user_id=user.user_id(), path="/")
                root_folder.put()
                myuser.root_folder = root_folder
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'
            myuser = None
            # folders = None

        template_values = {
            'url': url,
            'url_string': url_string,
            'my_user': myuser
            # 'folders': folders
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'Add Folder':
            new_folder = self.request.get('new_folder')
            cur_folder = self.request.get('current_folder')

            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            print(cur_folder)
            cur_folder_obj = ndb.get_multi(set(Folder.query(Folder.path == cur_folder).fetch(keys_only=True)).intersection(Folder.query(Folder.user_id == user.user_id()).fetch(keys_only=True)))

            print(cur_folder_obj)

            new_folder_obj = Folder(user_id=user.user_id(), path=str(cur_folder_obj[0].path + new_folder + "/"))
            new_folder_obj.put()

            print(myuser)

            myuser.root_folder.inner_folders.append(new_folder_obj.path)
            cur_folder_obj[0].inner_folders.append(new_folder_obj.path)
            # TODO Faire dans l'ordre /test -> /testrs -> /truc/dede
            myuser.put()

            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
