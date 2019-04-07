import webapp2;
import os;
import jinja2;
import random;
from google.appengine.ext import ndb;
from google.appengine.api import users
from model import model
from myuser import MyUser
from itertools import combinations

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)



def wordSort(word):
    listWord = list(word)
    subWordKey = []
    for i in range(3,len(word)+1):
        temp=(["".join(c)for c in combinations(word,i)])
        for c in temp:
            subWordKey.append(c)
    return subWordKey

class sub(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # message = "Welcome to sub anagram search page"
        result =[]
        template_values = {
        # 'message':message,
        'subAnag':result
        }
        template = JINJA_ENVIRONMENT.get_template('subAnag.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser',user.user_id())
        myuser = myuser_key.get()

        result =[]

        action = self.request.get('button')
        if action == 'search':
            word = self.request.get('word')

            if word=="":
                self.redirect('/subAnag')
            else:
                # lexi_word = lexi(word)
                wordLexi = list(word.lower())
                anaSort = sorted(wordLexi)
                subWord = ''.join(anaSort)

                subAn = wordSort(subWord)
                for subK in subAn:
                    subKey = ndb.Key('model',user.email()+subK)
                    word = subKey.get()

                    if word == None:
                        continue
                    else:
                        result.extend(word.wordList)
                template_values = {
                'subAnag':result,
                'message':"Displaying sub anagrams"
                }
                template = JINJA_ENVIRONMENT.get_template('subAnag.html')
                self.response.write(template.render(template_values))
        else:
            self.redirect('/subAnag')
