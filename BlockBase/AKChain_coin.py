import hashlib
import json
import datetime
import requests
from urllib.parse import urlparse

class AKChain():
    '''
    Base class for a simple blockchain
    '''

    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.mempool = []
        self.selected_transactions=[]
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
        time = time.strftime("%Y:%m:%d:%H:%M:%S")
        datablock = {'id' : len(self.chain) + 1,
        'prev_hash' : prev_hash,
        'AKnumber': AKnumber,
        'time' : time,
        'transactions': self.selected_transactions}
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
    
    def is_valid(self,chain=None):
        '''
        pass
        '''
        if chain==None:
            chain = self.chain

        if len(chain) == 1: 
            return True
        else:
            for i in range(len(chain)-1):
                if chain[i]['hash'] != chain[i+1]['datablock']['prev_hash']:
                    return False
                elif self.calc_hash(chain[i+1]['datablock']) != chain[i+1]['hash']:
                    return False
                elif self.calc_hash(chain[i+1]['datablock'])[:4] != '0000':
                    return False
            return True

    def add_transaction(self, who, amount):
        transaction = {'sender': who['sender'],
        'receiver': who['receiver'],
        'amount': amount}
        self.mempool.append(transaction)
        return transaction

    def add_reward(self, who):
        transaction = {'sender': who['sender'],
        'receiver': who['receiver'],
        'amount': 50}
        self.selected_transactions.append(transaction)
        return transaction


    def choose_transactions(self, who, transactions= None):
        self.selected_transactions = self.mempool
        self.add_reward(who)
        self.mempool = []
        return

    def connect_node(self,node_url):
        parsed_node = urlparse(node_url)
        self.nodes.add(parsed_node.netloc)

    def consensus(self):
        self._update_mempool()
        max_chain_length = len(self.chain)
        reset = False
        for node in self.nodes:
            chain_response = requests.get(f'http://{node}/show_chain')
            if chain_response.status_code == 200:
                length = chain_response.json()['length']
                chain = chain_response.json()['chain']
                #if (length > max_chain_length) and self.is_valid(chain):
                if (length > max_chain_length):
                    max_chain_length = length
                    self.chain = chain
                    reset = True
        return reset

    def _update_mempool(self):
        #Needs to be updated
        max_mem_length = len(self.mempool)
        reset = False
        for node in self.nodes:
            mem_response = requests.get(f'http://{node}/show_mempool')
            if mem_response.status_code == 200:
                length = mem_response.json()['length']
                mem = mem_response.json()['mempool']
                if length > max_mem_length:
                    max_mem_length = length
                    self.mempool = mem
                    reset = True
        return reset
                

        
