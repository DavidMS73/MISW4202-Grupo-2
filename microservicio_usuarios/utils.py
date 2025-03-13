from functools import wraps
import hashlib
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from modelos.modelos import RolesEnum

# Función para cifrar la clave de un usuario
def cifrar(clave):
    return hashlib.md5(clave.encode("utf-8")).hexdigest()

# Decorator para restringir el acceso segun el rol
def allowed_roles(roles: list[RolesEnum]):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if any(claims["role"] == role.value for role in roles):
                return fn(*args, **kwargs)
            else:
                return {"error": "Este rol no tiene permisos para realizar esta acción"}, 403

        return decorator

    return wrapper