# coding: utf-8
from flask import Flask
from flask import json, jsonify, abort, request
from flask import render_template

from sqlalchemy import func

import zhihu
from zhihu.models import Answer, Session, Question, Collection
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = Flask(__name__)
app.debug = True
LIMIT = 10

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/answer")
def answer():
    page = request.args.get('page', 1)
    session = Session()
    # answer = session.query(Answer).first()
    offset = (page - 1 ) * LIMIT
    answers_query = session.query(Answer.id,
                                Answer.vote_up,
                                func.left(Answer.content, 200).label('summary')
                            ).order_by(Answer.vote_up.desc())
    answers = answers_query.offset(offset).limit(LIMIT)

    pagination = {
        'total': answers_query.count(),
        'current_page': page,
        'limit': LIMIT,
    }

    return render_template('answer/index.html', answers=answers, pagination=pagination)

@app.route("/answer/<answer_id>")
def answer_detail(answer_id):
    session = Session()
    # answer = session.query(Answer).first()
    answer = session.query(Answer).filter_by(id=answer_id).first()
    if not answer:
        abort(404)
    return render_template('answer/detail.html', answer=answer)

# return jsonify(result)

@app.route("/question")
def question():
    session = Session()
    # answer = session.query(Answer).first()
    questions = session.query(Question).order_by(Question.created_at).all()
    return render_template('question/index.html', questions=questions)

@app.route("/collection")
def collection():
    session = Session()
    # answer = session.query(Answer).first()
    collections = session.query(Collection).order_by(Collection.created_at).all()
    return render_template('collection.html', collections=collections)

@app.route('/collection/<collection_id>/answer')
def collection_answer(collection_id):
    """
    SELECT a.id, a.user_token,a.question_id, a.vote_up,left(a.content, 100) as summary,
    a.review_count, a.published_at,a.edited_at,q.title AS question_title
    FROM answer as a, question as q WHERE a.question_id = q.id AND a.id IN
    (SELECT answer_id FROM collection_answer WHERE collection_id = '25185328');
    """
    session = Session()
    # answer = session.query(Answer).first()
    answers = session.query(Collection).order_by(Collection.created_at).all()
    return render_template('question.html', answers=answers)

@app.route("/invoke")
def invoke():
    return 'invoke'


if __name__ == "__main__":
    app.run()
