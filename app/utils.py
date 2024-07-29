from hashlib import sha256

from Crypto.Random import get_random_bytes


def generate_hash(value):
    return sha256(value.encode()).hexdigest()


def generate_aes_key():
    return get_random_bytes(16)  # 16 bytes = 128 bits key size