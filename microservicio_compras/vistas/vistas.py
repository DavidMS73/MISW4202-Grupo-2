import csv
import os
import random
import time
from datetime import date
from random import randint

import requests
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from logica import votar_recomendacion_compras, obtener_recomendaciones_real
from modelos import db, Compra, CompraSchema, Producto, ProductoSchema

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

        bodega_info = content_bodega.json()
        venta_info = content_venta.json()

        "Test purpose"
        time.sleep(2)

        eventos = ["evento_grande", "evento_mediano", "evento_pequeno"]
        eventos_elegidos = eventos[:random.randint(1, 3)]

        resultados = votar_recomendacion_compras(bodega_info, venta_info, eventos_elegidos)
        resultado_esperado = obtener_recomendaciones_real(bodega_info, venta_info, eventos_elegidos)
        first_return_time = min([result.return_time for result in resultados[1]])
        finish_time = time.perf_counter()
        voting_time = finish_time - first_return_time

        file_path = "voting_results.csv"
        file_exists = os.path.exists(file_path)

        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["resultado_1", "resultado_2", "resultado_3", "resultado_final", "resultado_correcto",
                                 "tiempo_votacion"])

            writer.writerow([resultados[1][0].result,
                             resultados[1][1].result,
                             resultados[1][2].result,
                             resultados[0],
                             resultado_esperado,
                             voting_time])

        return {"cantidad": resultados[0], "producto": "Producto {}".format(randint(0, 100))}, 200


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
        compra = Compra.query.get_or_404(id_compra)
        producto.compras.append(compra)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "El usuario ya tiene una compra con ese producto", 409

        return producto_schema.dump(producto)
