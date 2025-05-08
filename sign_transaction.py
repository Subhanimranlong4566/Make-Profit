from wallet import generate_keys, sign_data
import json
import requests

# Step 1: Generate keys (or load your saved ones)
private_key, public_key = generate_keys()

# Step 2: Create transaction data
transaction = {
    'sender': 'Alice',
    'receiver': 'Bob',
    'amount': 25
}

# Step 3: Sign transaction
transaction_data = json.dumps(transaction, sort_keys=True)
signature = sign_data(transaction_data, private_key)

# Step 4: Prepare full transaction payload
signed_transaction = {
    'sender': transaction['sender'],
    'receiver': transaction['receiver'],
    'amount': transaction['amount'],
    'signature': signature,
    'public_key': public_key
}

# Step 5: Send to the blockchain API
response = requests.post('http://localhost:5000/transactions/new', json=signed_transaction)

print("Server Response:", response.json())
