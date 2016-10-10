# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import math
import re
from flask import Flask
from flask import json, jsonify, abort, request, flash, session, g
from flask import render_template, redirect, url_for
from flask.ext.login import LoginManager, AnonymousUserMixin, \
    login_user, login_required, current_user, logout_user

from pony.orm import db_session, select, commit, desc

from models.pony_models import db, Answer, User, Question, \
    Collection, CollectionAnswer, Author
from forms import LoginForm, SignupForm, UserSchedulerForm

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from config.web_config import DB

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    DEBUG=True,
))

login_manager = LoginManager()
login_manager.init_app(app)
LIMIT = 10

@login_manager.user_loader
@db_session
def load_user(user_id):    
    if user_id:
        user = User.get(id=user_id)
    else:
        user = AnonymousUserMixin()
    return user

@db_session
def validate_user(email, next_url=None):
    user = select(u for u in User if u.email == email).first()
    if user:
        login_user(user)
        flash('登录成功', 'success')
        return redirect(next_url or url_for('index'))
    else:
        flash('登录失败', 'danger')
        return redirect(url_for('login'))


LIMIT = 10
db.bind('mysql', **DB)
db.generate_mapping()

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

def get_scheduler_type(url):
    """
    根据传入的url解析得到任务类型
    """
    m = re.match('^https?://www.zhihu.com/question/\d{8,}/answer/\d{8,}$', url)
    if m:
        return 'answer'

    m = re.match('^https?://www.zhihu.com/question/\d{8,}$', url)
    if m:
        return 'question'

    m = re.match('^https?://www.zhihu.com/collection/\d{8,}$', url)
    if m:
        return 'collection'

    m = re.match('^https?://www.zhihu.com/people/(.+)$', url)
    if m:
        return 'author'


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/test")
def test():
    print current_user.is_authenticated()
    return 'test'

@app.route("/")
@db_session
def index():
    return render_template('index.html')

# @app.route("/task", methods=['GET', 'POST'])
# def task():
#     user_scheduler_form = UserSchedulerForm(request.form)
#     context = {
#         'form': user_scheduler_form,
#     }

#     if request.method == 'GET':
#         return render_template('task.html', **context)

#     url = request.form.get('url', None)

#     if url:
#         url = url.strip()
#         type = get_scheduler_type(url)
#     else:
#         pass

#     return render_template('task.html', **context)

@app.route('/signup', methods=['GET', 'POST'])
@db_session
def signup():
    signup_form = SignupForm()
    context = {
        'form': signup_form,
    }

    if request.method == 'GET':
        return render_template("signup.html", **context)
   
    if signup_form.validate_on_submit():
        email = signup_form.email.data.strip()
        password = signup_form.password.data.strip()
        password_hash = User.set_password(password)
        user = User(email=email, password=password_hash)
        commit()
        flash('注册成功', 'success')  
        return redirect(url_for('index'))

    return render_template("signup.html", **context)

@app.route("/login", methods=['GET', 'POST'])
@db_session
def login():
    login_form = LoginForm(request.form)
    context = {
        'form': login_form,
        'next': request.args.get('next'),
    }

    if request.method == 'GET':
        return render_template("login.html", **context)

    email = request.form.get('email')
    password = request.form.get('password')
    if login_form.validate_on_submit():
        return validate_user(email=login_form.email.data.strip(),
                            next_url=request.args.get('next'))

    return render_template("login.html", **context)


@app.route('/logout')
@login_required
@db_session
def logout():
    logout_user()
    flash('退出成功', 'success')
    return redirect(url_for("index"))


@app.route("/answer")
@db_session
def answer():
    page = request.args.get('page', 1, int)
    
    answers_query = select(a for a in Answer).order_by(desc(Answer.vote_up))
    answers = answers_query.page(page, pagesize=LIMIT)

    pagination = get_pagination(answers_query.count(), LIMIT, page)

    return render_template('answer/index.html', answers=answers, pagination=pagination)


@app.route("/answer/<answer_id>")
@db_session
def answer_detail(answer_id):
    answer = Answer.get(id=answer_id)
    if not answer:
        abort(404)

    flash('New entry was successfully posted', 'success')

    return render_template('answer/detail.html', answer=answer)

@app.route("/question")
@db_session
def question():
    page = request.args.get('page', 1, int)
    
    questions_query = select(a for a in Question).order_by(desc(Question.answer_count))
    questions = questions_query.page(page, pagesize=LIMIT)

    pagination = get_pagination(questions_query.count(), LIMIT, page)

    return render_template('question/index.html', questions=questions, pagination=pagination)


@app.route("/question/<question_id>")
@db_session
def question_detail(question_id):
    question = Question.get(id=question_id)
    if not question:
        abort(404)

    answers_query = select(a for a in Answer if a.question_id == question_id).order_by(desc(Answer.vote_up))
    answers = answers_query.page(page, pagesize=LIMIT)

    pagination = get_pagination(answers_query.count(), LIMIT, page)

    return render_template('question/detail.html', question=question, answers=answers, pagination=pagination)


@app.route("/collection")
@db_session
def collection():
    page = request.args.get('page', 1, int)

    collections_query = select(c for c in Collection).order_by(desc(Collection.review_count))

    collections = collections_query.page(page, pagesize=LIMIT)

    pagination = get_pagination(collections_query.count(), LIMIT, page)

    return render_template('collection/index.html', collections=collections, pagination=pagination)


@app.route('/collection/<collection_id>')
@db_session
def collection_detail(collection_id):
    page = request.args.get('page', 1, int)

    collection = Collection.get(id=collection_id)
                            
    if not collection:
        abort(404)
    
    collection_answers_query = select(cs for cs in CollectionAnswer if cs.collection_id == collection_id)
    
    collection_answers = collection_answers_query.page(page, pagesize=LIMIT)

    answer_ids = [ca.answer_id for ca in collection_answers]
    answers = select(a for a in Answer if a.id in answer_ids)[:]

    pagination = get_pagination(collection_answers_query.count(), LIMIT, page)

    return render_template('collection/detail.html', collection=collection, answers=answers, pagination=pagination)


@app.route("/author")
@db_session
def author():
    page = request.args.get('page', 1, int)
    
    authors_query = select(a for a in Author).order_by(desc(Author.id))
    
    authors = authors_query.page(page, pagesize=LIMIT)

    pagination = get_pagination(authors_query.count(), LIMIT, page)

    return render_template('author/index.html', authors=authors, pagination=pagination)


@app.route("/author/<token>")
@db_session
def author_detail(token):
    author = Author.get(token=token)
    if not author:
        abort(404)

    return render_template('author/detail.html', author=author)
