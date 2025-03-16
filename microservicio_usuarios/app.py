from flask import Flask, request
from flask_jwt_extended import get_jwt, JWTManager
from flask_restful import Resource, Api

from modelos import db, Usuario, UsuarioSchema, RolesEnum
from utils import allowed_roles, generate_role_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:arquitectura@arquitecturas-agiles-software.ceebxtes3heo.us-east-1.rds.amazonaws.com:5432/usuarios"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_SECRET_KEY"] = "super-secret"

app_context = app.app_context()
app_context.push()

jwt = JWTManager(app)

db.init_app(app)
db.create_all()

api = Api(app)

usuario_schema = UsuarioSchema()
secret_key = b"clave_secreta"


class VistaUsuarios(Resource):
    @allowed_roles([RolesEnum.LOGISTIC_DIRECTOR])
    def get(self):
        return 456

    @allowed_roles([RolesEnum.LOGISTIC_DIRECTOR])
    def post(self):
        claims = get_jwt()
        user_id: str = str(claims["sub"])
        role_hash = generate_role_hash(request.json["role"], request.json["role"], user_id)

        nuevo_usuario = Usuario(
            nombre=request.json["nombre"],
            usuario=request.json["usuario"],
            contrasena=request.json["contrasena"],
            role=request.json["role"],
            prev_role=request.json["role"],
            role_assigned_by=user_id,
            role_hash=role_hash
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        return usuario_schema.dump(nuevo_usuario)

class VistaUsuario(Resource):
    @allowed_roles([RolesEnum.LOGISTIC_DIRECTOR])
    def put(self, user_id):
        usuario: Usuario = Usuario.query.get_or_404(user_id)

        if "nombre" in request.json:
            usuario.nombre = request.json["nombre"]

        if "usuario" in request.json:
            usuario.usuario = request.json["usuario"]

        if "contrasena" in request.json:
            usuario.contrasena = request.json["contrasena"]

        if "role" in request.json:
            claims = get_jwt()
            responsible_user_id: str = str(claims["sub"])
            usuario.prev_role = usuario.role
            usuario.role = request.json["role"]
            usuario.role_assigned_by = responsible_user_id
            usuario.role_hash = generate_role_hash(usuario.prev_role.value, usuario.role, responsible_user_id)

        db.session.commit()
        return usuario_schema.dump(usuario)

    

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


api.add_resource(VistaValidarUsuario, "/usuario/validar")
api.add_resource(VistaUsuario, "/usuario/<int:user_id>")
api.add_resource(VistaUsuarios, "/usuario")
