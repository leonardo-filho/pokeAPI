import requests

BASE_URL = "https://pokeapi.co/api/v2"

def get_pokemon_data(name):
    if name == "all":
        return get_all_pokemon_names()
    response = requests.get(f"{BASE_URL}/pokemon/{name.lower()}")
    response.raise_for_status()
    return response.json()

def get_pokemon_species(name):
    response = requests.get(f"{BASE_URL}/pokemon-species/{name.lower()}")
    response.raise_for_status()
    return response.json()

def get_evolution_chain(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_all_pokemon_names():
    url = f"{BASE_URL}/pokemon?limit=100000&offset=0"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    names = [entry["name"] for entry in data["results"]]
    return names
