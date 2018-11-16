# Code by AK74

import hashlib
import json
import datetime
from flask import Flask, jsonify

class AKChain():
    '''
    Base class for a simple blockchain
    '''

    def __init__(self):
        self.chain = []
        self.create_block(AKnumber=1, prev_hash='0')

    def create_block(self,AKnumber,prev_hash):

        datablock = self.create_datablock(AKnumber,prev_hash)
        chash = self.calc_hash(datablock)
        block = {'datablock' : datablock,
        'hash': chash}
        self.chain.append(block)
        return block

    def create_datablock(self,AKnumber,prev_hash):
        time = datetime.datetime.now()
        time = time.strftime("%Y:%m:%d:%H:%M")
        datablock = {'id' : len(self.chain) + 1,
        'prev_hash' : prev_hash,
        'AKnumber': AKnumber,
        'time' : time}
        return datablock

    def calc_hash(self,datablock):
        '''
        Calculate the hash value for a block
        '''
        chash = hashlib.sha256(json.dumps(datablock, sort_keys=True).encode()).hexdigest()
        return chash

    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self):
        '''
        pass
        '''
        AKnumber = 1
        isgood = False
        prev_hash = self.get_prev_block()['hash']
        while isgood is False:
            datablock = self.create_datablock(AKnumber,prev_hash)
            chash = self.calc_hash(datablock)
            if chash[:4] == '0000':
                isgood = True
            else:
                AKnumber += 1
        return AKnumber
    
    def is_valid(self):
        '''
        pass
        '''
        if len(self.chain) == 1: 
            return True
        else:
            #prev_block = self.chain[0]
            for i in range(len(self.chain)-1):
                if self.chain[i]['hash'] != self.chain[i+1]['datablock']['prev_hash']:
                    return False
                elif self.calc_hash(self.chain[i+1]['datablock']) != self.chain[i+1]['hash']:
                    return False
                elif self.calc_hash(self.chain[i+1]['datablock'])[:4] != '0000':
                    return False
            return True


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