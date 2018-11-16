from AKChain_coin import AKChain
from flask import Flask, jsonify, request

app = Flask(__name__)

akchain = AKChain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    prev_hash = akchain.get_prev_block()['hash']
    akchain.choose_transactions({'sender': 'coinbase',
    'receiver' : 'Kos3'})
    AKnumber = akchain.proof_of_work()
    block = akchain.create_block(AKnumber,prev_hash)
    response = {'message': 'Bia ino begir bahash kir bekhar',
    'datablock': block['datablock'],
    'hash': block['hash']}
    return jsonify(response), 200


@app.route('/show_chain', methods = ['GET'])
def show_chain():
    response = {'chain': akchain.chain,
    'length' : len(akchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    flag = akchain.is_valid()
    if flag is True:
        response =  {'message':'All good fam'}
    else:
        response =  {'message': "I don't feel so good Mr. Stark"}

    return jsonify(response), 200

@app.route('/add_transactions', methods = ['POST'])
def add_transactions():
    json = request.get_json()
    keys = ["who", "amount"]
    for transaction in json:
        if not all(key in transaction for key in keys):
            return "ya, you didn't put in the correct input",400
        else:
            akchain.add_transaction(who = transaction['who'], amount = transaction['amount'])
    return "All transactions have been successfully inputed", 201

@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    keys = ["who", "amount"]
    akchain.add_transaction(who = json['who'], amount = json['amount'])
    #akchain.add_transaction({'sender': 'AK', 'receiver': 'Kir'}, amount = 2000)
    response = {'message': "transaction added"}
    return jsonify(response), 201

@app.route('/connect_nodes', methods = ['POST'])
def connect_nodes():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes == None:
        response = "dude u didn't give me any nodes bro"
        return jsonify(response), 400
    else:
        for node in nodes:
            akchain.connect_node(node)
        response = "all done"
        return jsonify(response), 201

@app.route('/show_mempool', methods = ['GET'])
def show_mempool():
    response = {"mempool": akchain.mempool,
    "length": len(akchain.mempool)}
    return jsonify(response), 200

@app.route('/consensus', methods = ['GET'])
def consensus():
    is_replaced = akchain.consensus()
    if is_replaced:
        response = {"message": "Replaced",
        "chain": akchain.chain}
        return jsonify(response), 200
    else:
        response = {"message": "Same Same",
        "chain": akchain.chain}
        return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5003)