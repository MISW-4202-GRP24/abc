import json
import time
import requests
import concurrent.futures
from flask import Flask, jsonify
from celery import Celery
from datetime import datetime

app = Flask(__name__)

celery_app = Celery(__name__, broker="redis://localhost:6379/0")


@celery_app.task(name="register_log")
def register_log(*args):
    pass


# Cargar la configuración desde el archivo config.json
config_file = "config.json"
with open(config_file, "r") as config:
    config_data = json.load(config)

# Endpoint para enviar las registros
URL = config_data["ATTENDANCE_URL"]


def post_requests():
    with open("candidates.json", "r") as candidates:
        registers = json.load(candidates)

    def send_request(register):
        sent = datetime.utcnow()
        start = time.time()
        response = requests.post(URL, json=register)
        end = time.time()
        elapsed = (end - start) * 1000
        args = (
            "{} {}".format(register["first_name"], register["last_name"]),
            sent,
            elapsed,
            response.status_code,
        )
        register_log.apply_async(args=args, queue="logs")
        return response

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_request, register) for register in registers]
        for future in concurrent.futures.as_completed(futures):
            future.result()


post_requests()
