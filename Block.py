import json
import hashing


class Block:
    def __init__(self, hash_previous_block, transactions, nonce):
        self.transactions = transactions
        self.hash_previous_block = hash_previous_block
        self.nonce = nonce
        self.transaction_hashes = self.get_transaction_hashes()

    def get_hash(self):
        data = self.get_dict()
        json_data = json.dumps(data)
        return hashing.hash(json_data)

    def get_transaction_hashes(self):
        return [x.get_hash() for x in self.transactions]

    def get_dict(self):
        return {
           "transaction_hashes": self.get_transaction_hashes(),
           "transactions": list(map(lambda x: {
                "utxos": x["utxos"] if "utxos" in x else [],
                "receiver_public_keys": x["receiver_public_keys"],
                "messages": x["messages"],
                "signature": x["signature"] if "signature" in x else "",
            }, list(map(lambda x: x.get_dict(), self.transactions)))),
            "hash_previous_block": self.hash_previous_block,
            "nonce": self.nonce
        }
