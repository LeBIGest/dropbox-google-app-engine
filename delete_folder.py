import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from file import File
from folder import Folder
from delete_file import DeleteFile


class DeleteFolder(webapp2.RequestHandler):

    def delete_inner_folders(self, folder, origin_folder, my_user):

        deleteFile = DeleteFile()

        folders_found = Folder.query(Folder.parent_folder_path == folder.path, ancestor=my_user.key).fetch()
        for sub_folder in folders_found:
            print(sub_folder)
            self.delete_inner_folders(sub_folder, origin_folder, my_user)
        if len(folders_found) <= 0:
            files_found = File.query(ndb.AND(File.linked_folder_path == folder.path), ancestor=my_user.key).fetch()
            for inner_file in files_found:
                deleteFile.delFile(folder, inner_file)
            if folder.path == origin_folder:
                return
            folder.key.delete()
            parent_folder = Folder.query(Folder.path == folder.parent_folder_path, ancestor=my_user.key).fetch()
            if len(parent_folder) > 0:
                self.delete_inner_folders(parent_folder[0], origin_folder, my_user)

    def post(self):

        action = self.request.get('button')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if action == 'Delete Folder':
            del_folder = self.request.get('folder_path')
            cur_folder = self.request.get('cur_folder_path')
            del_fold = Folder.query(ndb.AND(Folder.path == del_folder, Folder.parent_folder_path == cur_folder), ancestor=myuser.key).fetch()
            if del_fold[0].path is "/":
                self.redirect(cur_folder)
                return
            else:
                parent_folder = Folder.query(Folder.path == del_fold[0].parent_folder_path, ancestor=myuser.key).fetch()
                idx = parent_folder[0].inner_folders.index(del_fold[0].path)
                self.delete_inner_folders(del_fold[0], del_fold[0].path, myuser)
                del parent_folder[0].inner_folders[idx]
                del_fold[0].key.delete()
                parent_folder[0].put()
                self.redirect(cur_folder)
