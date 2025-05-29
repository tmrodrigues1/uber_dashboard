import streamlit as st

st.set_page_config(page_title="Documentação", layout="wide")

st.title("Documentação")

st.markdown("""
Em manutenção
---

""")

# Menu lateral
st.sidebar.markdown("""
<div style='text-align: center;'>
    <div style='display: inline-block; padding: 6px 20px; background-color: #1f77b4;
                color: white; border-radius: 10px; font-size: 0.88em;'>
        <a href='https://thiagorodrigues1.com.br' target='_blank' style='text-decoration: none; color: white;'>
            Desenvolvido por <b>TR1</b>
        </a>
    </div>
</div>""", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; font-size: 0.85em;'><br>Versão 1.1</div>", unsafe_allow_html=True)