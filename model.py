
from google.appengine.ext import ndb;

class model(ndb.Model):
    anagramK = ndb.StringProperty()
    User = ndb.StringProperty()
    wordList = ndb.StringProperty(repeated=True)
    wCount = ndb.IntegerProperty()
    lCount = ndb.IntegerProperty()


