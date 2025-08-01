import os
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

def generate_key(password):
    b_pass = password.encode('utf-8')
    salt = os.urandom(16)
    kdf = Argon2id(salt=salt,
                   length=32,
                   iterations=1,
                   lanes=4,
                   memory_cost=64*1024,
                   ad=None,
                   secret=None
                   )
    key = kdf.derive(b_pass)
    return (key,salt)

def regenerate_key(password, salt):
    b_pass = password.encode('utf-8')
    kdf = Argon2id(salt=salt,
                   length=32,
                   iterations=1,
                   lanes=4,
                   memory_cost=64*1024,
                   ad=None,
                   secret=None
                   )
    key = kdf.derive(b_pass)
    return key

