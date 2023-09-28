from datetime import datetime, timedelta
import time
import os
import random
from redis import Redis
from flask_jwt_extended import current_user
import requests
from flask_restful import Resource
from flask import request
from celery import Celery

from jwt_api_gateway import JWTUtils


redis_endpoint = os.environ.get("REDIS_ENDPOINT", "redis://localhost:6379/0")
celery_app = Celery(__name__, broker=redis_endpoint)
redis_default = Redis.from_url(url=redis_endpoint)
limit = int(os.environ.get("LIMIT", "10"))
period = timedelta(seconds=int(os.environ.get("PERIOD", "60")))


@celery_app.task(name="register_apigateway_log")
def register_apigateway_log(*args):
    pass

def user_is_blocked():
    ## aqui leer si el current user está en la lista negra
    return current_user["sub"] 

def request_is_limited(
    red: Redis, redis_key: str, redis_limit: int, redis_period: timedelta
):
    if red.setnx(redis_key, redis_limit):
        red.expire(redis_key, int(redis_period.total_seconds()))
    bucket_val = red.get(redis_key)
    if bucket_val and int(bucket_val) > 0:
        red.decrby(redis_key, 1)
        return False
    ## aqui guardar en la lista negra
    return True


class AttendantView(Resource):
    @JWTUtils.rol_required("admin")
    def post(self):
        if user_is_blocked() or request_is_limited(
            redis_default, "{}".format(current_user["sub"]), limit, period
        ):
            return "Too many requests, please try again later.", 429
        return "ok"

    def send_request(self):
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
