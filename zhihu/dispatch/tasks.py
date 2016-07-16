# from celery import Celery
# celery_app = Celery()
# celery_app.config_from_object('celeryconfig')

from __future__ import absolute_import
from celery import Celery
import time

app = Celery('tasks', broker="redis://localhost:6379/0", 
	backend='redis://localhost:6379/1')

@app.task
def add(x, y):
    print 'hello celery'
    time.sleep(10)
    return x + y

@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)