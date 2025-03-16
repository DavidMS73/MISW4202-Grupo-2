import hashlib
import hmac
from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt

from modelos.modelos import RolesEnum

secret_key = b"clave_secreta"

# Función para cifrar la clave de un usuario
def cifrar(clave):
    return hashlib.md5(clave.encode("utf-8")).hexdigest()

# Decorator para restringir el acceso segun el rol
def allowed_roles(roles: list[RolesEnum]):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(locations='headers')
            claims = get_jwt()
            if any(claims["role"] == role.value for role in roles):
                return fn(*args, **kwargs)
            else:
                return {"error": "Este rol no tiene permisos para realizar esta acción"}, 403

        return decorator

    return wrapper


def generate_role_hash(prev_role: str, new_role: str, user_id: str):
    role_change: str = prev_role + "-" + new_role
    return hmac.new(secret_key + user_id.encode(), role_change.encode(), hashlib.sha256).hexdigest()
