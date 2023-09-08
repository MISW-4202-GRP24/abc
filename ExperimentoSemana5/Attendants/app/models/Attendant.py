from datetime import datetime
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from .Language import LanguageSchema
from .Base import db


class Attendant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    age = db.Column(db.Numeric)
    phone = db.Column(db.String(24))
    email = db.Column(db.String(254))
    country = db.Column(db.String(50))
    languages = db.relationship("Language", cascade="all, delete, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AttendantSchema(SQLAlchemySchema):
    class Meta:
        model = Attendant
        include_relationships = True
        load_instance = True

    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    age = fields.Integer()
    phone = fields.String()
    email = fields.String()
    country = fields.String()
    languages = fields.List(fields.Nested(LanguageSchema()))
    created_at = fields.DateTime()
