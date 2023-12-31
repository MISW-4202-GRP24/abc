from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine
from views import AttendantView
from models import db

import os

db_conn = os.environ.get("DB_CONN", "postgresql://postgres:postgres@127.0.0.1:15432/abc")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_conn
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

app_context = app.app_context()
app_context.push()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db.session.configure(bind=engine)
db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(AttendantView, "/attendant")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
