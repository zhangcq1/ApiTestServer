import hashlib
import base64
from Crypto.Cipher import AES

class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def decrypt_string(self, enc):
        enc = base64.b64decode(enc)
        return self.decrypt(enc).decode('utf8')

    def encrypt(self, data):
        data = AESCipher.str_to_bytes(data)
        cipher = AES.new(self.key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(AESCipher.pad(data))
        return base64.b64encode(cipher.iv + ciphertext).decode('utf8')

    @staticmethod
    def pad(s):
        padding_len = AES.block_size - len(s) % AES.block_size
        padding = chr(padding_len) * padding_len
        return s + padding.encode('utf8')