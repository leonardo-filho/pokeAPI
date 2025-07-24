import streamlit as st
from app.api_client import PokeAPIClient
from app.evolution_chain import extrair_evolucoes

def mostrar():
    client = PokeAPIClient()
    st.subheader("🧬 Evolução de Pokémon")
    nome = st.text_input("Nome base", "charmander")

    if st.button("Ver Evolução"):
        especie = client.get_species(nome)
        if "evolution_chain" not in especie:
            st.error("Não encontrado ou sem evolução.")
        else:
            evo_id = especie["evolution_chain"]["url"].rstrip("/").split("/")[-1]
            cadeia = client.get_evolution_chain(evo_id)
            nomes = extrair_evolucoes(cadeia)

            cols = st.columns(len(nomes))
            for i, n in enumerate(nomes):
                poke = client.get_pokemon(n)
                with cols[i]:
                    st.image(poke["sprites"]["front_default"], width=90)
                    st.markdown(n.capitalize())
