# coding: utf-8
import math
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

def get_pagination(total, limit, current_page):
    last_page = int(math.ceil(total / limit))
    page_range = []

    if last_page > 1:
        for i in range(max(current_page - 2, 2), min(max(current_page - 2, 2) + 3, last_page + 1)):
            page_range.append(i)

    return {
        'total': total,
        'current_page': current_page,
        'limit': limit,
        'last_page': last_page,
        'has_prev_page': current_page > 1,
        'has_next_page': current_page + 1 <= last_page,
        'page_range': page_range,
    }

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/answer")
def answer():
    # @todo: 换页检测
    page = request.args.get('page', 1, int)
    session = Session()
    offset = (page - 1) * LIMIT
    print '=============>'
    print offset
    answers_query = session.query(Answer.id,
                                Answer.question_id,
                                Answer.vote_up,
                                Answer.summary,
                                Question.title
                            ).filter(Answer.question_id == Question.id) \
                            .order_by(Answer.vote_up.desc())

    answers = answers_query.offset(offset).limit(LIMIT)
    print answers_query.count()
    print answers.count()
    print answers[0]
    pagination = get_pagination(answers_query.count(), LIMIT, page)

    return render_template('answer/index.html', answers=answers, pagination=pagination)

@app.route("/answer/<answer_id>")
def answer_detail(answer_id):
    session = Session()
    # answer = session.query(Answer).first()
    answer = session.query(Answer.id,
                        Answer.vote_up,
                        Answer.content,
                        Answer.question_id,
                         Question.title
                        ).filter(Answer.question_id == Question.id) \
                        .filter_by(id=answer_id).first()
    print answer.id
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
