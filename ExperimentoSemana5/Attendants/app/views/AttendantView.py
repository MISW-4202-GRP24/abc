from datetime import datetime
import random
import socket
from faker import Faker
from flask import make_response, request
from flask_restful import Resource

from .Base import attendant_schema
from models import db

fake = Faker()


class AttendantView(Resource):
    error_frequency = 7

    def post(self):
        server_ip = socket.gethostbyname(socket.gethostname())
        server_name = socket.gethostname()
        try:
            if random.randint(1, self.error_frequency) == 1:
                raise Exception(fake.sentence())
            data = request.get_json()
            attendant = attendant_schema.load(data, transient=True)
            db.session.add(attendant)
            db.session.commit()
            resp = make_response(attendant_schema.dump(attendant), 200)
            resp.headers.extend({"Server-IP": server_ip})
            resp.headers.extend({"Server-Name": server_name})
            return resp
        except Exception as e:
            db.session.rollback()
            return {
                "error": e.args[0],
                "current_timestamp": datetime.utcnow().isoformat(),
            }, 500
