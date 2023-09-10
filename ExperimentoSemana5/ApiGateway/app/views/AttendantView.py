from datetime import datetime
import json
import time
import os
import random
import requests
from flask_restful import Resource
from flask import request


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
        print(
            f'{datetime.utcnow()}\t{request.method}\t{request.path}\t{response.status_code}\t{elapsed:.2f}\t{response_headers.get("Server-IP")}\t{response_headers.get("Server-Name")}'
        )
        ## aquí el guardado del log
        return response
