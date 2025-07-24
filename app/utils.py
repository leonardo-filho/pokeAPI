import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='app', level='INFO'):
    logger = logging.getLogger(name)

    # Evita duplicação de handlers ao recarregar módulos
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    # Cria pasta de logs se não existir
    os.makedirs('logs', exist_ok=True)

    # Define handler rotativo
    handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
