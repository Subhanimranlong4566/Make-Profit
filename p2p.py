from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from blockchain import Blockchain
from transaction import Transaction
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
blockchain = Blockchain()
peers = set()

@app.route('/peers', methods=['GET', 'POST'])
def peer_nodes():
    if request.method == 'POST':
        data = request.get_json()
        node = data.get('node')
        if node:
            peers.add(node)
            return jsonify({'message': f'Node {node} added'}), 201
        return jsonify({'error': 'No node provided'}), 400
    return jsonify({'peers': list(peers)})

@socketio.on('broadcast_transaction')
def broadcast_transaction(data):
    tx = Transaction(data['sender'], data['recipient'], data['amount'], data['signature'])
    if tx.is_valid():
        blockchain.add_transaction(tx)
        emit('transaction_received', data, broadcast=True)
    else:
        emit('error', {'message': 'Invalid transaction signature'})

@socketio.on('broadcast_block')
def broadcast_block(data):
    block_data = data['block']
    proof = data['proof']
    new_block = blockchain.last_block()
    new_block.index = block_data['index']
    new_block.transactions = block_data['transactions']
    new_block.previous_hash = block_data['previous_hash']
    new_block.timestamp = block_data['timestamp']
    new_block.nonce = block_data['nonce']
    
    added = blockchain.add_block(new_block, proof)
    emit('block_received', {'status': 'added' if added else 'rejected'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=8000)
