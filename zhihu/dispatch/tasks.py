from celery import Celery
celery_app = Celery()
celery_app.config_from_object('celeryconfig')

@celery_app.task
def add(x, y):
    return x + y

@celery_app.task
def mul(x, y):
    return x * y


@celery_app.task
def xsum(numbers):
    return sum(numbers)

# from __future__ import absolute_import
# from celery import Celery
# import time

# app = Celery('tasks', backend="amqp", broker='amqp://guest@localhost')
# app = Celery('tasks', backend="redis://localhost:6379/0", broker='amqp://guest@localhost')

# @app.task
# def add(x, y):
#     print 'hello celery'
#     time.sleep(10)
#     return x + y

# @app.task
# def mul(x, y):
#     return x * y


# @app.task
# def xsum(numbers):
#     return sum(numbers)