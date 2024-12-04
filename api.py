from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client['EconoBalance']
user = db['User']
investimentos = db['Investimentos']

app = Flask(__name__)

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if user.find_one({'email': data['email']}):
        return jsonify({'error': 'Usuário já cadastrado'}), 400
    if '@' not in data['email']:
        return jsonify({'error': 'Email inválido'}), 400
    user.insert_one(data)
    result = user.find_one({'email': data['email']})
    result['_id'] = str(result['_id'])  
    return jsonify(result), 201


@app.route('/api/user/<string:email>', methods=['GET'])
def get_user(email):
    result = user.find_one({'email': email})
    if result is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    result['_id'] = str(result['_id'])
    return jsonify(result), 200

@app.route('/api/user', methods=['GET'])
def get_users():
    result = list(user.find())
    for user in result:
        user['_id'] = str(user['_id'])
    return jsonify(result), 200

@app.route('/api/user/<string:email>', methods=['PUT'])
def update_user(email):
    data = request.get_json()
    result = user.find_one({'email': email})
    if result is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    user.update(result,data)
    result = user.find_one({'email': email})
    result['_id'] = str(result['_id'])
    return jsonify(result), 200

@app.route('api/investimentos', methods=['POST'])
def create_investimento():
    data = request.get_json()
    investimentos.insert_one(data)
    result = investimentos.find_one(data)
    result['_id'] = str(result['_id'])
    return jsonify(result), 201

@app.route('api/investimentos/<string:email>', methods=['GET'])
def get_investimentos(email):
    result = list(investimentos.find({'email': email}))
    for investimento in result:
        investimento['_id'] = str(investimento['_id'])
    return jsonify(result), 200

@app.route('api/investimentos/<string:email>', methods=['PUT'])
def update_investimento(email):
    data = request.get_json()
    result = investimentos.find_one({'email': email})
    if result is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    investimentos.update(result,data)
    result = investimentos.find_one({'email': email})
    result['_id'] = str(result['_id'])
    return jsonify(result), 200

@app.route('api/calcula_investimentos/<string:email>', methods=['GET'])
def calcula_investimentos(email):
    result = list(investimentos.find({'email': email}))
    rendimento = 0
    for investimento in result:
        investimento['_id'] = str(investimento['_id'])
        rendimento += investimento['valor_investido'] * investimento['rentabilidade'] / 100
    valor = {'rendimento': rendimento}
    return jsonify(valor), 200

    



app.run(debug=True)