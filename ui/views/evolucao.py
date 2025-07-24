import streamlit as st
import requests
from app.utils import get_all_pokemon_names, format_pokemon_name
from app.type_matchup import TYPE_COLORS  # mesma estrutura usada na tela de consulta

def mostrar(lang):
    titulos = {
        "pt": {
            "titulo": "🧬 Linha Evolutiva",
            "placeholder": "Digite o nome do Pokémon base",
            "erro": "Pokémon não encontrado ou erro na API.",
        },
        "en": {
            "titulo": "🧬 Evolution Chain",
            "placeholder": "Enter base Pokémon name",
            "erro": "Pokémon not found or API error.",
        }
    }

    t = titulos.get(lang, titulos["en"])
    st.markdown(f"## {t['titulo']}")

    nomes_disponiveis = get_all_pokemon_names()
    nome = st.selectbox(t["placeholder"], nomes_disponiveis, placeholder="Ex: bulbasaur").strip().lower()
    if not nome:
        return

    # Obter cadeia evolutiva
    try:
        species_url = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{nome}").json()["evolution_chain"]["url"]
        chain = requests.get(species_url).json()["chain"]
    except:
        st.error(t["erro"])
        return

    # Recursivamente extrai os nomes da cadeia
    def extrair_nomes(no):
        nomes = [no["species"]["name"]]
        for prox in no["evolves_to"]:
            nomes.extend(extrair_nomes(prox))
        return nomes

    nomes = list(dict.fromkeys(extrair_nomes(chain)))  # remove duplicatas

    # Renderização vertical dos cards
    for i, nome_poke in enumerate(nomes):
        dados = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome_poke}").json()
        imagem = dados["sprites"]["front_default"]
        tipos = [t["type"]["name"] for t in dados["types"]]

        # Card do Pokémon
        with st.container():
            st.markdown(
                f"""
                <div style='
                    background-color: #1f1f1f;
                    border-radius: 12px;
                    padding: 1rem;
                    margin-bottom: 1.5rem;
                    text-align: center;
                    box-shadow: 0 0 10px rgba(255,255,255,0.05);
                '>
                    <img src="{imagem}" width="120">
                    <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">
                        {format_pokemon_name(nome_poke)}
                    </div>
                    <div style="margin-top: 0.5rem;">
                        {''.join([f"<span style='background-color: {TYPE_COLORS.get(tipo, "#888")}; color: white; padding: 0.3rem 0.6rem; border-radius: 8px; margin: 0 0.2rem; font-size: 0.9rem;'>{tipo.title()}</span>" for tipo in tipos])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if i < len(nomes) - 1:
            st.markdown("<div style='text-align: center; font-size: 2rem;'>⬇️</div>", unsafe_allow_html=True)
