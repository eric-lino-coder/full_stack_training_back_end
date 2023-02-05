from flask import Flask, make_response, jsonify
from bd import Carros

app = Flask(__name__)

@app.route('/carros', methods=['GET'])
def get_carros():
    return  make_response(
        jsonify(Carros)
    )

app.run()

