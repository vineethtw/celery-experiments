from celery import Celery

app = Celery('tasks', broker='amqp://guest@localhost//', backend='db+postgresql://paa_db_user:password@localhost/postgres', include="tasks")

