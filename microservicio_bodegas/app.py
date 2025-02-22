from flask_restful import Resource, Api
from flask import Flask, request
import requests
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ccpms1.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app_context = app.app_context()
app_context.push()

api = Api(app)


class VistaBodegas(Resource):

    def get(self):
        return 123


api.add_resource(VistaBodegas, "/bodega")
