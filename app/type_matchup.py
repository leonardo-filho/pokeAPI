def calcular_fraquezas_resistencias(types_list, api_client):
    """
    Calcula fraquezas, resistências e imunidades com base nos tipos fornecidos.

    Args:
        types_list (list): Exemplo: ["fire", "flying"]
        api_client (module): Módulo que contém a função get_type.

    Returns:
        dict: {"fraco": set(), "resistente": set(), "imune": set()}
    """
    result = {
        "fraco": set(),
        "resistente": set(),
        "imune": set()
    }

    for tipo in types_list:
        data = api_client.get_type(tipo)  # <<< função do módulo
        if "damage_relations" in data:
            dr = data["damage_relations"]
            result["fraco"].update([t["name"] for t in dr["double_damage_from"]])
            result["resistente"].update([t["name"] for t in dr["half_damage_from"]])
            result["imune"].update([t["name"] for t in dr["no_damage_from"]])

    # Corrige sobreposição (ex: fraco e resistente ao mesmo tempo)
    result["fraco"] -= result["resistente"] | result["imune"]
    result["resistente"] -= result["imune"]

    return result


TYPE_COLORS = {
    "normal": "#A8A77A",
    "fire": "#EE8130",
    "water": "#6390F0",
    "electric": "#F7D02C",
    "grass": "#7AC74C",
    "ice": "#96D9D6",
    "fighting": "#C22E28",
    "poison": "#A33EA1",
    "ground": "#E2BF65",
    "flying": "#A98FF3",
    "psychic": "#F95587",
    "bug": "#A6B91A",
    "rock": "#B6A136",
    "ghost": "#735797",
    "dragon": "#6F35FC",
    "dark": "#705746",
    "steel": "#B7B7CE",
    "fairy": "#D685AD",
}