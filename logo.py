import base64
import os
import streamlit as st

# Configurar el tema de Streamlit
st.set_page_config(page_title="Directorio empresas en INEGI", layout="centered", initial_sidebar_state="collapsed")

# Mostrar el logo de la empresa centrado y con el tamaño original
logo_path = os.path.join('path_to_your_logo_directory', 'logo.webp')
logo_bytes = open(logo_path, "rb").read()
logo_base64 = base64.b64encode(logo_bytes).decode("utf-8")

st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/webp;base64,{logo_base64}">
    </div>
""", unsafe_allow_html=True)
