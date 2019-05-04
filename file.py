# Import the ndb Class from the Google App Engine
from google.appengine.ext import ndb


# The File Model to store all files in the application
class File(ndb.Model):

    # The path of the folder where the file is
    linked_folder_path = ndb.StringProperty()

    # The properties of the file
    filename = ndb.StringProperty()  # the filename
    size = ndb.IntegerProperty()  # the size of the file
    created_at = ndb.DateTimeProperty()  # the date and time creation
    type = ndb.StringProperty()  # the type of the file
    md5_hash = ndb.StringProperty()  # the content of the file in a MD5 hash format

    # The blob of the file (content data)
    blob = ndb.BlobKeyProperty()
