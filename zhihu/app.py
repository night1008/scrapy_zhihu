# coding: utf-8
from flask import Flask
from flask import json, jsonify
from flask import render_template

import zhihu
from zhihu.models import Answer, Session, Question
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/answer")
def answer():
	session = Session()
	# answer = session.query(Answer).first()
	answers = session.query(Answer).order_by(Answer.created_at).all()
	return render_template('answer.html', answers=answers)
	# return jsonify(result)

@app.route("/question")
def question():
	session = Session()
	# answer = session.query(Answer).first()
	questions = session.query(Question).order_by(Question.created_at).all()
	return render_template('question.html', questions=questions)

@app.route("/invoke")
def invoke():
	return 'aaa'

if __name__ == "__main__":
    app.run()