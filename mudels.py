import pyrebase as pb
from datetime import datetime

Config = {
    'apiKey': "AIzaSyDqJIXnDJ9gMT4k8bDdSkJJTk7PEDRHlUI",
    'authDomain': "muslimbook-38f85.firebaseapp.com",
    'databaseURL': "https://muslimbook-38f85.firebaseio.com",
    'projectId': "muslimbook-38f85",
    'storageBucket': "muslimbook-38f85.appspot.com",
    'messagingSenderId': "847402124105",
    'appId': "1:847402124105:web:b858c01727c15313891098",
    'measurementId': "G-G8CFSF8G9H"
}
firebase = pb.initialize_app(Config)
db = firebase.database()
current_user = None
print(str(datetime.utcnow()).replace(' ','_'))



def creatAccount( username, email, password, image_file='defult.png'):
    if type(username) == str and type(email) == str and type(password) == str and type(image_file) == str:
        check = db.child('ueres').child(username).get()
        if not check.val():
            db.child('ueres').child(username).set({'email': email, 'password': password, 'image_file': image_file})
            print('user created!')
            '''
            لازم نضيف شرط اذا اليوزر نيم موجد والايميل
            '''


def logIn(username, password):
    global current_user
    if type(username) == str and type(password) == str:
        check = db.child('ueres').child(username).get()
        if check.key() == username and dict(check.val())['password'] == password:
            current_user = user(check.key(), dict(check.val()))


class user:

    def __init__(self, username, kwargs):
        self.username = username
        self.email = kwargs['email']
        self.password = kwargs['password']
        self.image_file = kwargs['image_file'] if kwargs['image_file'] else 'default.jpg'

    def logOut(self):
        global current_user
        if current_user:
            current_user = None

    def creatPost(self, content, image=None, video=None):
        post = {'auther':self.username,'time': repr(datetime.utcnow()).split('.')[1]}#في مشكلة فالتاريخ بحلها بعدين
        if content:
            post['content'] = content
        if image and not video:
            post['image'] = image
        if video and not image:
            post['video'] = video
        db.child('ueres').child(self.username).child('postes').child(self.username+str(datetime.utcnow()).replace(' ','').replace('-','').replace(':','').replace('.','')).set(post)

    def updatePost(self,  id, content=None, image=None, video=None):
        theNewPost = {}
        if content:
            theNewPost['content'] = content
        if image and not video:
            theNewPost['image'] = image
        if video and not image:
            theNewPost['video'] = video
        if len(theNewPost) > 0:
            db.child('ueres').child(self.username).child(id).update(theNewPost)

    def deletePost(self, id):
        if db.child('ueres').child(self.username).child(id).get().val():
            db.child('ueres').child(self.username).child(id).remove()


class post():
    def __init__(self,ather,postId):
        self.postAuther=ather
        self.postId=postId
        self.content=db.child('ueres').child(self.postAuther).child('content').get().val()
        self.dateTime=eval(db.child('ueres').child(self.postAuther).child('time').get().val())
    def like(self,liker):
        '''
        لازم اسويها بعدين
        '''
        pass
    def comment(self,auther,content):
        '''
        لازم اسويها بعدين
        '''
        pass

creatAccount('ahmad','alkoran1234@gmail.com','123456')
logIn('ahmad','123456')
current_user.creatPost('first post')
