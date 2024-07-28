import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    # Cria a pasta de logs se não existir
    log_dir = 'log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configuração do logger
    log_file_path = os.path.join(log_dir, 'log.txt')
    log_handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=1)
    log_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    return logger
