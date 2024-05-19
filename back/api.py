from flask import Flask, request, jsonify
from http import HTTPStatus
from analyzer import Archivos

app = Flask(__name__)
archivos: Archivos = None

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

@app.route('/comparar', methods=['GET'])
def get_comparasion_archivos():
    global archivos
    matricula1, matricula2 = request.args.get('matricula1'), request.args.get('matricula2')

    return jsonify(archivos.comparacion(matricula1, matricula2)), HTTPStatus.OK

@app.route('/heatmap', methods=['GET'])
def get_heatmap():
    global archivos

    return jsonify(archivos.heatmap), HTTPStatus.OK

if __name__ == '__main__':
    app.run(debug=True)