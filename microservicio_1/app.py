from microservicio_1 import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import requests
import json

app = create_app("default")
app_context = app.app_context()
app_context.push()

api = Api(app)


class VistaBodegas(Resource):

    def get(self):
        return 123


api.add_resource(VistaBodegas, "/bodega")
