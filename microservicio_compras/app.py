from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db
from vistas import VistaCompras, VistaRecomendacionCompras, VistaProductos, VistaEnv, VistaProveedores

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:arquitectura@arquitecturas-agiles-software.ceebxtes3heo.us-east-1.rds.amazonaws.com:5432/compras'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_context = app.app_context()
app_context.push()

app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_SECRET_KEY"] = "super-secret"

jwt = JWTManager(app)

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCompras, "/compra")
api.add_resource(VistaRecomendacionCompras, "/compra/recomendacion")
api.add_resource(VistaProductos, "/producto")
api.add_resource(VistaEnv, "/env")
api.add_resource(VistaProveedores, "/proveedores")
