import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "API Gateway funcionando!"})

@app.route('/api/<service_name>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_to_service(service_name, subpath):
    try:
        # Autorizar usuario
        if service_name != "autorizador":
            response = requests.get("http://autorizador:5000/autorizador",
                                    headers={"Authorization": request.headers.get("Authorization")})

            if response.status_code != 200:
                return response.json(), response.status_code

        service_name = "compras" if service_name == "proveedores" else service_name
        base_service_url = "http://" + service_name + ":5000"
        
        service_ports = {
            "compras": 9000,
            "bodegas": 9001,
            "ventas": 9002,
            "usuarios": 9003,
            "autorizador": 9004,
            "proveedores": 9000
        }

        if service_name not in service_ports:
            return jsonify({"error": "Service not found"}), 404

        service_url = f"{base_service_url}/{subpath}"

        if request.method == 'GET':
            response = requests.get(service_url, params=request.args, headers=request.headers)
        elif request.method == 'POST':
            response = requests.post(service_url, json=request.json, headers=request.headers, params=request.args)
        elif request.method == 'PUT':
            response = requests.put(service_url, json=request.json, headers=request.headers, params=request.args)
        elif request.method == 'DELETE':
            response = requests.delete(service_url, headers=request.headers, params=request.args)
        else:
            return jsonify({"error": "Unsupported HTTP method"}), 405

        return (response.content, response.status_code, response.headers.items())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


