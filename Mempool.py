import json
import os
from Transaction import Transaction
from UTXO import UTXO

the_mempool = None


def get_mempool():
    global the_mempool
    if the_mempool == None:
        the_mempool = Mempool()
    the_mempool.tx = the_mempool.get_mempool_txs()
    return the_mempool


class Mempool:
    def __init__(self):
        self.tx = []
        self.write_to_mempool()

    def insert_transaction(self, tx):
        assert isinstance(tx, Transaction)
        assert tx.is_valid()
        self.tx.append(tx)
        self.write_to_mempool()

    def clear_n_transactions(self, n):
        for i in range(n):
            if len(self.tx) > 0:
                self.tx.pop(0)
                self.write_to_mempool()
                self.tx = self.get_mempool_txs()

    def write_to_mempool(self):
        with open("mempool.json", "w") as save_file:
            if len(self.tx) > 0:
                save_file.write(json.dumps({
                    "txs": list(map(lambda x: x.get_full_dict(), self.tx)),
                }))

    def get_mempool_txs(self):
        with open("mempool.json", "r") as save_file:
            if os.stat("mempool.json").st_size != 0:
                mempool = json.load(save_file)
                return list(map(lambda x: Transaction(
                    utxos=list(map(lambda u: UTXO(u["tx_hash"], u["public_key"], u["message"]), x["utxos"])),
                    receiver_public_keys=x["receiver_public_keys"],
                    messages=x["messages"],
                    signature=x["signature"],
                ), mempool["txs"]))
            return []
