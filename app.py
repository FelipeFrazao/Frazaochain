from uuid import uuid4

from flask import Flask, jsonify, request

from api.frazaochain import Frazaochain

app = Flask(__name__)

node_identifier = str(uuid4()).replace("-", "")

frazaochain = Frazaochain()


@app.route('/', methods=['GET'])
def main():
    return 'oi', 200


@app.route('/mine', methods=['GET'])
def mine():
    last_block = frazaochain.last_block
    last_proof = last_block['proof']
    proof = frazaochain.proof_of_work(last_proof)
    frazaochain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = frazaochain.hash(last_block)
    block = frazaochain.new_block(proof, previous_hash)
    response = {
        'message': "New block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(value in values for requirements in required):
        return "Mising requirements", 400

    index = frazaochain.new_transaction(values['sender'],
                                        values['recipient', values['amount']])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response, 201)


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': frazaochain.chain,
        'length': len(frazaochain.chain)
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
