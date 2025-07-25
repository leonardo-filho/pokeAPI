import streamlit as st
from app import api_client
from app.type_matchup import calcular_fraquezas_resistencias, calcular_forte_contra
from app.utils import format_pokemon_name

# Traduções e cores
TIPO_TRADUZIDO = {
    "normal": "normal", "fire": "fogo", "water": "água", "electric": "elétrico", "grass": "planta",
    "ice": "gelo", "fighting": "lutador", "poison": "veneno", "ground": "terra", "flying": "voador",
    "psychic": "psíquico", "bug": "inseto", "rock": "pedra", "ghost": "fantasma", "dragon": "dragão",
    "dark": "noturno", "steel": "aço", "fairy": "fada"
}

CORES_TIPOS = {
    "normal": "#A8A878", "fire": "#F08030", "water": "#6890F0", "electric": "#F8D030", "grass": "#78C850",
    "ice": "#98D8D8", "fighting": "#C03028", "poison": "#A040A0", "ground": "#E0C068", "flying": "#A890F0",
    "psychic": "#F85888", "bug": "#A8B820", "rock": "#B8A038", "ghost": "#705898", "dragon": "#7038F8",
    "dark": "#705848", "steel": "#B8B8D0", "fairy": "#EE99AC"
}

def traduzir_tipos(tipos, lang):
    return [TIPO_TRADUZIDO.get(t, t) for t in tipos] if lang == "pt" else tipos

def render_tipo_badge(nome_tipo, lang):
    tipo_en = nome_tipo if lang == "en" else next((k for k, v in TIPO_TRADUZIDO.items() if v == nome_tipo), nome_tipo)
    cor = CORES_TIPOS.get(tipo_en, "#999")
    return f"<span style='background-color: {cor}; color: black; padding: 6px 12px; margin: 3px; border-radius: 10px; display: inline-block;'>{nome_tipo}</span>"

def mostrar(lang):
    titulo = "🔍 Consulta de Pokémon" if lang == "pt" else "🔍 Pokémon Search"
    st.markdown(f"<h1 style='color:#F5F5F5'>{titulo}</h1>", unsafe_allow_html=True)

    nomes_full = api_client.get_all_pokemon_names()
    nomes_base = sorted(set([name.split("-")[0] for name in nomes_full]))

    nome_base = st.selectbox("Nome base do Pokémon" if lang == "pt" else "Base Pokémon name", options=nomes_base, index=None, placeholder="Ex: charizard")

    if nome_base:
        variations = sorted([n for n in nomes_full if n.startswith(nome_base)])
        variacao = st.selectbox("Selecione a variação" if lang == "pt" else "Select variation", options=variations)

        if st.button("🔴 Buscar" if lang == "pt" else "🔴 Search"):
            data = api_client.get_pokemon_data(variacao)
            if "name" not in data:
                st.error("Pokémon não encontrado." if lang == "pt" else "Pokémon not found.")
                return

            tipos_en = [t["type"]["name"] for t in data["types"]]
            tipos_traduzidos = traduzir_tipos(tipos_en, lang)
            img_url = data["sprites"]["front_default"]

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown(f"""
                <div style="background-color: #1f1f1f; padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 0 15px #111; max-width: 350px; margin: auto;">
                    <img src="{img_url}" width="160">
                    <p style="margin-top: 12px;"><strong style="color:white;">Tipos:</strong></p>
                    {"".join([render_tipo_badge(tt, lang) for tt in tipos_traduzidos])}
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            efetividades = calcular_fraquezas_resistencias(tipos_en, api_client)
            forte_contra = calcular_forte_contra(tipos_en, api_client)

            efetividades = {k: traduzir_tipos(v, lang) for k, v in efetividades.items()}
            forte_contra = traduzir_tipos(forte_contra, lang)

            # Novo cálculo: tipos que esse Pokémon não causa dano
            nao_causa_dano = set()
            for tipo in tipos_en:
                tipo_data = api_client.get_type(tipo)
                if "damage_relations" in tipo_data:
                    nao_causa_dano.update([t["name"] for t in tipo_data["damage_relations"]["no_damage_to"]])
            nao_causa_dano = traduzir_tipos(nao_causa_dano, lang)

            def render_card(lista, titulo, emoji):
                if not lista:
                    return f"""
                        <div style="background-color: #2e2e2e; padding: 20px; border-radius: 10px; margin-top: 20px;">
                            <h5 style="color: white;">{emoji} {titulo}</h5>
                            <p style="color: #aaa; margin-top: 10px;">(Não tem)</p>
                        </div>
                    """
                return f"""
                    <div style="background-color: #2e2e2e; padding: 20px; border-radius: 10px; margin-top: 20px;">
                        <h5 style="color: white;">{emoji} {titulo}</h5>
                        <div style="margin-top: 10px;">
                            {"".join([render_tipo_badge(t, lang) for t in lista])}
                        </div>
                    </div>
                """

            # Linha 1
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(render_card(efetividades["fraco"], "Fraquezas" if lang == "pt" else "Weaknesses", "⚡"), unsafe_allow_html=True)
            with col2:
                st.markdown(render_card(efetividades["resistente"], "Resistências" if lang == "pt" else "Resistances", "🛡️"), unsafe_allow_html=True)

            # Linha 2
            col3, col4 = st.columns(2)
            with col3:
                st.markdown(render_card(efetividades["imune"], "Imune" if lang == "pt" else "Immunities", "🚫"), unsafe_allow_html=True)
            with col4:
                st.markdown(render_card(forte_contra, "É forte contra" if lang == "pt" else "Strong Against", "🔥"), unsafe_allow_html=True)

            # Linha 3 – Nova seção
            col5, col6 = st.columns(2)
            with col5:
                st.markdown(render_card(nao_causa_dano, "Não causa dano em" if lang == "pt" else "Doesn't affect", "🔇"), unsafe_allow_html=True)
