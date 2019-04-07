from google.appengine.ext import ndb


class MyUser(ndb.Model):
    username = ndb.StringProperty()
    wordCount = ndb.IntegerProperty()
    anaCount = ndb.IntegerProperty()

