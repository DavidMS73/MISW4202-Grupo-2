from flask_restful import Resource, Api
from flask import Flask, request
import requests
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:arquitectura@arquitecturas-agiles-software.ceebxtes3heo.us-east-1.rds.amazonaws.com:5432/bodegas"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app_context = app.app_context()
app_context.push()

api = Api(app)


class VistaBodegas(Resource):

    def get(self):
        return 123


api.add_resource(VistaBodegas, "/bodega")
