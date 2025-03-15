from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "API Gateway is running!"})

@app.route('/api/<service_name>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_to_service(service_name, subpath):
    try:
        service_urls = {
            "bodegas": "http://host.docker.internal:9001",
            "ventas": "http://host.docker.internal:9002",
            "compras": "http://host.docker.internal:9000"
        }

        print("service_name: " + service_name)

        if service_name not in service_urls:
            return jsonify({"error": "Service not found"}), 404

        service_url = f"{service_urls[service_name]}/{subpath}"
        print(service_url)        

        # Determina el método HTTP y redirige con datos/cabeceras
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


