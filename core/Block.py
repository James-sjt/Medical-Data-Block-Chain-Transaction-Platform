import hashlib
import json
import time
from .Transaction import TransactionEncoder


class Block:

    def __init__(self, timestamp, transactions, previous_hash=''):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        raw_str = self.previous_hash + str(self.timestamp) + json.dumps(self.transactions, ensure_ascii=False, cls=TransactionEncoder) + str(self.nonce)
        sha256 = hashlib.sha256()
        sha256.update(raw_str.encode('utf-8'))
        hash = sha256.hexdigest()
        return hash

    def mine_block(self, difficulty):
        time_start = time.time()
        while self.hash[0: difficulty] != ''.join(['0'] * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("挖到区块:%s, 耗时: %f秒" % (self.hash, time.time() - time_start))

