import streamlit as st
from app.api_client import get_pokemon_data, get_pokemon_species, get_evolution_chain
from app.utils import format_pokemon_name
from app.config import PRIMARY_COLOR

def mostrar():
    st.markdown(f"<h1 style='color:{PRIMARY_COLOR}'>🔁 Evolução de Pokémon</h1>", unsafe_allow_html=True)

    # Autocomplete com todos os nomes de Pokémon base
    if "pokemon_list" not in st.session_state:
        st.session_state.pokemon_list = get_pokemon_data("all")  # implementa essa função para retornar lista simples de nomes

    base_name = st.selectbox("Nome base do Pokémon", st.session_state.pokemon_list, index=0)

    if st.button("🔍 Buscar"):
        try:
            species_data = get_pokemon_species(base_name)
            evo_chain_url = species_data["evolution_chain"]["url"]
            evolution_chain = get_evolution_chain(evo_chain_url)

            # Renderizar cadeia evolutiva
            st.markdown("---")
            st.markdown("### 🧬 Linha Evolutiva")
            render_chain(evolution_chain)

        except Exception as e:
            st.error(f"Erro ao buscar evolução: {e}")

def render_chain(chain_data):
    def render_stage(pokemon):
        name = pokemon["name"]
        img_url = get_pokemon_data(name)["sprites"]["front_default"]

        with st.container():
            st.image(img_url, width=120)
            st.markdown(f"<h4 style='text-align:center;color:white'>{format_pokemon_name(name)}</h4>", unsafe_allow_html=True)

    current = chain_data["chain"]
    while current:
        cols = st.columns(len(current["evolves_to"]) + 1)
        render_stage(current["species"])
        for evo in current["evolves_to"]:
            with cols.pop(0):
                render_stage(evo["species"])
        if current["evolves_to"]:
            current = current["evolves_to"][0]
        else:
            break
