from flask import Flask, make_response, jsonify, request
from bd import pessoas
import psycopg2

# Update connection string information

host = "51.79.67.184"
dbname = "lasthope_dev"
user = "postgres"
password = "193theth"
sslmode = "require"

# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/carros', methods=['GET'])
def get_carros():

    # Drop previous table of same name if one exists

    cursor.execute("select usr_id, usr_name from tb_users;")
    dadosDoBanco = cursor.fetchall()
    print("Finished dropping table (if existed)")
    return  make_response(
        jsonify(dadosDoBanco)
    )
# inderir dados no banco de dados com insert e pegando os dados do front/postman

@app.route('/carros', methods=['POST'])
def create_carro():
    dadosRecebidosDoFrontEnd = request.json ("pessoas")
    
    nomeRecebidosDoFrontEnd = dadosRecebidosDoFrontEnd["pessoas"]
    return make_response(
        jsonify(
            mesagem = 'LISTA DE USUARIOS.',
            pessoas = [p for p in pessoas if p["pessoas"] == nomeRecebidosDoFrontEnd]
        )
    )

# deletar um registro do banco de dados usando id com a função dropsql

@app.route('/delete/<string:cpf>', methods=['DELETE'])
def delete_pessoa(cpf):
    indiceDaPessoa = next((index for (index, d) in enumerate(pessoas) if d["cpf"] == cpf), None)
    pessoas.pop(indiceDaPessoa)
    return  make_response(
        jsonify("pessoa deletada! :)")
    )
 
app.run()

