import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from folder import Folder


class DeleteFolder(webapp2.RequestHandler):

    def post(self):

        action = self.request.get('button')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if action == 'Delete Folder':
            del_folder = self.request.get('folder_path')
            cur_folder = self.request.get('cur_folder_path')
            del_fold = Folder.query(Folder.path == del_folder, ancestor=myuser.key).fetch()
            if del_fold[0].path is "/":
                self.redirect(cur_folder)
                return
            else:
                parent_folder = Folder.query(Folder.path == del_fold[0].parent_folder_path, ancestor=myuser.key).fetch()
                idx = parent_folder[0].inner_folders.index(del_fold[0].path)
                del parent_folder[0].inner_folders[idx]
                del_fold[0].key.delete()
                parent_folder[0].put()
                self.redirect(cur_folder)
