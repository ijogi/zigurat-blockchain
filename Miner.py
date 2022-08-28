import hashing
import time
import logging
from Mempool import get_mempool
from Block import Block
from Blockchain import get_blockchain
from Transaction import Coinbase, Transaction
import random
from CONFIG import *

class Miner:
    def __init__(self, own_public_key):
        self.log = logging.getLogger("Miner")
        self.log.info("🔥 starting up 🔥")
        self.log.info("Throttle=%s",throttle)
        self.log.info("Mining Target=%s",mining_target)
        self.public_key = own_public_key
        while True:
            self.mine()
            time.sleep(throttle)

    def check_agains_target(self, hash_string):
        hex = hashing.string_to_hex(hash_string)
        for i in range(1, mining_target+1):
            if not hex[i] == "0":
                return False
        return True

    def mine(self): 
        mempool = get_mempool()
        txs = mempool.tx
        if len(txs) > 0:
            topmost_block = get_blockchain().get_topmost_block()
            assert isinstance(topmost_block, Block)
            hash_prev = topmost_block.get_hash()
            for i in txs:
                assert isinstance(i, Transaction) or isinstance(i, Coinbase)
                if not i.is_valid():
                    self.log.warning("Miner: Removed invalid transaction. TX=%s",i.get_hash())
                    txs.remove(i)
            
            coinbase = Coinbase(self.public_key)
            if coinbase.get_hash() not in list(map(lambda x: x.get_hash(), txs)):
                txs.insert(0, coinbase)
        
            nonce = random.randint(0, 9999999999999999999999999999)
            block = Block(hash_prev, txs, nonce)
            hash = block.get_hash()
            check = self.check_agains_target(hash)
            
            if check:
                #FOUND NEW BLOCK; COINBASE$$$$
                self.log.info("Found new Block")
                success = get_blockchain().insert_block(block)
                if success:
                    self.log.info("Block with %s tx successfully inserted", len(txs))
                    for i,tx in enumerate(txs):
                        self.log.info("TX[%s]: Hash=%s, Messages=%s", i,tx.get_hash(),tx.messages)
                    mempool.clear_n_transactions(len(txs))
                    self.log.debug("Blockchain dump: %s", get_blockchain().get_json())


