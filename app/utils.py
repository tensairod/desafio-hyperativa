from hashlib import sha256

from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def generate_hash(value):
    return sha256(value.encode()).hexdigest()


def generate_aes_key():
    return get_random_bytes(16)  # 16 bytes = 128 bits key size


def decrypt_data(encrypted_data):
    if isinstance(encrypted_data, str):
        encrypted_data = encrypted_data.encode()
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
        return private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()


def encrypt_data(data: bytes):
    if isinstance(data, str):
        data = data.encode()
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
