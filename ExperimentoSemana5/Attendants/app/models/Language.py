from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema
from .Base import db


class Language(db.Model):
    attendant_id = db.Column(db.Integer, db.ForeignKey("attendant.id"))
    name = db.Column(db.String)

    __table_args__ = (db.PrimaryKeyConstraint(attendant_id, name),)


class LanguageSchema(SQLAlchemySchema):
    class Meta:
        model = Language
        include_relationships = True
        load_instance = True
        transient = True

    name = fields.String()
