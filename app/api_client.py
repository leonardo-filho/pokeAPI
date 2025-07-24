import requests
from app.utils import setup_logger

BASE_URL = "https://pokeapi.co/api/v2"
logger = setup_logger()

def get_pokemon_data(name):
    """Retorna os dados detalhados de um Pokémon"""
    if name == "all":
        return get_all_pokemon_names()

    try:
        response = requests.get(f"{BASE_URL}/pokemon/{name.lower()}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar dados do Pokémon '{name}': {e}")
        return {}

def get_pokemon_species(name):
    """Retorna dados da espécie do Pokémon (para linha evolutiva)"""
    try:
        response = requests.get(f"{BASE_URL}/pokemon-species/{name.lower()}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar species do Pokémon '{name}': {e}")
        return {}

def get_evolution_chain(url):
    """Consulta a cadeia evolutiva completa a partir da URL da species"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar cadeia evolutiva: {e}")
        return {}

def get_all_pokemon_names():
    """Retorna todos os nomes de Pokémon disponíveis na PokéAPI"""
    url = f"{BASE_URL}/pokemon?limit=100000&offset=0"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [entry["name"] for entry in data["results"]]
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar todos os Pokémon: {e}")
        return []

def get_type(type_name):
    """Retorna os dados de um tipo específico (ex: 'electric', 'fire')"""
    try:
        response = requests.get(f"{BASE_URL}/type/{type_name.lower()}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar dados do tipo '{type_name}': {e}")
        return {}
