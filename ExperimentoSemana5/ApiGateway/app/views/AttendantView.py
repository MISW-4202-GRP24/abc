from datetime import datetime
import json
import time
import os
import random
import requests
from flask_restful import Resource
from flask import request
from celery import Celery

redis_endpoint = os.environ.get("REDIS_ENDPOINT", "redis://localhost:6379/0")
celery_app = Celery(__name__, broker=redis_endpoint)


@celery_app.task(name="register_apigateway_log")
def register_apigateway_log(*args):
    pass


class AttendantView(Resource):
    def post(self):
        endpoints = os.environ.get("ENDPOINTS", "http://127.0.0.1:6000").split(",")
        url = "{}/attendant".format(random.choice(endpoints))
        response = self.send_and_log_request(url)
        return response.json(), response.status_code

    def send_and_log_request(self, url):
        start = time.time()
        response = requests.post(
            url,
            data=request.data,
            headers=request.headers,
        )
        end = time.time()
        response_headers = dict(response.headers)
        elapsed = (end - start) * 1000

        args = (
            datetime.utcnow(),
            request.method,
            request.path,
            response.status_code,
            elapsed,
            response_headers.get("Server-IP"),
            response_headers.get("Server-Name"),
        )
        register_apigateway_log.apply_async(args=args, queue="logs")

        return response
