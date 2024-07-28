from cryptography.fernet import Fernet

from app.models import Card


def get_card_by_number(fernet_key: bytes, number: str):
    fernet = Fernet(fernet_key)

    # Criptografar o número do cartão fornecido
    encrypted_card_number = fernet.encrypt(number.encode())

    # Buscar no banco de dados
    return Card.query.filter_by(get_number=encrypted_card_number).first()
