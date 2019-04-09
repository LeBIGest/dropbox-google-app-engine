from google.appengine.api.users import User
from google.appengine.ext import ndb
from file import File


class Folder(ndb.Model):
    user_id = ndb.StringProperty()
    path = ndb.StringProperty()
    inner_folders = ndb.StringProperty(repeated=True)
    files = ndb.StructuredProperty(File, repeated=True)
