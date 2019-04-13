from google.appengine.ext import ndb


class File(ndb.Model):
    linked_folder_path = ndb.StringProperty()
    filename = ndb.StringProperty()
    size = ndb.IntegerProperty()
    created_at = ndb.DateTimeProperty()
    type = ndb.StringProperty()
    blob = ndb.BlobKeyProperty()
