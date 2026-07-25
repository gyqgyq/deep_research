import hashlib

def string2hash(string: str) -> str:
    return hashlib.sha256(string.encode("utf-8")).hexdigest()