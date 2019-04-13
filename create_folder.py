import webapp2
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


class CreateFolder(webapp2.RequestHandler):

    def post(self):

        action = self.request.get('button')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if action == 'Add Folder':
            new_folder = self.request.get('new_folder')
            cur_folder = self.request.get('current_folder')

            if len(new_folder) <= 0:
                self.redirect(str(cur_folder))
                return
            else:
                cur_folder_obj = ndb.get_multi(
                    set(Folder.query(Folder.path == cur_folder).fetch(keys_only=True)).intersection(
                        Folder.query(ancestor=myuser.key).fetch(keys_only=True)))

                if ndb.get_multi(set(Folder.query(Folder.path == str(cur_folder_obj[0].path + new_folder + "/")).fetch(
                        keys_only=True)).intersection(Folder.query(ancestor=myuser.key).fetch(keys_only=True))):
                    self.redirect(str(cur_folder))
                else:
                    new_folder_obj = Folder(parent=myuser.key, path=str(cur_folder_obj[0].path + new_folder + "/"),
                                            parent_folder_path=cur_folder_obj[0].path)
                    new_folder_obj.put()
                    cur_folder_obj[0].inner_folders.append(new_folder_obj.path)
                    cur_folder_obj[0].put()
                    self.redirect(str(cur_folder))
