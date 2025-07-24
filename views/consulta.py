import streamlit as st
from app.api_client import PokeAPIClient
from app.type_matchup import calcular_efetividades

def mostrar():
    client = PokeAPIClient()
    st.markdown("## 🔍 Consulta de Pokémon")

    nome = st.text_input("### Nome do Pokémon", "charizard")

    if st.button("🔴 Buscar", use_container_width=True):
        dados = client.get_pokemon(nome)
        if "erro" in dados:
            st.error("❌ Não encontrado.")
        else:
            tipos = [t["type"]["name"] for t in dados["types"]]
            ef = calcular_efetividades(tipos, client)

            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(dados["sprites"]["front_default"], width=130)
            with col2:
                st.markdown(f"### {dados['name'].capitalize()}")
                st.markdown(f"**Tipos:** " + ", ".join(f"`{t}`" for t in tipos))

            st.markdown("---")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### ⚡ Fraquezas")
                st.markdown(", ".join(f"`{t}`" for t in sorted(ef["fraco"])) or "Nenhuma")

            with col2:
                st.markdown("#### 🛡️ Resistências")
                st.markdown(", ".join(f"`{t}`" for t in sorted(ef["resistente"])) or "Nenhuma")

            with col3:
                st.markdown("#### 🚫 Imunes")
                st.markdown(", ".join(f"`{t}`" for t in sorted(ef["imune"])) or "Nenhuma")
