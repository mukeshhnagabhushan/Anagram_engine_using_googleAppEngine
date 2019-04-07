import webapp2;
import os;
import jinja2;
import random;
from google.appengine.ext import ndb;
from google.appengine.api import users
from myuser import MyUser
from model import model
import re

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

class upload(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        Message = ''
        template_values ={
        'message':Message
        }
        template = JINJA_ENVIRONMENT.get_template('upload.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        fileUpload = self.request.get('file')
        action = self.request.get('button')
        user = users.get_current_user()
        # def lexicography(word):
        #     anaList = list(word.lower())
        #     sorted_list = sorted(anaList)
        #     return ''.join(sorted_list)

        if action=='Upload':
            openf= open(fileUpload)
            readFile = openf.readline()
            while readFile:
                Word=(readFile.strip('\n\r')).lower()
                # readText = self.request.get(Word)
                wordLexi = list(Word.lower())
                anaSort = sorted(wordLexi)
                addWord = ''.join(anaSort)
                anagramEnginekey = ndb.Key('model',user.email()+addWord)
                anagram = anagramEnginekey.get()
                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()

                if anagram == None :
                    addAnagram = model(id=user.email()+addWord,anagramK=addWord)
                    addAnagram.User=user.email()
                    addAnagram.wordList.append(Word)
                    addAnagram.wCount = 1
                    addAnagram.lCount =  len(Word)
                    addAnagram.put()

                    wordCount = myuser.wordCount+1
                    anaCount = myuser.anaCount+1
                    myuser = MyUser(id=user.user_id(),username=user.email(),anaCount=anaCount,wordCount=wordCount)
                    myuser.put()
                    message = 'File uploaded successfully'
                else:
                    flag = False
                    for word in anagram.wordList:
                        if word == Word:
                            flag = True
                            break
                        else:
                            flag = False

                    if flag:
                        message = 'Word already exists'
                    else:
                        # anagram.User=user.email()
                        anagram.wordList.append(Word)
                        anagram.wCount = anagram.wCount + 1
                        anagram.put()
                        wordCount = myuser.wordCount+1
                        anaCount = myuser.anaCount
                        myuser = MyUser(id=user.user_id(),username=user.email(),anaCount=anaCount,wordCount=wordCount)
                        myuser.put()


                readFile = openf.readline()
            openf.close()

        template_values ={
            'message': message


            }
        template = JINJA_ENVIRONMENT.get_template('upload.html')
        self.response.write(template.render(template_values))


