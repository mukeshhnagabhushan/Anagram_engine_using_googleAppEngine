
import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from model import model
from add import Add
from upload import upload
from subAnag import sub

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url' : users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if myuser == None:
            myuser = MyUser(id=user.user_id(),username=user.email(),anaCount=0,wordCount=0)
            myuser.put()

        anagrmEngine = model.query().fetch()

        template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'user':user,
            'anagrmEngine':anagrmEngine,
            'anaCount':myuser.anaCount,
            'wordCount':myuser.wordCount

        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'search':

            user = users.get_current_user()

            searchText = (self.request.get('word')).lower()
            if searchText == "":

                template_values={
                    'user':user,
                    'message': 'Word not found, please try entering different word',
                    'anagrmEngine': model.query().fetch()
                    }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))
            else:

                wordLexi = list(searchText.lower())
                anaSort = sorted(wordLexi)
                searchWord = ''.join(anaSort)

                anagramEnginekey = ndb.Key("model",user.email()+searchWord)
                anagrmEngine = anagramEnginekey.get()

                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()
                template_values={
                    'anagrmEngine':anagrmEngine,
                    'user':user,
                    'anaCount':myuser.anaCount,
                    'wordCount':myuser.wordCount

                    }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add', Add),
    ('/upload', upload),
    ('/subAnag',sub)
], debug=True)
