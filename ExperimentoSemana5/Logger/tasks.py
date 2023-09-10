from celery import Celery

celery = Celery(__name__, broker="redis://localhost:6379/0")


@celery.task(name="register_log")
def register_log(candidate, date, elapsed, status_code):
    with open("log_sender_requests.txt", "a+") as file:
        file.write("{}\t{}\t{}\t{}\n".format(date, elapsed, candidate, status_code))
