import flask
import logging
from flask import request
from multiprocessing import Process
from Blockchain import get_blockchain

from Wallet import Wallet
from Miner import Miner

app = flask.Flask(__name__)  

# @app.route('/mine', methods=['POST'])
# def mine():
#   if request.method == 'POST':
#     global p
#     wallet = Wallet()
#     p = Process(target=Miner, args=(wallet.public_key,))
#     p.start()
#     return "Mining"
#   return "Wrong HTTP method"

@app.route('/send', methods=['POST'])
def send():
  if request.method == 'POST':
    data = request.get_json(silent=True)
    try:
      wallet = Wallet()
      wallet.send_money([wallet.public_key], [data['amount']])
      return get_blockchain().get_topmost_block().get_dict()
    except Exception as e:
      print(e)
      return repr(e)
  return "Wrong HTTP method"

def init_server():
  logging.basicConfig(level=logging.INFO)
  logging.info("Team 4 Blockchain starting up")
  wallet = Wallet()
  global p
  p = Process(target=Miner, args=(wallet.public_key,))
  p.start()

if __name__ == '__main__':
  init_server()
  app.run(host='0.0.0.0', port=8100, threaded=True, debug=True, use_reloader=False)
  
  