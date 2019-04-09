from google.appengine.ext import ndb
# from folder import Folder


class MyUser(ndb.Model):
    key = ndb.KeyProperty()
    email = ndb.StringProperty()
    # root_folder = ndb.StructuredProperty(Folder)
