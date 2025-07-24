def calcular_efetividades(types_list, client):
    result = {
        "fraco": set(),
        "resistente": set(),
        "imune": set()
    }

    for tipo in types_list:
        data = client.get_type(tipo)
        if "damage_relations" in data:
            dr = data["damage_relations"]
            result["fraco"].update([d["name"] for d in dr["double_damage_from"]])
            result["resistente"].update([d["name"] for d in dr["half_damage_from"]])
            result["imune"].update([d["name"] for d in dr["no_damage_from"]])

    # Remove sobreposições
    result["fraco"] -= result["resistente"]
    result["fraco"] -= result["imune"]
    result["resistente"] -= result["imune"]

    return result
