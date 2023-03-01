# from flask_login import current_user
# from sqlalchemy import null
from app import app
from flask import jsonify, request
import json
# from app.models import User, Text
from app.qa_model import get_answer

@app.route('/')
def index():
    return jsonify({'response':'hello world'})

# @app.route('/login', methods=['POST','GET'])
# def login():
#     if (request.method == 'POST'):
#         request_data = request.data
#         request_data = json.loads(request_data.decode('utf-8'))
#         uname = request_data['username']
#         passwd = request_data['password']
#         _user = User.query.filter_by(username=uname).first()
#         if (_user):
#             if (_user.username and _user.password == passwd):
#                 print ("Yes it is validated: ")
#                 return jsonify(_user.serialize)
#             else:
#                 return "404"
#         else:
#             return "404"

# @app.route('/register',methods=['POST','GET'])
# def register():
#     print ("is there")
#     if (request.method == 'POST'):
#         request_data = request.data
#         request_data = json.loads(request_data.decode('utf-8'))
#         fname = request_data['fullname']
#         uname = request_data['username']
#         passwd = request_data['password']
#         _user = User.query.filter_by(username=uname).first()
#         if (_user):
#             return "404"
#         else:
#             newuser = User(fname,uname,passwd)
#             db.session.add(newuser)
#             db.session.commit()
#             return str(newuser.id)

# @app.route('/get_data', methods=['POST','GET'])
# def get_data():
#     if (request.method=='POST'):
#         request_data = request.data
#         request_data = json.loads(request_data.decode('utf-8'))
#         userid = request_data['user_id']
#         all_texts = jsonify(json_list= [i.serialize for i in Text.query.filter_by(user_id=userid)])
#         print (all_texts)
#         return all_texts

# @app.route('/add_data', methods=['POST','GET'])
# def add_data():
#     if (request.method == 'POST'):
#         request_data = request.data
#         request_data = json.loads(request_data.decode('utf-8'))
#         atitle = request_data['title']
#         content = request_data['content']
#         date = request_data['date']
#         userid = request_data['user_id']
#         _text = Text.query.filter_by(title=atitle, user_id=userid).first()
#         if (_text):
#             _text.content = content
#             db.session.commit()
#             return str(_text.id)
#         else:
#             text = Text(title=atitle,content=content,date=date,user_id=userid)
#             db.session.add(text)
#             db.session.commit()
#             return str(text.id)

# @app.route('/delete_data',methods=['POST','GET'])
# def del_data():
#     if (request.method=='POST'):
#         request_data = request.data
#         request_data = json.loads(request_data.decode('utf-8'))
#         textid = request_data['text_id']
#         userid = request_data['user_id']
#         _text = Text.query.filter_by(id=textid, user_id=userid).first()
#         if (_text):
#             db.session.delete(_text)
#             db.session.commit()
#             return (str(_text.id))
#         else:
#             return "404"

@app.route('/question_answer', methods=['POST','GET'])
def do_qa():
    if (request.method == 'POST'):
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        question = request_data['question']
        current_text = request_data['text']
        # userid = request_data['user_id']
        # _text = Text.query.filter_by(id=current_text,user_id=userid).first()
        answer = get_answer(current_text,question)
        print (answer['answer'])
        print (answer['score'])
        if (answer['score'] < 0.01):
            return "Could'nt find the answer. Please Try again."
        else:
            return answer['answer']