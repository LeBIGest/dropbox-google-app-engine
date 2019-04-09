from google.appengine.ext import ndb
from file import File
from myuser import MyUser


class Folder(ndb.Model):
    path = ndb.StringProperty()
    parent_folder_path = ndb.StringProperty()
    inner_folders = ndb.StringProperty(repeated=True)
    files = ndb.StructuredProperty(File, repeated=True)
