from flask_restful import Api
from flask import Flask
from views import AttendantView

app = Flask(__name__)

app_context = app.app_context()
app_context.push()
api = Api(app)
api.init_app(app)

api.add_resource(AttendantView, "/attendant")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
