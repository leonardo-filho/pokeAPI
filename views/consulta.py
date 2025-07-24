import streamlit as st
from app import api_client
from app.type_matchup import calcular_fraquezas_resistencias

def mostrar():
    st.title("🔍 Consulta de Pokémon")
    client = PokeAPIClient()

    # Lista completa de Pokémon
    all_pokemons = client._get("pokemon?limit=10000")["results"]
    nomes_full = [p["name"] for p in all_pokemons]

    # Extrai os nomes base (antes de "-" se houver)
    nomes_base = sorted(set([name.split("-")[0] for name in nomes_full]))

    # Primeira entrada: Nome base
    nome_base = st.selectbox(
        "Nome base do Pokémon", 
        options=nomes_base, 
        index=None, 
        placeholder="Ex: charizard"
    )

    if nome_base:
        # Filtra variações
        variations = sorted([n for n in nomes_full if n.startswith(nome_base)])
        variacao = st.selectbox("Selecione a variação", options=variations)

        if st.button("🔴 Buscar"):
            data = client.get_pokemon(variacao)

            if "name" not in data:
                st.error("Pokémon não encontrado.")
                return

            tipos = [t["type"]["name"] for t in data["types"]]
            img_url = data["sprites"]["front_default"]

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown(f"""
                <div style="
                    background-color: #1f1f1f;
                    padding: 30px;
                    border-radius: 15px;
                    text-align: center;
                    box-shadow: 0 0 15px #111;
                    max-width: 350px;
                    margin: auto;
                ">
                    <img src="{img_url}" width="160">
                    <p style="margin-top: 12px;"><strong style="color:white;">Tipos:</strong> <span style='color: #00ff00;'>{' '.join(tipos)}</span></p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)

            efetividades = calcular_fraquezas_resistencias(tipos, client)

            col_f, col_r = st.columns(2)

            with col_f:
                st.markdown("""
                    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px;">
                        <h5 style="color: orange;">⚡ Fraquezas</h5>
                        <div style="color: #00ff00;">{}</div>
                    </div>
                """.format(" ".join(efetividades["fraco"])), unsafe_allow_html=True)

            with col_r:
                st.markdown("""
                    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px;">
                        <h5 style="color: deepskyblue;">🛡️ Resistências</h5>
                        <div style="color: #00ff00;">{}</div>
                    </div>
                """.format(" ".join(efetividades["resistente"])), unsafe_allow_html=True)

            if efetividades["imune"]:
                st.markdown("""
                    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-top: 20px;">
                        <h5 style="color: crimson;">🚫 Imunes</h5>
                        <div style="color: #00ff00;">{}</div>
                    </div>
                """.format(" ".join(efetividades["imune"])), unsafe_allow_html=True)
