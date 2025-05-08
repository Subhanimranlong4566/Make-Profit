from flask import Flask, jsonify, request
from blockchain import Blockchain
from transaction import Transaction
from wallet import generate_keys
import json

app = Flask(__name__)
blockchain = Blockchain()

# Home
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to MakeProfit Blockchain'}), 200

# View the full blockchain
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify({'length': len(chain_data), 'chain': chain_data}), 200

# Mine a block
@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block.proof
    proof = blockchain.proof_of_work(previous_proof)

    blockchain.add_transaction(sender="MINING", receiver="node", amount=10)
    block = blockchain.create_block(proof, blockchain.hash_block(previous_block))

    response = {
        'message': 'Block mined successfully!',
        'index': block.index,
        'timestamp': block.timestamp,
        'proof': block.proof,
        'previous_hash': block.previous_hash,
        'transactions': block.transactions
    }
    return jsonify(response), 201

# Add a new transaction
@app.route('/transactions/new', methods=['POST'])
def add_transaction():
    tx_data = request.get_json()
    required_fields = ['sender', 'receiver', 'amount', 'signature', 'public_key']

    if not all(field in tx_data for field in required_fields):
        return 'Missing fields in transaction data', 400

    transaction = Transaction(
        sender=tx_data['sender'],
        receiver=tx_data['receiver'],
        amount=tx_data['amount'],
        signature=tx_data['signature'],
        public_key=tx_data['public_key']
    )

    if not transaction.is_valid():
        return 'Invalid transaction signature!', 400

    index = blockchain.add_transaction(
        sender=transaction.sender,
        receiver=transaction.receiver,
        amount=transaction.amount
    )

    return jsonify({'message': f'Transaction will be added to Block {index}'}), 201

# Create new wallet (RSA key pair)
@app.route('/wallet/new', methods=['GET'])
def create_wallet():
    private_key, public_key = generate_keys()
    return jsonify({
        'private_key': private_key,
        'public_key': public_key
    }), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
