import flask
import logging
import json
from flask import request, Response, render_template
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

@app.route('/')
def start():
  return render_template('base.html')

@app.route('/send', methods=['POST']) #DONE
def send():
  if request.method == 'POST':
    try:
      wallet = Wallet()
      public_key = request.args.get('receiver_public_key')
      print(public_key)
      wallet.send_money([public_key], [int(request.form['amount_to_send'])])
      result = json.dumps(get_blockchain().get_topmost_block().get_dict())
      #return Response(result, mimetype='text/json')

      return render_template('send.html',response = Response(result, mimetype='text/json'))
    except Exception as e:
      logging.error(e,exc_info=True)
      return repr(e)
  return "Wrong HTTP method"

@app.route('/block', methods=['GET']) #DONE -> Add a button for block explorer
def getBlocks():
  if request.method == 'GET':
    try:
      response = get_blockchain().get_blockhashes_json()
      return render_template('BlockExplorer.html', returned_blockhashes=response)
    except Exception as e:
      logging.error(e,exc_info=True)
      return repr(e)
  return "Wrong HTTP method"

@app.route('/blockhashsearch', methods=['GET']) # DONE
def getBlock():
  if request.method == 'GET':
    try:
      blockhash = request.args.get('blockhash')
      block = get_blockchain().get_block_by_hash(blockhash)
      if block == None:
        return repr("Error: No block found with this hash")
      else:
        return render_template('blocksearch.html',response = json.dumps(block.get_dict()), mimetype='text/json')
    except Exception as e:
      logging.error(e,exc_info=True)
      return repr(e)
  return "Wrong HTTP method"

@app.route('/transaction_search_from_blockhash', methods=['GET']) #DONE
def getTxs():
  if request.method == 'GET':
    try:
      blockhash = request.args.get('blockhash')
      block = get_blockchain().get_block_by_hash(blockhash)
      if block == None:
        return repr("Error: No block found with this hash")
      else:
        return Response(json.dumps(block.get_transactions()), mimetype='text/json')
    except Exception as e:
      logging.error(e,exc_info=True)
      return repr(e)
  return "Wrong HTTP method"

@app.route('/blocktxsearch', methods=['GET']) #DONE
def getTx():
  if request.method == 'GET':
    try:
      blockhash = request.args.get('blockhash')
      txhash = request.args.get('txhash')
      block = get_blockchain().get_block_by_hash(blockhash)
      if block == None:
        return render_template('blocksearch.html',response = repr("Error: No block found with this hash"))
      else:
        tx = block.get_tx_by_hash(txhash)
        if tx == None:
          return repr("Error: No tx found with this hash")
        else:
          return render_template('blocksearch.html', response = json.dumps(tx.get_dict()), mimetype='text/json')
    except Exception as e:
      logging.error(e,exc_info=True)
      return repr(e)
  return "Wrong HTTP method"


@app.route('/balance', methods=['POST']) #DONE
def get_balance():
  try:
    logging.info('HERE')
    public_key = request.form.get("public_key_input")
    print(public_key)
    balance = 0
    with open("blockchain.json", "r") as save_file:    
      data = json.load(save_file)
      print(len(data["blocks"]))

      for block in data["blocks"]:
        for transaction in block['transactions']:
          for utxo in transaction['utxos']:
            if public_key in utxo['public_key']:
              balance += utxo['message']
      if balance ==0:
        return render_template('balance.html',bal="You have no balance")
      else:
        return render_template('balance.html', bal=balance)

  except: raise Exception('The blockchain does not exsist yet')




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
  


  