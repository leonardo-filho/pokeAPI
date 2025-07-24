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

def format_pokemon_name(name: str) -> str:
    """
    Formata nomes como 'charizard-mega-y' para 'Charizard Mega Y'
    """
    return name.replace("-", " ").title()

# utils.py (complemento no final do arquivo)

import requests

def get_all_pokemon_names():
    """
    Retorna uma lista com todos os nomes de Pokémon da PokéAPI, ordenados.
    """
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
    response = requests.get(url).json()
    return sorted([p["name"] for p in response["results"]])
