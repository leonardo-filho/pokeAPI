import requests
from app.config import Config
from app.utils import setup_logger

logger = setup_logger(level=Config.LOG_LEVEL)

class PokeAPIClient:
    def __init__(self):
        """Inicializa o cliente com a URL base da PokéAPI."""
        self.base_url = Config.API_URL

    def _get(self, path, params=None):
        """Faz uma requisição GET segura à PokéAPI."""
        url = f"{self.base_url}/{path}"
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            logger.info(f"GET {url} → {response.status_code}")
            return response.json()
        except requests.RequestException as e:
            logger.exception(f"Erro ao acessar '{url}': {e}")
            return {"erro": str(e)}

    def get_pokemon(self, name_or_id):
        """Retorna dados básicos de um Pokémon pelo nome ou ID."""
        return self._get(f"pokemon/{name_or_id}")

    def get_type(self, type_name):
        """Retorna dados de um tipo de Pokémon (para calcular fraquezas)."""
        return self._get(f"type/{type_name}")

    def get_species(self, name_or_id):
        """Retorna dados da espécie do Pokémon (usado para obter a linha evolutiva)."""
        return self._get(f"pokemon-species/{name_or_id}")

    def get_evolution_chain(self, evo_id):
        """Retorna a cadeia evolutiva de um Pokémon."""
        return self._get(f"evolution-chain/{evo_id}")