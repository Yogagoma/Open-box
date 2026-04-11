import hashlib

def sha256_hash(data:str) -> str:


    if not isinstance(data, str):
        raise TypeError("Input must be a string.")
    
    # Encode string to bytes, then hash
    hash_object = hashlib.sha256(data.encode('utf-8'))
    return hash_object.hexdigest()
