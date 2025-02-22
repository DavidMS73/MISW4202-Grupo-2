from flask import Flask
from flask_restful import Api
from modelos import db
from vistas import VistaCompras, VistaRecomendacionCompras, VistaProductos, VistaEnv

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ccpms2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCompras, "/compra")
api.add_resource(VistaRecomendacionCompras, "/compra/recomendacion")
api.add_resource(VistaProductos, "/producto")
api.add_resource(VistaEnv, "/env")
