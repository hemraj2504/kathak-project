
from app import app,db
from flask import jsonify, request
import json
from app.models import User
from app.qa_model import get_answer
from newspaper import Article

@app.route('/')
def index():
    return jsonify({'response':'hello world'})

def process_url(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

@app.route('/question_answer', methods=['POST','GET'])
def do_qa():
    if (request.method == 'POST'):
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        question = request_data['question']
        current_text = request_data['text']
        if (current_text[:4] == 'http'):
            current_text = process_url(current_text)
        # userid = request_data['user_id']
        # _text = Text.query.filter_by(id=current_text,user_id=userid).first()
        answer = get_answer(current_text,question)
        print (answer['answer'])
        print (answer['score'])
        if (answer['score'] < 0.01):
            return "Could'nt find the answer. Please Try again."
        else:
            return answer['answer']

@app.route('/login', methods=['POST','GET'])
def login():
    if (request.method == 'POST'):
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        uname = request_data['username']
        passwd = request_data['password']
        _user = User.query.filter_by(username=uname).first()
        if (_user):
            if (_user.username and _user.password == passwd):
                print ("Yes it is validated: ")
                return jsonify(_user.serialize)
            else:
                return "404"
        else:
            return "404"

@app.route('/register',methods=['POST','GET'])
def register():
    print ("is there")
    if (request.method == 'POST'):
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        email = request_data['email']
        uname = request_data['username']
        passwd = request_data['password']
        _user = User.query.filter_by(username=uname).first()
        if (_user):
            return "404"
        else:
            newuser = User(email,uname,passwd)
            db.session.add(newuser)
            db.session.commit()
            return str(newuser.id)