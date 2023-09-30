from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask
from views import AttendantView, LoginView, AttendantViewRaw

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "frase-secreta"

app_context = app.app_context()
app_context.push()
api = Api(app)
api.init_app(app)

api.add_resource(LoginView, "/login")
api.add_resource(AttendantView, "/attendant")
api.add_resource(AttendantViewRaw, "/attendantraw")

jwt = JWTManager(app)
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["id"]

@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    return jwt_data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

