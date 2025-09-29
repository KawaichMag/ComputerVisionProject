from datetime import datetime
import hashlib


def photo_hashed_name(username: str, format:str = "jpg") -> str:
    hash_input = f"{username}_{datetime.now()}"
    hash_output =  hashlib.sha256(hash_input.encode())
    return f"{hash_output.hexdigest()}.{format}"
    