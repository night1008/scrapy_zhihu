# coding: utf-8
import math
from flask import Flask
from flask import json, jsonify, abort, request, flash, session, g
from flask import render_template

from sqlalchemy import func

from models import Answer, Session, Question, Collection, CollectionAnswer, Author
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    DEBUG=True,
))

LIMIT = 10

def get_session():
    if not hasattr(g, 'session'):
        g.session = Session()
    return g.session


@app.teardown_appcontext
def close_session(error):
    if hasattr(g, 'session'):
        g.session.close()


# @app.cli.command('test_app_command')
# def test_app_command():
#     """Initializes the database."""
#     print 'Test App Command'


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

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/task", methods=['GET', 'POST'])
def task():
    if request.method == 'GET':
        return render_template('task.html')

    url = request.form.get('url')
    
    return render_template('task.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form.get('email')
    password = request.form.get('password')
  
    return render_template("login.html")

@app.route("/answer")
def answer():
    # @todo: 换页检测
    page = request.args.get('page', 1, int)
    session = get_session()
    offset = (page - 1) * LIMIT
    answers_query = session.query(Answer.id,
                                Answer.question_id,
                                Answer.user_token,
                                Answer.vote_up,
                                Answer.summary,
                                Question.title.label('question_title')
                            ).filter(Answer.question_id == Question.id) \
                            .order_by(Answer.vote_up.desc())

    answers = answers_query.offset(offset).limit(LIMIT)
    pagination = get_pagination(answers_query.count(), LIMIT, page)

    flash('New entry was successfully posted')

    return render_template('answer/index.html', answers=answers, pagination=pagination)


@app.route("/answer/<answer_id>")
def answer_detail(answer_id):
    session = get_session()
    answer = session.query(Answer.id,
                        Answer.vote_up,
                        Answer.content,
                        Answer.question_id,
                        Question.title.label('question_title')
                        ).filter(Answer.question_id == Question.id) \
                        .filter_by(id=answer_id).first()
    if not answer:
        abort(404)
    return render_template('answer/detail.html', answer=answer)


@app.route("/question")
def question():
    page = request.args.get('page', 1, int)
    session = get_session()
    offset = (page - 1) * LIMIT
    
    questions_query = session.query(Question.id,
                                Question.title,
                                Question.content,
                            ) \
                            .order_by(Question.answer_count.desc())
                            # ).filter(Answer.question_id == Question.id) \
                            

    questions = questions_query.offset(offset).limit(LIMIT)
    
    pagination = get_pagination(questions_query.count(), LIMIT, page)

    return render_template('question/index.html', questions=questions, pagination=pagination)


@app.route("/question/<question_id>")
def question_detail(question_id):
    page = request.args.get('page', 1, int)
    session = get_session()
    offset = (page - 1) * LIMIT
    
    question = session.query(Question.id,
                                Question.title,
                                Question.content,
                            ) \
                            .filter_by(id=question_id).first()
                            
    if not question:
        abort(404)

    answers_query = session.query(Answer.id,
                                Answer.question_id,
                                Answer.user_token,
                                Answer.vote_up,
                                Answer.summary,
                            ).filter(Answer.question_id == question_id) \
                            .order_by(Answer.vote_up.desc())
    
    answers = answers_query.offset(offset).limit(LIMIT)

    pagination = get_pagination(answers_query.count(), LIMIT, page)

    return render_template('question/detail.html', question=question, answers=answers, pagination=pagination)


@app.route("/collection")
def collection():
    page = request.args.get('page', 1, int)
    session = get_session()
    offset = (page - 1) * LIMIT
    
    collections_query = session.query(Collection) \
                            .order_by(Collection.review_count.desc())

    collections = collections_query.offset(offset).limit(LIMIT)
    
    pagination = get_pagination(collections_query.count(), LIMIT, page)

    return render_template('collection/index.html', collections=collections, pagination=pagination)


@app.route('/collection/<collection_id>')
def collection_detail(collection_id):
    """
    SELECT a.id, a.user_token,a.question_id, a.vote_up, a.summary,
    a.review_count, a.published_at,a.edited_at,q.title AS question_title
    FROM answer as a, question as q WHERE a.question_id = q.id AND a.id IN
    (SELECT answer_id FROM collection_answer WHERE collection_id = '25185328');
    """
    page = request.args.get('page', 1, int)
    session = get_session()
    offset = (page - 1) * LIMIT

    collection = session.query(Collection) \
                            .filter_by(id=collection_id).first()
                            
    if not collection:
        abort(404)
    
    collection_answers_query = session.query(CollectionAnswer) \
                                        .filter_by(collection_id=collection_id)
    
    collection_answers = collection_answers_query.offset(offset).limit(LIMIT)

    answers = []
    for collection_answer in collection_answers:
        answer = session.query(Answer.id,
                        Answer.user_token,
                        Answer.vote_up,
                        Answer.summary,
                        Answer.question_id,
                        Question.title.label('question_title')
                        ).filter(Answer.question_id == Question.id) \
                        .filter_by(id=collection_answer.answer_id).first()
        if answer:
            answers.append(answer)

    pagination = get_pagination(collection_answers_query.count(), LIMIT, page)

    return render_template('collection/detail.html', collection=collection, answers=answers, pagination=pagination)


@app.route("/author")
def author():
    page = request.args.get('page', 1, int)
    session = get_session()
    offset = (page - 1) * LIMIT
    
    authors_query = session.query(Author) \
                            .order_by(Author.id.desc())

    authors = authors_query.offset(offset).limit(LIMIT)
    
    pagination = get_pagination(authors_query.count(), LIMIT, page)

    return render_template('author/index.html', authors=authors, pagination=pagination)


@app.route("/author/<author_token>")
def author_detail():
    return 'author detail'

@app.route("/invoke")
def invoke():
    return 'invoke'

