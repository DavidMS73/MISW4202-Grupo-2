from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager, jwt_required
import requests as req
import traceback
from json import JSONEncoder

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.app_context().push()

jwt = JWTManager(app)
api = Api(app)

json_encoder = JSONEncoder()

parser = reqparse.RequestParser()
parser.add_argument('usuario', type=str)
parser.add_argument('contrasena', type=str)
class VistaAutorizador(Resource):
    usuarios_url = 'http://usuarios:5000/usuario/validar'

    @jwt_required()
    def get(self):
        return 'El token es válido', 200

    def post(self):
        args = parser.parse_args()
        try:
            headers = {'Content-Type': 'application/json'}
            response = req.post(
                self.usuarios_url,
                data=json_encoder.encode({
                    'usuario': args['usuario'],
                    'contrasena': args['contrasena']
                }),
                headers=headers,
            )
            if response.status_code == 401:
                return {'error': 'Usuario o contraseña incorrectos'}, 401
            
            res_json = response.json()
            access_token = create_access_token(
                identity=res_json['usuario'],
                additional_claims={
                    "nombre": res_json['nombre'],
                    "usuario": res_json['usuario'],
                    "contrasena": res_json['contrasena']
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
