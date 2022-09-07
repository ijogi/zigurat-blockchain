import flask
import logging
import json
from flask import request, Response
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
      result = json.dumps(get_blockchain().get_topmost_block().get_dict())
      return Response(result, mimetype='text/json')
    except Exception as e:
      logging.error(e,exc_info=True)
      return repr(e)
  return "Wrong HTTP method"

@app.route('/block', methods=['GET'])
def getBlocks():
  if request.method == 'GET':
    try:
      return Response(get_blockchain().get_blockhashes_json(), mimetype='text/json')
    except Exception as e:
      logging.error(e,exc_info=True)
      return repr(e)
  return "Wrong HTTP method"

@app.route('/block/<blockhash>', methods=['GET'])
def getBlock(blockhash):
  if request.method == 'GET':
    try:
      block = get_blockchain().get_block_by_hash(blockhash)
      if block == None:
        return repr("Error: No block found with this hash")
      else:
        return Response(json.dumps(block.get_dict()), mimetype='text/json')
    except Exception as e:
      logging.error(e,exc_info=True)
      return repr(e)
  return "Wrong HTTP method"

@app.route('/block/<blockhash>/tx', methods=['GET'])
def getTxs(blockhash):
  if request.method == 'GET':
    try:
      block = get_blockchain().get_block_by_hash(blockhash)
      if block == None:
        return repr("Error: No block found with this hash")
      else:
        return Response(json.dumps(block.get_transactions()), mimetype='text/json')
    except Exception as e:
      logging.error(e,exc_info=True)
      return repr(e)
  return "Wrong HTTP method"

@app.route('/block/<blockhash>/tx/<txhash>', methods=['GET'])
def getTx(blockhash,txhash):
  if request.method == 'GET':
    try:
      block = get_blockchain().get_block_by_hash(blockhash)
      if block == None:
        return repr("Error: No block found with this hash")
      else:
        tx = block.get_tx_by_hash(txhash)
        if tx == None:
          return repr("Error: No tx found with this hash")
        else:
          return Response(json.dumps(tx.get_dict()), mimetype='text/json')
    except Exception as e:
      logging.error(e,exc_info=True)
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
  
  