import json
import os
import hashing
from Block import Block
from CONFIG import mining_target
from Genesis import genesis_coinbase
from Transaction import Coinbase, Transaction
from UTXO import UTXO

the_blockchain = None


def get_blockchain():
    global the_blockchain
    if the_blockchain == None:
        the_blockchain = Blockchain()
    return the_blockchain


class Blockchain:
    def __init__(self):
        self.blocks = [Block("ZEvMflZDcwQJmarInnYi88px+6HZcv2Uoxw7+/JOOTg=",
                             [genesis_coinbase()], 0)]

    def insert_block(self, block):
        print(block.transactions)
        if not isinstance(block, Block):
            return False
        for tx in block.transactions:
            if not tx.is_valid():
                return False
            if isinstance(tx, Transaction):
                for utxo in tx.utxos:
                    if not self.is_valid_UTXO(utxo):
                        return False
        if not self.check_agains_target(block.get_hash()):
            return False
        self.blocks.append(block)
        self.write_to_blockchain()
        return True

    def check_agains_target(self, hash_string):
        hex = hashing.string_to_hex(hash_string)
        for i in range(1, mining_target+1):
            if not hex[i] == "0":
                return False
        return True

    def get_utxos(self, public_key):
        utxos = []
        for block in self.blocks:
            for tx in block.transactions:
                counter = 0
                for pk in tx.receiver_public_keys:
                    if pk in public_key:
                        utxo = UTXO(tx.get_hash(), public_key,
                                    tx.messages[counter])
                        utxos.append(utxo)
                    counter = counter + 1
        return utxos

    def get_topmost_block(self):
        return self.blocks[len(self.blocks)-1]

    def is_valid_UTXO(self, UTXO):
        valid = False
        # blocks = self.read_from_blockchain()
        blocks = self.blocks
        #find possible UTXO on Blockchain
        for block in blocks:
            # for tx in block["transactions"]:
            for tx in block.transactions:
                if tx.get_hash() == UTXO.tx_hash:
                    counter = 0
                    for pk in tx.receiver_public_keys:
                        if pk in UTXO.public_key:
                            if UTXO.message == tx.messages[counter]:
                                valid = True
                        counter = counter + 1
        if valid == False:
            return False
        #check double_spending
        for block in blocks:
            for tx in block.transactions:
            # for tx in block["transactions"]:
                if isinstance(tx, Transaction):
                    for tx_utxo in tx.utxos:
                        if tx_utxo.get_hash() != UTXO.get_hash():
                            print("Breaks here")
                            return False
        return True

    def get_json(self):
        blocks = []
        for i in self.blocks:
            blocks.append(i.get_dict())
        return json.dumps({
            "blocks": blocks
        })

    def write_to_blockchain(self):
        with open("blockchain.json", "w") as save_file:
            save_file.write(self.get_json())

    def read_from_blockchain(self):
        with open("blockchain.json", "r") as save_file:
            if os.stat("blockchain.json").st_size != 0:
                blocks = json.load(save_file)
                return list(map(lambda x: {
                    "transaction_hashes": x["transaction_hashes"],
                    "hash_previous_block": x["hash_previous_block"],
                    "nonce": x["nonce"],
                    "transactions": self.serialize_transactions(x["transactions"] if "transactions" in x else []),
                }, blocks["blocks"]))
            return self.blocks

    def serialize_transactions(self, txs):
        if len(txs) < 1:
            return []
        genesis_tx = [Coinbase(txs[0]['receiver_public_keys'][0])]
        processed_txs = list(map(lambda x: Transaction(
                        utxos=list(map(lambda u: UTXO(
                            tx_hash=u["tx_hash"],
                            public_key=u["public_key"],
                            message=u["message"],
                        ),x["utxos"] if "utxos" in x else [])),
                        receiver_public_keys=x["receiver_public_keys"] if "receiver_public_keys" in x else [],
                        messages=x["messages"] if "messages" in x else [],
                        signature=x["signature"] if "signature" in x else "",
                    ), txs[1:]))
        return genesis_tx + processed_txs
