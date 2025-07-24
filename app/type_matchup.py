def calcular_fraquezas_resistencias(types_list, client):
    """
    Calcula fraquezas, resistências e imunidades com base nos tipos fornecidos.

    Args:
        types_list (list): Exemplo: ["fire", "flying"]
        client (PokeAPIClient): Instância do cliente da PokéAPI.

    Returns:
        dict: {"fraco": set(), "resistente": set(), "imune": set()}
    """
    result = {
        "fraco": set(),
        "resistente": set(),
        "imune": set()
    }

    for tipo in types_list:
        data = client.get_type(tipo)
        if "damage_relations" in data:
            dr = data["damage_relations"]
            result["fraco"].update([t["name"] for t in dr["double_damage_from"]])
            result["resistente"].update([t["name"] for t in dr["half_damage_from"]])
            result["imune"].update([t["name"] for t in dr["no_damage_from"]])

    result["fraco"] -= result["resistente"] | result["imune"]
    result["resistente"] -= result["imune"]

    return result
