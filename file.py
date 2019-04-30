# Import the ndb Class from the Google App Engine
from google.appengine.ext import ndb


# The File Model to store all files in the application
class File(ndb.Model):

    # The path of the folder where the file is
    linked_folder_path = ndb.StringProperty()

    # The properties of the file
    filename = ndb.StringProperty()
    size = ndb.IntegerProperty()
    created_at = ndb.DateTimeProperty()
    type = ndb.StringProperty()
    md5_hash = ndb.StringProperty()

    # The blob of the file (content data)
    blob = ndb.BlobKeyProperty()
