from datetime import datetime
import random
from faker import Faker
from flask import jsonify, request
from flask_restful import Resource

from .Base import attendant_schema
from models import db

fake = Faker()


class AttendantView(Resource):
    error_frequency = 7

    def post(self):
        try:
            if random.randint(1, self.error_frequency) == 1:
                raise Exception(fake.sentence())
            data = request.get_json()
            attendant = attendant_schema.load(data, transient=True)
            db.session.add(attendant)
            db.session.commit()
            return attendant_schema.dump(attendant), 200
        except Exception as e:
            db.session.rollback()
            return {
                "error": e.args[0],
                "current_timestamp": datetime.utcnow().isoformat(),
            }, 500
