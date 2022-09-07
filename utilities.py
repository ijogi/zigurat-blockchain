from Transaction import Coinbase, Transaction, UnsignedTransaction
from UTXO import UTXO


def serialize_utxo(utxo):
  return UTXO(
      tx_hash=utxo["tx_hash"],
      public_key=utxo["public_key"],
      message=utxo["message"],
  )

def serialize_transaction(tx):
    if "utxos" in tx:
        if "signature" in tx:
            return Transaction(
                utxos=list(map(lambda u: serialize_utxo(u), tx["utxos"] if "utxos" in tx else [])),
                receiver_public_keys=tx["receiver_public_keys"] if "receiver_public_keys" in tx else [],
                messages=tx["messages"] if "messages" in tx else [],
                signature=tx["signature"] if "signature" in tx else "",
            )
        else:
            return UnsignedTransaction(
                    utxos=list(map(lambda u: serialize_utxo(u), tx["utxos"] if "utxos" in tx else [])),
                    receiver_public_keys=tx["receiver_public_keys"] if "receiver_public_keys" in tx else [],
                    messages=tx["messages"] if "messages" in tx else [],
            )

    return Coinbase(receiver=tx["receiver_public_keys"][0])

def serialize_transactions(txs):
    if len(txs) < 1:
        return []
    return list(map(lambda x: serialize_transaction(x), txs))