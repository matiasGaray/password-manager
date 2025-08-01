from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def cipher_pass(password, key):
    b_pass = password.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(b_pass, AES.block_size))
    ct = b64encode(ct_bytes).decode('utf-8')
    iv = b64encode(cipher.iv).decode('utf-8')
    return (ct, iv)

def decipher_pass(ct_encoded, iv_encoded, key):
    try:
        ct = b64decode(ct_encoded)
        iv = b64decode(iv_encoded)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    
    except (ValueError, KeyError):
        print("Hubo un error desencriptando")





