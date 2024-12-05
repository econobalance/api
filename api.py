from flask import Flask, request, jsonify
from dotenv import load_dotenv
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS
import os

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

client = MongoClient(MONGODB_URI, server_api=ServerApi('1'), tls=True, serverSelectionTimeoutMS=5000, connectTimeoutMS=10000)
db = client['EconoBalance']
print(db.list_collection_names())
user = db['User']
investimentos = db['Investimentos']
gastos = db['Gasto']
saldo2 = db['teste']




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/user/', methods=['POST'])
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

@app.route('/api/investimentos', methods=['POST'])
def create_investimento():
    data = request.get_json()
    investimentos.insert_one(data)
    result = investimentos.find_one(data)
    result['_id'] = str(result['_id'])
    return jsonify(result), 201

@app.route('/api/investimentos/<string:email>', methods=['GET'])
def get_investimentos(email):
    result = list(investimentos.find({'email': email}))
    for investimento in result:
        investimento['_id'] = str(investimento['_id'])
    return jsonify(result), 200

@app.route('/api/investimentos/<string:email>', methods=['PUT'])
def update_investimento(email):
    data = request.get_json()
    result = investimentos.find_one({'email': email})
    if result is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    investimentos.update(result,data)
    result = investimentos.find_one({'email': email})
    result['_id'] = str(result['_id'])
    return jsonify(result), 200

@app.route('/api/calcula_investimentos/<string:email>', methods=['GET'])
def calcula_investimentos(email):
    result = list(investimentos.find({'email': email}))
    rendimento = 0
    for investimento in result:
        investimento['_id'] = str(investimento['_id'])
        rendimento += investimento['valor_investido'] * investimento['rentabilidade'] / 100
    valor = {'rendimento': rendimento}
    return jsonify(valor), 200

@app.route('/api/saldo/<string:email>', methods=['GET'])
def saldo(email):
    result = saldo2.find_one({'email': email})
    if result is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    result['_id'] = str(result['_id'])
    return jsonify(result), 200

@app.route('/api/saldo/<string:email>', methods=['PUT'])
def update_saldo(email):
    data = request.get_json()
    result = saldo2.find_one({'email': email})
    if result is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    saldo2.update_one({'email': email}, {'$set': {'saldo': data['saldo']}})
    result = saldo2.find_one({'email': email})
    result['_id'] = str(result['_id'])
    return jsonify(result), 200

@app.route('/api/saldo/<string:email>', methods=['POST'])
def create_saldo(email):
    try:
        data = request.get_json()
        print(email)
        
        if 'email' not in data:
            return jsonify({'error': 'O campo email é necessário'}), 400

        if saldo2.find_one({'email': email}):
            return jsonify({'error': 'Saldo já cadastrado para este email'}), 400

        saldo2.insert_one(data)

        result = saldo2.find_one({'email': email})
        result['_id'] = str(result['_id'])
        return jsonify(result), 201
    
    except pymongo.errors.DuplicateKeyError:
        return jsonify({'error': 'Saldo já cadastrado para este email'}), 400
    except pymongo.errors.ServerSelectionTimeoutError:
        return jsonify({'error': 'Erro de conexão com o banco de dados'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/gastos/<string:email>', methods=['POST'])
def create_gasto(email):
    data = request.get_json()
    gastos.insert_one(data)
    result = gastos.find_one(data)
    result['_id'] = str(result['_id'])
    return jsonify(result), 201

@app.route('/api/gastos/<string:email>', methods=['GET'])
def get_gastos(email):
    result = list(gastos.find({'email': email}))
    for gasto in result:
        gasto['_id'] = str(gasto['_id'])
    return jsonify(result), 200

@app.route('/api/gastos/<string:email>', methods=['PUT'])
def update_gasto(email):
    data = request.get_json()
    result = gastos.find
    if result is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    gastos.update_one(result,data)
    result = gastos.find_one({'email': email})
    result['_id'] = str(result['_id'])
    return jsonify(result), 200

@app.route('/api/calcula_gastos/<string:email>', methods=['GET'])
def calcula_gastos(email):
    result = list(gastos.find({'email': email}))
    total = 0
    for gasto in result:
        gasto['_id'] = str(gasto['_id'])
        total += gasto['valor']
    valor = {'total': total}
    return jsonify(valor), 200

@app.route('/api/gastos/<string:id>', methods=['DELETE'])
def delete_gasto(id):
    gastos.delete_one({'_id': id})
    return jsonify({'message': 'Gasto deletado com sucesso'}), 200
    
    

if __name__ == '__main__':
    app.run(debug=True)