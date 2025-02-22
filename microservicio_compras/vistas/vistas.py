from flask import request
import requests
from modelos import db, Compra, CompraSchema, Producto, ProductoSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import date
import time
import os

compra_schema = CompraSchema()
producto_schema = ProductoSchema()

env_bodegas_host = os.environ.get('BODEGAS_HOST')
env_ventas_host = os.environ.get('VENTAS_HOST')
bodegas_host = env_bodegas_host if env_bodegas_host else 'http://127.0.0.1:9001'
ventas_host = env_ventas_host if env_ventas_host else 'http://127.0.0.1:9002'

class VistaEnv(Resource):
    def get(self):
        return {
            "bodegas_host": bodegas_host,
            "ventas_host": ventas_host,
        }

class VistaCompras(Resource):

    def post(self):
        nueva_compra = Compra(
            estado=request.json["estado"], fecha_creacion=date.today()
        )
        db.session.add(nueva_compra)
        db.session.commit()
        return compra_schema.dump(nueva_compra)

    def get(self):
        return [compra_schema.dump(ca) for ca in Compra.query.all()]


class VistaRecomendacionCompras(Resource):

    def get(self):
        "Simula una recomendación de compras"
        content_bodega = requests.get(f"{bodegas_host}/bodega")
        content_venta = requests.get(f"{ventas_host}/venta")

        if content_bodega.status_code == 404:
            return content_bodega.json(), 404
        
        if content_venta.status_code == 404:
            return content_venta.json(), 404

        else:
            bodega_info = content_bodega.json()
            venta_info = content_venta.json()

            "Test purpose"
            time.sleep(2)

            return [
                {
                    "nombre": "Producto 1",
                    "bodega": bodega_info,
                    "venta": venta_info,
                    "descripcion": "Descripción del producto 1",
                    "condiciones_almacenamiento": "Condiciones de almacenamiento del producto 1",
                    "valor_unidad": 1000,
                },
            ]


class VistaProductos(Resource):
    def post(self):
        nuevo_producto = Producto(
            nombre=request.json["nombre"],
            descripcion=request.json["descripcion"],
            condiciones_almacenamiento=request.json["condiciones_almacenamiento"],
            valor_unidad=request.json["valor_unidad"],
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return producto_schema.dump(nuevo_producto)

    def get(self):
        return [producto_schema.dump(ca) for ca in Producto.query.all()]


class VistaComprasProductos(Resource):

    def post(self, id_producto, id_compra):
        producto = Producto.query.get_or_404(id_producto)
        compra = compra.query.get_or_404(id_compra)
        producto.compras.append(compra)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "El usuario ya tiene una compra con ese producto", 409

        return producto_schema.dump(producto)
