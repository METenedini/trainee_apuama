import streamlit as st
from comandos import LeitorDataFrame, Graficos
import inspect

@st.cache_data
def carregar_dados():
    caminho_arquivo = "dados1.csv"
    df = LeitorDataFrame(caminho_arquivo).df
    return df

def verificar(string, tipo):
    if string in inspect.getfullargspec(Graficos(carregar_dados()).methods[tipo])[0]:
        return True
    else:
        return False

def plotar(tipo_grafico, eixo_x=None, eixo_y=None, plot=None, col=None, hue=None, size=None):
    if plot:
        if col:
            st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, col), use_container_width=True)
        elif hue:
            if size:
                st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, hue, size), use_container_width=True)
            else:
                st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, hue), use_container_width=True)
        else:
            if eixo_y:
                st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y), use_container_width=True)
            else:
                st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x), use_container_width=True)


def salvar(tipo_grafico, eixo_x=None, eixo_y=None, col=None, hue=None, size=None, save=None):
    if col:
        Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, col, save)
    elif hue:
        if size:
            Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, hue, size, save)
        else:
            Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, hue, save)
    else:
        if eixo_y:
            Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, save)
        else:
            Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, save)


def layout(opcao):
    match opcao:
        case 'Dashboard':
            layout_dashboard()
        case 'Plotar Gráfico':
            layout_plotar_grafico()

def layout_dashboard():
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    with col1:
        st.pyplot(Graficos(carregar_dados()).plot("linearplot_hue", "TIME", "RPM", "Marcha"), use_container_width=True)
    with col2:
        st.pyplot(Graficos(carregar_dados()).plot("jointplot", "Pressão_de_Óleo", "RPM", "Marcha"), use_container_width=True)
    with col3:
        st.pyplot(Graficos(carregar_dados()).plot("barplot", "Marcha", "RPM"), use_container_width=True)
    with col4:
        st.pyplot(Graficos(carregar_dados()).plot("relplot", "RPM", "RPM_motor_/_Cardan","Marcha","RPM_do_câmbio"), use_container_width=True)
    with col5:
        st.pyplot(Graficos(carregar_dados()).plot("linearplot", "TIME","Temp._do_motor","Marcha"), use_container_width=True)
    with col6:
        st.pyplot(Graficos(carregar_dados()).plot("dispersão 3D", "RPM","RPM_motor_/_Cardan","RPM_do_câmbio"), use_container_width=True)

def layout_plotar_grafico():
    eixo_x = None
    eixo_y = None
    hue = None
    size = None
    col = None
    save = st.session_state.get("save", None)

    col1 = st.empty()
    col2, col3 = st.columns(2)
    col4, col5 = st.columns(2)
    col6 = st.empty()
    
    with col1:
        tipo_grafico = st.selectbox("Selecione o Gráfico", options=Graficos(carregar_dados()).get_method_names())
    with col2:
        eixo_x = st.selectbox("Eixo X", options=list(carregar_dados().columns))
        if verificar("hue", tipo_grafico):
            hue = st.selectbox("hue", options=list(carregar_dados().columns))
    with col3:
        if verificar("y", tipo_grafico):
            eixo_y = st.selectbox("Eixo Y", options=list(carregar_dados().columns))
        if verificar("col", tipo_grafico):
            col = st.selectbox("Colunas", options=list(carregar_dados().columns))
        if verificar("size", tipo_grafico):
            size = st.selectbox("size", options=list(carregar_dados().columns))
    with col4:
        if verificar("z",tipo_grafico):
            eixo_z=st.selectbox("Eixo Z", options=list(carregar_dados().columns))
        plot = st.button("Plotar Gráfico")
    with col5:
        save = st.text_input("Nome do arquivo para salvar", value=save, key="save_input")
        save_button = st.button("Salvar")
        if save_button:
            st.session_state.save = save  # Atualiza o valor em session_state
            salvar(tipo_grafico, eixo_x, eixo_y, col, hue, size, save)
    with col6:
        plotar(tipo_grafico, eixo_x, eixo_y, plot, col, hue, size)
