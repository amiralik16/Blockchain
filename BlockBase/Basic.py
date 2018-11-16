from AKChain import AKChain
from flask import Flask, jsonify

app = Flask(__name__)

akchain = AKChain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    prev_hash = akchain.get_prev_block()['hash']
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

app.run(host = '0.0.0.0', port = 5000)