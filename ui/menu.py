import streamlit as st

def menu_sidebar():
    st.sidebar.markdown("<h3 style='font-size:20px;'>🌐 Idioma</h3>", unsafe_allow_html=True)
    lang = st.sidebar.radio("", options=["pt", "en"], horizontal=True)

    traducoes = {
        "pt": {
            "consulta": "🔍 Consulta Pokémon",
            "evolucao": "🧬 Evoluções"
        },
        "en": {
            "consulta": "🔍 Pokémon Search",
            "evolucao": "🧬 Evolutions"
        }
    }

    paginas = traducoes[lang]

    st.sidebar.markdown("---")
    pagina_traduzida = st.sidebar.radio("", list(paginas.values()))

    id_paginas = {v: k for k, v in paginas.items()}
    return id_paginas[pagina_traduzida], lang
