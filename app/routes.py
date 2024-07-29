from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Card
import os

from app.querys import get_card_by_number
from logging_config import setup_logging

bp = Blueprint('routes', __name__)
logger = setup_logging()


@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        logger.info(f"Dados da requisicao de registrar usuario: {data['username']}")

        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], password_hash=hashed_password)
        logger.info("Usuario criado, adicionando no banco de dados...")
        db.session.add(new_user)
        db.session.commit()
        logger.info("Usuario adicionado no banco com sucesso")
        return jsonify({"message": "User registered successfully"}), 201
    except Exception:  # noqa
        logger.exception("Excecao ao registrar usuario")


@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logger.info(f"Tentando logar com o usuario: {data}")
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            logger.info(f"Usuario {user.username} encontrado! Criando token de acesso")
            access_token = create_access_token(identity={'username': user.username})
            logger.info(f"Token gerado: {access_token}")
            return jsonify(access_token=access_token), 200
        logger.error(f"Credenciais do usuario {data['username']} estao incorretas")
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception:  # noqa
        logger.exception("Excecao nao mapeada ao tentar logar com o usuario")


@bp.route('/cards', methods=['POST'])
@jwt_required()
def add_card():
    try:
        data = request.get_json()
        logger.debug(f"dados da requisicao de adicionar cartao {data}")
        aes_key = os.environ.get('AES_KEY').encode()
        number = data['number']

        if not isinstance(number, str) or not number.strip():
            logger.error("Numero de cartao invalido")
            return jsonify({"message": "Invalid card number"}), 400

        existing_card = get_card_by_number(aes_key, number)
        if existing_card:
            logger.warning(f'Ja existe um cartao com esse numero: {number}')
            return jsonify({"message": "Card already exists"}), 400

        new_card = Card(number=number, aes_key=aes_key)
        logger.info("Cartao criado, enviando para o banco de dados")
        db.session.add(new_card)
        db.session.commit()
        logger.info("Cartao adicionado no banco com sucesso")
        return jsonify({"message": "Card added successfully"}), 201
    except Exception:  # noqa
        logger.exception("Excecao nao mapeada ao tentar adicionar cartao")


@bp.route('/cards/upload', methods=['POST'])
@jwt_required()
def upload_cards():
    try:
        file = request.files.get('file')

        if file is None:
            logger.error("Nenhum arquivo foi upado")
            return jsonify({"message": "No file uploaded"}), 400

        logger.info(f"Lendo o arquivo {file.filename}...")

        if not file.filename.endswith('.txt'):
            logger.error("Tipo de arquivo nao é suportado")
            return jsonify({"message": "Unsupported file type"}), 400

        aes_key = os.environ.get('AES_KEY')
        try:
            file_content = file.stream.read().decode('utf-8')
        except Exception:  # noqa
            logger.exception("Excecao nao mapeada ao tentar ler arquivo")
            return jsonify({"message": f"Error reading file"}), 500

        lines = file_content.splitlines()
        logger.info("Passando linha por linha...")
        for line in lines:
            line = line.strip()

            if line.startswith('C'):
                logger.info("Linha com numeros encontrada, extraindo numero do cartao...")
                card_number = line[7:23].strip()

                logger.info(f"Numero encontrado: {card_number}")

                if len(card_number) != 16:
                    logger.info(f"Numero de cartao nao esta no padrao correto: {card_number}")
                    continue
                existing_card = get_card_by_number(aes_key, card_number)
                if existing_card is None:
                    new_card = Card(number=card_number, aes_key=aes_key)
                    db.session.add(new_card)
                    logger.info("Cartao adicionado!")
                else:
                    logger.warning(f"Cartao {card_number} ja existe")

        db.session.commit()
        logger.info(f"Cartoes adicionados no banco de dados!")
        return jsonify({"message": "Cards added successfully"}), 201
    except Exception:  # noqa
        logger.exception("Excecao nao mapeada ao tentar adicionar cartoes via arquivo")


@bp.route('/cards/<number>', methods=['GET'])
@jwt_required()
def get_card(number):
    try:
        logger.info(f"Buscando cartao {number}")
        aes_key = os.environ.get('AES_KEY').encode()
        card = get_card_by_number(aes_key, number)

        if card:
            logger.info(f'Cartao encontrado: {number}')
            return jsonify({"card_id": card.id, "card_number": number}), 200
        else:
            logger.warning(f'Cartao nao encontrado: {number}')
            return jsonify({"message": "Card not found"}), 404
    except Exception:  # noqa
        logger.exception("Excecao nao mapeada ao tentar buscar cartao")
