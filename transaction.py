import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender  # PEM-encoded public key
        self.recipient = recipient  # PEM-encoded public key
        self.amount = amount
        self.signature = signature  # base64 string or None

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

    def compute_hash(self):
        tx_dict = self.to_dict()
        tx_string = json.dumps(tx_dict, sort_keys=True)
        return SHA256.new(tx_string.encode('utf-8'))

    def sign_transaction(self, private_key_pem):
        private_key = RSA.import_key(private_key_pem)
        hash_value = self.compute_hash()
        signature = pkcs1_15.new(private_key).sign(hash_value)
        self.signature = base64.b64encode(signature).decode()

    def is_valid(self):
        if self.sender == "MINING_REWARD":
            return True  # mining reward has no signature
        if not self.signature:
            return False
        try:
            public_key = RSA.import_key(self.sender)
            hash_value = self.compute_hash()
            pkcs1_15.new(public_key).verify(hash_value, base64.b64decode(self.signature))
            return True
        except (ValueError, TypeError):
            return False
