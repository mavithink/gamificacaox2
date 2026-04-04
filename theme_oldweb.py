import streamlit as st

def injetar_css_oldweb():
    st.markdown("""
    <style>
    /* Importando a fonte Pixel Art (VT323) */
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    /* 1. Reset Global e Fundo */
    .stApp {
        background-color: #C0C0C0; 
        font-family: 'VT323', monospace !important;
        color: #000000 !important;
        font-size: 18px !important; 
    }

    /* 2. Container Principal */
    .block-container {
        background-color: #ffffff;
        border: 2px solid #000000; 
        padding: 10px 15px !important; 
        box-shadow: 2px 2px 0px #808080; 
        margin-top: 10px;
    }

    /* 3. Cabeçalhos */
    h1 { font-size: 26px !important; padding-bottom: 2px; }
    h2 { font-size: 22px !important; }
    h3, h4 { font-size: 20px !important; }
    
    h1, h2, h3, h4 {
        font-family: 'VT323', monospace !important;
        color: #6e0b8a !important; /* ROXO */
        font-weight: normal !important;
        border-bottom: 1px solid #6e0b8a; 
        margin-bottom: 5px !important;
        margin-top: 5px !important;
    }

    /* 4. Botões Estilo Clássico */
    .stButton > button {
        background-color: #DFDFDF !important;
        border: 2px solid !important;
        border-color: #FFFFFF #404040 #404040 #FFFFFF !important; 
        border-radius: 0px !important; 
        color: #000000 !important;
        font-family: 'VT323', monospace !important;
        font-size: 18px !important;
        padding: 0px 5px !important; 
        min-height: 25px !important; 
        box-shadow: none !important;
        transition: none !important; 
    }
    .stButton > button:active {
        border-color: #404040 #FFFFFF #FFFFFF #404040 !important; 
        background-color: #C0C0C0 !important;
    }
    
    /* BOTÃO PRIMÁRIO COM A COR ROXA */
    .stButton > button[kind="primary"] {
        background-color: #6e0b8a !important;
        color: #FFFFFF !important;
        border-color: #a84bc4 #3a054a #3a054a #a84bc4 !important;
    }

    /* 5. Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #C0C0C0 !important;
        border-right: 2px solid #000000 !important;
    }
    [data-testid="stSidebar"] * {
        color: #000000 !important;
        font-family: 'VT323', monospace !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #6e0b8a !important;
        text-decoration: underline; 
        cursor: pointer;
    }

    /* 6. Entradas de Dados e Alertas */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 0px !important;
        border: 1px solid #000000 !important;
        font-family: 'VT323', monospace !important;
        color: #000000 !important;
        background-color: #FFFFFF !important;
        padding: 2px !important;
    }
    
    [data-testid="stAlert"], [data-testid="stAlert"] * {
        font-family: 'VT323', monospace !important;
        border-radius: 0px !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'VT323', monospace !important;
        font-size: 24px !important;
    }

    /* 7. Remoção de Espaços Fantasmas */
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    hr {
        margin: 10px 0 !important;
        border-color: #808080 !important;
    }

    /* 8. Anulando caixas escuras residuais */
    div[style*="background-color: #1a1a2e"], 
    div[style*="background-color: #262730"],
    div[style*="background-color: #2e2e48"] {
        background-color: transparent !important;
        border: none !important;
        color: #000000 !important;
    }
    p, span, div {
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)
