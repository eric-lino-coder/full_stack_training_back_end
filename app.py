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


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/carros', methods=['GET'])
def get_carros():

    #cusor.execute é o comando que roda uma query no banco de dados configurado pré-viamente 
    cursor = conn.cursor()
    cursor.execute("select usr_id, usr_name from tb_users;")
    dadosDoBanco = cursor.fetchall() 
    cursor.close()

    return  make_response(
        jsonify(dadosDoBanco)
    )
# inderir dados no banco de dados com insert e pegando os dados do front/postman

@app.route('/carros', methods=['POST'])
def create_carro():
    #request.json é a variavel que esta armazenando os dados que o front-end esta enviando
    cursor = conn.cursor()
    dadosRecebidosDoFrontEnd = request.json

    #aqui estamos acessando aspropriedades do objeto recebido do front-end
    nomeRecebidosDoFrontEnd = dadosRecebidosDoFrontEnd["usr_name"]
    pagamentoRecebidoDoFrontEnd = dadosRecebidosDoFrontEnd["usr_dadospagamento"]
    
    print("nomeRecebidosDoFrontEnd:",nomeRecebidosDoFrontEnd)
    print("pagamentoRecebidoDoFrontEnd:",pagamentoRecebidoDoFrontEnd)

    query = "INSERT INTO tb_users (usr_name , usr_dadospagamento) values ('{p2}', '{p3}');"
    formatted_query = query.format(p2=nomeRecebidosDoFrontEnd, p3=pagamentoRecebidoDoFrontEnd)
    cursor.execute(formatted_query)
    conn.commit()
    cursor.close()
    return make_response(
         jsonify(
             mesagem = 'usuario cadastrado.',          
         )
     )

# deletar um registro do banco de dados usando id com a função dropsql

@app.route('/delete/<string:usr_id>', methods=['DELETE'])
def delete_pessoa(usr_id):
    cursor = conn.cursor()
    
    query = "DELETE FROM tb_users WHERE usr_id = '{p2}';"
    formatted_query = query.format(p2=usr_id)
    cursor.execute(formatted_query)
    conn.commit()
    cursor.close()

    return  make_response(
    jsonify("pessoa deletada! :)")
    )
 
app.run()

