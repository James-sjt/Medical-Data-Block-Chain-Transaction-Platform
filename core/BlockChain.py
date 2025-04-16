from core.Block import Block
import time
import datetime

class BlockChain:
    def __init__(self):
        self.chain = [self._create_genesis_block()]
        self.difficulty = 5
        self.pending_transactions = []
        self.mining_reward = 100

    @staticmethod
    def _create_genesis_block():
        timestamp = time.mktime(time.strptime('2025-04-16 00:00:00', '%Y-%m-%d %H:%M:%S'))
        block = Block(timestamp, [], '')
        return block

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transaction(self):
        if self.verify_blockchain():
            block = Block(time.time(), self.pending_transactions, self.chain[-1].hash)
            block.mine_block(self.difficulty)
            self.chain.append(block)
            self.pending_transactions = []
            Time = datetime.datetime.fromtimestamp(float(block.transactions[0].timestamp))
            data_block = {
                'previous_hash': block.previous_hash,
                'timestamp': block.timestamp,
                'transactions': {
                    'filename': block.transactions[0].filename,
                    'uploader': block.transactions[0].uploader,
                    'hash': block.transactions[0].hash,
                    'timestamp': Time.strftime('%Y-%m-%d %H:%M:%S'),
                    'pre_owner': block.transactions[0].pre_owner,
                    'current_owner': block.transactions[0].current_owner,
                    'trans_type': block.transactions[0].trans_type,
                },
                'nonce': block.nonce,
                'hash': block.hash
            }

            with open("Transaction.txt", "a", encoding="utf-8") as file:
                file.write(str(data_block) + '\n')
        else:
            raise RuntimeError('Block chain has been changed!')


    def verify_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.calculate_hash():
                return False
        return True


