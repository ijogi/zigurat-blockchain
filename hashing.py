import hashlib, codecs

def hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def string_to_hex(string):
    return codecs.encode(string.encode('utf-8'), 'hex_codec').decode()