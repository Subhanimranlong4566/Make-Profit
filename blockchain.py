from block import Block
from transaction import Transaction
import time

class Blockchain:
    difficulty = 2
    mining_reward = 10

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, [], "0")
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if transaction.is_valid():
            self.unconfirmed_transactions.append(transaction)
            return True
        return False

    def proof_of_work(self, block):
        block.nonce = 0
        while not block.compute_hash().startswith('0' * self.difficulty):
            block.nonce += 1
        return block.compute_hash()

    def add_block(self, block, proof):
        last_hash = self.last_block().compute_hash()
        if last_hash != block.previous_hash or not proof.startswith('0' * self.difficulty):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def mine(self, miner_address):
        reward_tx = Transaction("MINING", miner_address, self.mining_reward)
        self.unconfirmed_transactions.insert(0, reward_tx)
        new_block = Block(index=len(self.chain),
                          transactions=[tx.__dict__ for tx in self.unconfirmed_transactions],
                          previous_hash=self.last_block().compute_hash())
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
