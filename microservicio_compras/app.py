from microservicio_compras import create_app
from flask_restful import Api
from .modelos import db
from .vistas import VistaCompras, VistaRecomendacionCompras, VistaProductos

app = create_app("default")
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCompras, "/compra")
api.add_resource(VistaRecomendacionCompras, "/compra/recomendacion")
api.add_resource(VistaProductos, "/producto")
