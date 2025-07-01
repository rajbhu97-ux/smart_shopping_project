import bcrypt 
from dataclasses import dataclass

def encode_password(password):
    return password.encode('utf-8')

def hash_password(raw_password):
    return bcrypt.hashpw(encode_password(raw_password), bcrypt.gensalt()).decode("utf-8")

def check_password(raw_password, hashed):
    return bcrypt.checkpw(encode_password(raw_password), hashed_password=encode_password(hashed))

@dataclass
class OrderStatus:
    in_progress = "INPROGRESS"
    completed = "COMPLETED"
    failed = "FAILED"