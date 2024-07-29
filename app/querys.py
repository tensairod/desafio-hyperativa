import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from app.models import Card


def get_card_by_number(aes_key, number):
    aes_key = base64.b64decode(aes_key)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=b'\x00' * AES.block_size)
    ct_bytes = cipher.encrypt(pad(number.encode(), AES.block_size))
    iv = cipher.iv
    encrypted_number = iv + ct_bytes
    return Card.query.filter_by(_number=encrypted_number).first()
