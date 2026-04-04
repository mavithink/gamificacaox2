import streamlit as st

def injetar_css_oldweb():
    """
    Injeta CSS customizado para emular a estética da web dos anos 2000.
    Força fontes clássicas, bordas afiadas, cores planas e sombras duras.
    """
    st.markdown("""
    <style>
    /* 1. Reset Global e Fundo */
    .stApp {
        background-color: #E9EAED; /* Fundo cinza/azul claro clássico */
        font-family: 'Verdana', 'Tahoma', 'Arial', sans-serif !important;
        color: #000000 !important;
    }

    /* 2. Container Principal (A "Página" de conteúdo) */
    .block-container {
        background-color: #ffffff;
        border: 2px solid #3B5998; /* Azul clássico do MySpace/Facebook */
        padding: 30px !important;
        box-shadow: 4px 4px 0px #A0A0A0; /* Sombra dura (sem desfoque) */
        margin-top: 20px;
    }

    /* 3. Cabeçalhos (H1, H2, H3) */
    h1, h2, h3, h4 {
        font-family: 'Tahoma', 'Arial', sans-serif !important;
        color: #3B5998 !important;
        font-weight: bold !important;
        border-bottom: 2px solid #3B5998; /* Linha de separação */
        padding-bottom: 4px;
        margin-bottom: 15px !important;
    }

    /* 4. Botões Estilo Windows 98/XP / HTML Padrão */
    .stButton > button {
        background-color: #E0E0E0 !important;
        border: 2px solid !important;
        border-color: #FFFFFF #808080 #808080 #FFFFFF !important; /* Efeito Bevel (Relevo) */
        border-radius: 0px !important; /* Bordas quadradas */
        color: #000000 !important;
        font-family: 'MS Sans Serif', 'Verdana', sans-serif !important;
        font-weight: bold !important;
        font-size: 13px !important;
        box-shadow: none !important;
        transition: none !important; /* Remove animações modernas */
    }
    .stButton > button:active {
        border-color: #808080 #FFFFFF #FFFFFF #808080 !important; /* Inverte o relevo ao clicar */
        background-color: #D0D0D0 !important;
    }
    
    /* Botões Primários (Em Destaque) */
    .stButton > button[kind="primary"] {
        background-color: #3B5998 !important;
        color: #FFFFFF !important;
        border-color: #8B9DC3 #1D2B4D #1D2B4D #8B9DC3 !important;
    }

    /* 5. Barra Lateral (Navegação) */
    [data-testid="stSidebar"] {
        background-color: #D8DFEA !important;
        border-right: 2px solid #3B5998 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-family: 'Verdana', sans-serif !important;
        color: #3B5998 !important;
        text-decoration: underline; /* Links clássicos */
        cursor: pointer;
    }

    /* 6. Caixas de Texto e Entradas de Dados */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 0px !important;
        border: 1px solid #707070 !important;
        box-shadow: inset 1px 1px 3px #cccccc !important;
        font-family: 'Verdana', sans-serif !important;
    }

    /* 7. Caixas de Aviso (Success, Error, Warning) */
    [data-testid="stAlert"] {
        border-radius: 0px !important;
        border: 1px solid #000000 !important;
        box-shadow: 2px 2px 0px #888888 !important;
    }

    /* 8. Estilização das Divs personalizadas (Anulando CSS moderno anterior) */
    div[style*="background-color: #1a1a2e"], 
    div[style*="background-color: #262730"] {
        background-color: #F7F7F7 !important;
        border: 1px solid #3B5998 !important;
        border-radius: 0px !important;
        color: #000000 !important;
        box-shadow: none !important;
    }
    
    /* Substituindo cores de texto claras por escuras nos painéis */
    div[style*="color: white"], p[style*="color: #8a8a9d"] {
        color: #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)
