
from app import app
from flask import jsonify, request
import json
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