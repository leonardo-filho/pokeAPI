# app/i18n.py

TRANSLATIONS = {
    "pt": {
        "pagina_consulta": "Consulta Pokémon",
        "pagina_evolucao": "Evoluções",
        "idioma": "🌐 Idioma",
        "menu": "📂 Menu",
        "bem_vindo": "📺 Bem-vindo",
        "nome_base": "Nome base do Pokémon",
        "selecione_variacao": "Selecione a variação",
        "buscar": "🔴 Buscar",
        "tipos": "Tipos",
        "fraquezas": "⚡ Fraquezas",
        "resistencias": "🛡️ Resistências",
        "imunidades": "🌀 Imunidades",
    },
    "en": {
        "pagina_consulta": "Pokémon Search",
        "pagina_evolucao": "Evolution",
        "idioma": "🌐 Language",
        "menu": "📂 Menu",
        "bem_vindo": "📺 Welcome",
        "nome_base": "Base name of the Pokémon",
        "selecione_variacao": "Select variation",
        "buscar": "🔴 Search",
        "tipos": "Types",
        "fraquezas": "⚡ Weaknesses",
        "resistencias": "🛡️ Resistances",
        "imunidades": "🌀 Immunities",
    }
}

def t(key: str, lang: str = "pt") -> str:
    return TRANSLATIONS.get(lang, {}).get(key, key)
