import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _number = db.Column(db.LargeBinary, unique=True, nullable=False)

    def __init__(self, number, aes_key):
        aes_key = base64.b64decode(aes_key)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv=b'\x00' * AES.block_size)
        ct_bytes = cipher.encrypt(pad(number.encode(), AES.block_size))
        iv = cipher.iv
        self._number = iv + ct_bytes

    def get_number(self, aes_key):
        aes_key = base64.b64decode(aes_key)
        iv = self._number[:AES.block_size]
        ct = self._number[AES.block_size:]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ct), AES.block_size)
        return decrypted_data.decode()