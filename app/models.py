from . import db
from cryptography.fernet import Fernet


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _number = db.Column(db.LargeBinary, unique=True, nullable=False)  # Alterado para LargeBinary

    def __init__(self, number, fernet_key):
        fernet = Fernet(fernet_key)
        self._number = fernet.encrypt(number.encode())  # Criptografar e armazenar como bytes

    def get_number(self, fernet_key):
        fernet = Fernet(fernet_key)
        return fernet.decrypt(self._number).decode()  # Descriptografar e retornar como string
