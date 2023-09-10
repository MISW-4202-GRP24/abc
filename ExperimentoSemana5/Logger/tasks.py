from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task(name="register_log")
def register_log(user, date, status_code):
    with open('log_sender_requests.txt','a') as file:
        file.write('{} - Request sent:{}\n'.format(user, date, status_code))