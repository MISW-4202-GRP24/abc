import hashlib
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from sqlalchemy.orm import with_polymorphic


class LoginView(Resource):
    def post(self):
        user = request.json["user"]
        password = request.json["password"]
        token_de_acceso = None
        if "admin" in user and user == password:
            token_de_acceso = create_access_token(
                identity={
                    "id": user,
                    "usuario": user,
                    "rol": "admin",
                },
                additional_claims={"role": "admin"},
            )
        elif "user" in user and user == password:
            token_de_acceso = create_access_token(
                identity={
                    "id": user,
                    "usuario": user,
                    "rol": "user",
                },
                additional_claims={"role": "user"},
            )
        else:
            return "El usuario no existe", 401

        return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
