from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def rol_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == role:
                return fn(*args, **kwargs)
            else:
                return {"mensaje": "No autorizado"}, 403

        return decorator

    return wrapper
