from uuid import uuid4

from api.frazaochain import Frazaochain
from flask import Flask, jsonify, request

app = Flask(__name__)

node_identifier = str(uuid4()).replace("-", "")

frazaochain = Frazaochain()


@app.route("/", methods=["GET"])
def main():
    return "oi", 200


@app.route("/mine", methods=["GET"])
def mine():
    last_block = frazaochain.last_block
    last_proof = last_block["proof"]
    proof = frazaochain.proof_of_work(last_proof)
    frazaochain.new_transaction(sender="0", recipient=node_identifier, amount=1)

    previous_hash = frazaochain.hash(last_block)
    block = frazaochain.new_block(proof, previous_hash)
    response = {
        "message": "New block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    return jsonify(response), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()
    if values is None:
        return "Missing requirements", 400

    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Mising requirements", 400

    index = frazaochain.new_transaction(values["sender"], values["recipient"], values["amount"])

    response = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(response), 201


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {"chain": frazaochain.chain, "length": len(frazaochain.chain)}

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5005)


@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    values = request.get_json()

    nodes = values.get("nodes")
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        frazaochain.register_node(node)

    response = {"message": "New nodes have been added", "total_nodes": list(frazaochain.nodes)}
    return jsonify(response), 201


@app.route("/nodes/resolve", methods=["GET"])
def consensus():
    replaced = frazaochain.resolve_conflicts()

    if replaced:
        response = {"message": "Frazaochain was replaced", "new_chain": frazaochain.chain}
    else:
        response = {"message": "Frazaochain is authoritative", "chain": frazaochain.chain}

    return jsonify(response), 200
