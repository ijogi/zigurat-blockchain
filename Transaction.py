import crypto
import hashing
from UTXO import UTXO
import json

class Coinbase:
    def __init__(self, receiver):
        self.receiver_public_keys = [receiver]
        self.messages = [50]
        self.type = 'coinbase'

    def get_hash(self):
        return hashing.hash(self.get_json())

    def is_valid(self):
        return True

    def get_dict(self):
        data = {
            "receiver_public_keys": self.receiver_public_keys,
            "messages": self.messages
        }
        return data

    def get_json(self):
        return json.dumps(self.get_dict())

class UnsignedTransaction(Coinbase):
    def __init__(self, utxos, receiver_public_keys, messages):
        assert isinstance(receiver_public_keys, list)
        assert isinstance(messages, list)
        assert len(receiver_public_keys) == len(messages)
        assert len(receiver_public_keys) > 0
        assert isinstance(utxos, list)
        assert len(utxos) > 0
        for i in utxos:
            assert isinstance(i, UTXO)
            assert i.public_key == utxos[0].public_key
        self.utxos = utxos
        self.receiver_public_keys = receiver_public_keys
        self.messages = messages
        self.type = 'unsignedtx'

    def get_dict(self):
        utxos_json = []
        for i in self.utxos:
            utxos_json.append(i.get_dict())
        data = {
            "utxos": utxos_json,
            "receiver_public_keys": self.receiver_public_keys,
            "messages": self.messages,
        }
        return data

    def sign(self, priv_key, password):
        return crypto.sign(priv_key, password, self.get_hash())

class Transaction(UnsignedTransaction):
    def __init__(self, utxos, receiver_public_keys, messages, signature):
        assert isinstance(receiver_public_keys, list)
        assert isinstance(messages, list)
        assert len(receiver_public_keys) == len(messages)
        assert len(receiver_public_keys) > 0
        assert isinstance(utxos, list)
        assert len(utxos) > 0
        for i in utxos:
            assert isinstance(i, UTXO)
            assert i.public_key == utxos[0].public_key
        UnsignedTransaction.__init__(self, utxos, receiver_public_keys, messages)
        self.signature = signature
        self.type = 'transaction'
        assert self.is_valid()

    def get_dict(self):
        utxos_json = []
        for i in self.utxos:
            utxos_json.append(i.get_dict())
        data = {
            "utxos": utxos_json,
            "receiver_public_keys": self.receiver_public_keys,
            "messages": self.messages,
        }
        return data

    def is_valid(self):
        signature_valid = crypto.verify(self.utxos[0].public_key, self.signature, self.get_hash())
        spent = 0
        for msg in self.messages:
            spent = spent+msg
        balance = 0
        for utxo in self.utxos:
            balance = balance + utxo.message
        amount_enough = balance >= spent
        return signature_valid and amount_enough
