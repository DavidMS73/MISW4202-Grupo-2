from flask_restful import Resource, Api
from flask import Flask, request

from modelos import db, Usuario, UsuarioSchema, RolesEnum
from utils import allowed_roles

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:arquitectura@arquitecturas-agiles-software.ceebxtes3heo.us-east-1.rds.amazonaws.com:5432/usuarios"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

usuario_schema = UsuarioSchema()


class VistaUsuarios(Resource):

    @allowed_roles([RolesEnum.LOGISTIC_DIRECTOR])
    def get(self):
        return 456

    @allowed_roles([RolesEnum.LOGISTIC_DIRECTOR])
    def post(self):
        nuevo_usuario = Usuario(
            nombre=request.json["nombre"],
            usuario=request.json["usuario"],
            contrasena=request.json["contrasena"],
            type=request.json["type"],
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        return usuario_schema.dump(nuevo_usuario)
    

class VistaValidarUsuario(Resource):
    def post(self):
        req_json = request.json
        usuario = Usuario.query.filter(
            Usuario.usuario == req_json['usuario'],
            Usuario.contrasena == req_json['contrasena']
        ).first()
        if usuario == None:
            return 'Usuario o contraseña incorrectos', 401
        return usuario_schema.dump(usuario)


api.add_resource(VistaUsuarios, "/usuario")
api.add_resource(VistaValidarUsuario, "/usuario/validar")
