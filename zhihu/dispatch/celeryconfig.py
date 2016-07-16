# coding: utf-8
CELERY_ACKS_LATE = True
CELERY_ENABLE_UTC = True
BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
# CELERY_TASK_RESULT_EXPIRES = 300

CELERY_QUEUES = (
   
)

CELERY_ROUTES = {
    'tasks.add': 'low-priority',
}

CELERY_IMPORTS = (
   'tasks',        
)

CELERYBEAT_SCHEDULE = {
   
}

CELERY_SEND_TASK_ERROR_EMAILS = False
ADMINS = (
    
)
