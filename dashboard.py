import streamlit as st
from funções import layout

st.set_page_config(page_title="Apuama Racing Dashboard", layout="wide")

with st.container():
    with st.sidebar:
        st.image("apuama_logo.png")
        st.subheader("Análise de Dados")
        opção = st.selectbox("Opção desejada", options=["Dashboard", "Plotar Gráfico"])

with st.container():
    layout(opção)

                    








    