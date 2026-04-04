import streamlit as st

def injetar_css_oldweb():
    st.markdown("""
    <style>
    /* 1. Reset Global e Fundo */
    .stApp {
        background-color: #E9EAED; 
        font-family: 'Verdana', 'Tahoma', 'Arial', sans-serif !important;
        color: #000000 !important;
    }

    /* 2. Container Principal */
    .block-container {
        background-color: #ffffff;
        border: 2px solid #3B5998; 
        padding: 20px !important;
        box-shadow: 4px 4px 0px #A0A0A0; 
        margin-top: 20px;
    }

    /* 3. Cabeçalhos (Reduzidos para estética retro) */
    h1 { font-size: 22px !important; padding-bottom: 5px; }
    h2 { font-size: 18px !important; }
    h3, h4 { font-size: 15px !important; }
    
    h1, h2, h3, h4 {
        font-family: 'Tahoma', 'Arial', sans-serif !important;
        color: #3B5998 !important;
        font-weight: bold !important;
        border-bottom: 2px solid #3B5998; 
        margin-bottom: 15px !important;
        margin-top: 10px !important;
    }

    /* 4. Botões Estilo Clássico */
    .stButton > button {
        background-color: #E0E0E0 !important;
        border: 2px solid !important;
        border-color: #FFFFFF #808080 #808080 #FFFFFF !important; 
        border-radius: 0px !important; 
        color: #000000 !important;
        font-family: 'MS Sans Serif', 'Verdana', sans-serif !important;
        font-weight: bold !important;
        font-size: 12px !important;
        padding: 2px 10px !important;
        box-shadow: none !important;
        transition: none !important; 
    }
    .stButton > button:active {
        border-color: #808080 #FFFFFF #FFFFFF #808080 !important; 
        background-color: #D0D0D0 !important;
    }
    .stButton > button[kind="primary"] {
        background-color: #3B5998 !important;
        color: #FFFFFF !important;
        border-color: #8B9DC3 #1D2B4D #1D2B4D #8B9DC3 !important;
    }

    /* 5. Barra Lateral (Forçando contraste) */
    [data-testid="stSidebar"] {
        background-color: #D8DFEA !important;
        border-right: 2px solid #3B5998 !important;
    }
    [data-testid="stSidebar"] * {
        color: #000000 !important; /* Força todo o texto a ficar preto */
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #3B5998 !important;
        text-decoration: underline; 
        cursor: pointer;
        font-weight: bold;
    }

    /* 6. Entradas de Dados */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 0px !important;
        border: 1px solid #707070 !important;
        box-shadow: inset 1px 1px 3px #cccccc !important;
        font-family: 'Verdana', sans-serif !important;
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    /* 7. Alertas e Divs */
    [data-testid="stAlert"] {
        border-radius: 0px !important;
        border: 1px solid #000000 !important;
        box-shadow: 2px 2px 0px #888888 !important;
        color: #000000 !important;
    }
    div[style*="background-color: #1a1a2e"], 
    div[style*="background-color: #262730"],
    div[style*="background-color: #2e2e48"] {
        background-color: #F7F7F7 !important;
        border: 1px solid #3B5998 !important;
        border-radius: 0px !important;
        color: #000000 !important;
        box-shadow: none !important;
    }
    p, span, div {
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)
