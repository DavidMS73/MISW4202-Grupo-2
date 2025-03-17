import csv
import hashlib
import hmac
import os
import traceback
from json import JSONEncoder

import requests as req
from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from flask_jwt_extended import create_access_token
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.app_context().push()

jwt = JWTManager(app)
api = Api(app)

json_encoder = JSONEncoder()
secret_key = b"clave_secreta"

parser = reqparse.RequestParser()
parser.add_argument('usuario', type=str)
parser.add_argument('contrasena', type=str)
class VistaAutorizador(Resource):
    usuarios_url = 'http://usuarios:5000/usuario'

    @jwt_required()
    def get(self):
        token_payload = get_jwt()
        user_id = token_payload['sub']
        response = req.get(
            f"{self.usuarios_url}/{user_id}",
        )

        res_json = response.json()
        if not self.__role_is_valid(res_json):
            self.__log_suspicious_activity(res_json)
            return {'error': 'El rol del usuario no es válido'}, 403

        return 'El token es válido', 200

    def __role_is_valid(self, user):
        user_id: str = str(user["role_assigned_by"])
        role_change: str = user["prev_role"] + "-" + user["role"]
        role_hash = hmac.new(secret_key + user_id.encode(), role_change.encode(), hashlib.sha256).hexdigest()

        return role_hash == user["role_hash"]

    def __log_suspicious_activity(self, res_json):
        file_path = "suspicious-activity.csv"
        file_exists = os.path.exists(file_path)

        with open(file_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["ID Usuario", "Usuario", "Rol", "Rol Anterior", "Motivo"])

            if not file_exists:
                writer.writeheader()

            writer.writerows([{
                "ID Usuario": res_json["id"],
                "Usuario": res_json["usuario"],
                "Rol": res_json["role"],
                "Rol Anterior": res_json["prev_role"],
                "Motivo": "Intento de cambio de rol no autorizado"
            }])

    def post(self):
        args = parser.parse_args()
        try:
            headers = {'Content-Type': 'application/json'}
            response = req.post(
                f"{self.usuarios_url}/validar",
                headers=headers,
                data=json_encoder.encode({
                    'usuario': args['usuario'],
                    'contrasena': args['contrasena']
                }),
            )
            if response.status_code == 401:
                return {'error': 'Usuario o contraseña incorrectos'}, 401

            res_json = response.json()
            if not self.__role_is_valid(res_json):
                self.__log_suspicious_activity(res_json)
                return {'error': 'El rol del usuario no es válido'}, 403

            access_token = create_access_token(
                identity=res_json['id'],
                additional_claims={
                    "nombre": res_json['nombre'],
                    "usuario": res_json['usuario'],
                    "contrasena": res_json['contrasena'],
                    "role": res_json['role']
                }
            )
            return {
                "access_token": access_token
            }, 200
        except Exception as e:
            print(f'Error: {e}')
            return {
                'error': 'Ha ocurrido un error',
                'stacktrace': traceback.format_exc(),
            }, 500


api.add_resource(VistaAutorizador, '/autorizador')
