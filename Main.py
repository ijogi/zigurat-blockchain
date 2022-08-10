import time
from Blockchain import get_blockchain
from Wallet import Wallet
from Miner import Miner
from multiprocessing import Process

wallet = Wallet()
wallet.send_money([wallet.public_key], [10])
wallet.send_money([wallet.public_key], [5])
wallet.send_money([wallet.public_key], [5])
wallet.send_money([wallet.public_key], [10])
wallet.send_money([wallet.public_key], [20])
wallet.send_money([wallet.public_key], [10])
print(get_blockchain().blocks)



# print(wallet.send_money([wallet.public_key], [10]))
# miner = Miner(wallet.public_key)
# print("Hell0")


if __name__ == '__main__':
    p = Process(target=Miner, args=(wallet.public_key,))
    p.start()
    p.join()
