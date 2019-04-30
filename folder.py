# Import the ndb Class from the Google App Engine
from google.appengine.ext import ndb

# Import the File Model
from file import File


# The Folder class to represent a folder in the application
class Folder(ndb.Model):

    # The path of the folder
    path = ndb.StringProperty()

    # The path of the parent folder
    parent_folder_path = ndb.StringProperty()

    # An array of paths which represent all sub folders of this folder
    inner_folders = ndb.StringProperty(repeated=True)

    # An array of File which the contained files in this folder
    files = ndb.StructuredProperty(File, repeated=True)
