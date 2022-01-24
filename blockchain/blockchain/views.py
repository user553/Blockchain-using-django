from django.http import JsonResponse
from django.http import response
from django.http.response import HttpResponse
import datetime
import hashlib
import json

# from blockchain import blockchain


class Blockchain:

    def __init__(self) -> None:
        self.chain = []
        self.createBlock(nonce=1, prevHash='0')

    def createBlock(self, nonce, prevHash):

        index = len(self.chain) + 1

        block = {
            'index': index,
            'timestamp': str(datetime.datetime.now()),
            'nonce': nonce,
            'prevHash': prevHash,
        }

        self.chain.append(block)

        return block
    
    def getLastBlock(self):
        return self.chain[-1]

    def proofOfWork(self, prevNonce):
        newNonce = 1
        checkNonce = False

        while not checkNonce:
            hashOperation = hashlib.sha256(str(newNonce^2 - prevNonce^2).encode()).hexdigest()
            if hashOperation[:4] == '0000':
                checkNonce = True
            else:
                newNonce += 1

        return newNonce

    def hash(seff, block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

    def isChainValid(self, chain):
        prevBlock = chain[0]
        blockIndex = 1

        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['prevHash'] != self.hash(prevBlock):
                return False

            prevNonce = prevBlock['nonce']
            currentNonce = block['nonce']
            hashOperation = hashlib.sha256(str(currentNonce^2 - prevNonce^2).encode()).hexdigest()
            
            if hashOperation[:4] != '0000':
                return False

            prevBlock = block
            blockIndex += 1

        return True


blockchain = Blockchain()

def get_chain(request):

    if request.method == 'GET':
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }

    return JsonResponse(response) 

def mine_block(request):

    if request.method == 'GET':
        previousBlock = blockchain.getLastBlock()
        previousNonce = previousBlock['nonce']
        newNonce = blockchain.proofOfWork(previousNonce)
        prevHash = blockchain.hash(previousBlock)
        block = blockchain.createBlock(newNonce, prevHash)
        
        response = {
            'message': 'Block is mined',
            'block': block,
        }
    return JsonResponse(response)

def is_chain_valid(request):

    if request.method == 'GET':
        is_valid = blockchain.isChainValid(blockchain.chain)

        if is_valid:
            response = {
                'message': 'blockchain is valid'
            }
        else:
            response = {
                'message': 'blockchain is not valid'
            }

    return JsonResponse(response)