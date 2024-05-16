from flask import Flask, request, jsonify
from http import HTTPStatus
from models import *

app = Flask(__name__)
archivos = None

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong!'

@app.route('/archivos', methods=['POST'])
def post_archivos():
    global archivos
    data = request.json
    archivos = Archivos(data)
    return "", HTTPStatus.NO_CONTENT

@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    global archivos
    return jsonify(archivos.estudiantes()), HTTPStatus.OK

if __name__ == '__main__':
    app.run(debug=True)