# Import the ndb Class from the Google App Engine
from google.appengine.ext import ndb


# Model to represent a user in the application
class MyUser(ndb.Model):

    # The key of the User Model (Google app engine) to retrieve easier the user
    user_key = ndb.KeyProperty()

    # The user mail
    email = ndb.StringProperty()
