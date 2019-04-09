from google.appengine.ext import ndb


class File(ndb.Model):
    filename = ndb.StringProperty()
    blob = ndb.BlobKeyProperty()
