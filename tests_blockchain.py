import unittest
from blockchain import Blockchain
from transaction import Transaction
from wallet import generate_keys

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()
        self.private_key, self.public_key = generate_keys()
        self.recipient_key = generate_keys()[1]

    def test_genesis_block(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)

    def test_transaction_and_mining(self):
        tx = Transaction(
            sender=self.public_key,
            recipient=self.recipient_key,
            amount=10,
            signature=''
        )
        tx.sign_transaction(self.private_key)
        self.assertTrue(tx.is_valid())
        self.assertTrue(self.blockchain.add_transaction(tx))

        # Mine block
        index = self.blockchain.mine(self.public_key)
        self.assertEqual(index, 1)
        self.assertEqual(len(self.blockchain.chain), 2)

    def test_invalid_transaction(self):
        tx = Transaction(
            sender=self.public_key,
            recipient=self.recipient_key,
            amount=10,
            signature='invalid'
        )
        self.assertFalse(tx.is_valid())
        self.assertFalse(self.blockchain.add_transaction(tx))

    def test_wallet_key_generation(self):
        private_key, public_key = generate_keys()
        self.assertTrue(private_key.startswith('-----BEGIN RSA PRIVATE KEY-----'))
        self.assertTrue(public_key.startswith('-----BEGIN PUBLIC KEY-----'))

if __name__ == '__main__':
    unittest.main()
