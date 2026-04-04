import streamlit as st

def injetar_css_oldweb():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    /* 1. Reset Global e Fundo */
    .stApp {
        background-color: #C0C0C0; 
        font-family: 'VT323', monospace !important;
        color: #000000 !important;
        font-size: 18px !important; 
    }

    /* 2. Container Principal (Borda grossa preta) */
    .block-container {
        background-color: #E9EAED; 
        border: 4px solid #000000 !important; /* AUMENTADO */
        padding: 10px 20px !important; 
        box-shadow: 4px 4px 0px #808080 !important; /* Sombra mais densa */
        margin-top: 10px;
    }

    /* 3. Cabeçalhos */
    h1 { font-size: 28px !important; padding-bottom: 2px; }
    h2 { font-size: 24px !important; }
    h3, h4 { font-size: 22px !important; }
    
    h1, h2, h3, h4 {
        font-family: 'VT323', monospace !important;
        color: #6e0b8a !important; 
        font-weight: normal !important;
        border-bottom: 3px solid #6e0b8a !important; /* AUMENTADO */
        margin-bottom: 10px !important;
        margin-top: 5px !important;
    }

    /* 4. Botões Estilo Clássico (Efeito 3D mais robusto) */
    .stButton > button {
        background-color: #DFDFDF !important;
        border: 3px solid !important; /* AUMENTADO */
        border-color: #FFFFFF #404040 #404040 #FFFFFF !important; 
        border-radius: 0px !important; 
        color: #000000 !important;
        font-family: 'VT323', monospace !important;
        font-size: 18px !important;
        padding: 2px 5px !important; 
        min-height: 25px !important; 
        box-shadow: none !important;
        transition: none !important; 
    }
    .stButton > button:active {
        border-color: #404040 #FFFFFF #FFFFFF #404040 !important; 
        background-color: #C0C0C0 !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #6e0b8a !important;
        color: #FFFFFF !important;
        border-color: #a84bc4 #2e043a #2e043a #a84bc4 !important;
    }

    /* 5. Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #C0C0C0 !important;
        border-right: 4px solid #000000 !important; /* AUMENTADO */
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
        border: 2px solid #000000 !important; /* AUMENTADO */
        font-family: 'VT323', monospace !important;
        color: #000000 !important;
        background-color: #FFFFFF !important;
        padding: 2px !important;
    }
    
    [data-testid="stAlert"], [data-testid="stAlert"] * {
        font-family: 'VT323', monospace !important;
        border-radius: 0px !important;
        border-width: 2px !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'VT323', monospace !important;
        font-size: 24px !important;
    }

    /* 7. Quadros (Containers) com Bordas Grossas */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 4px solid #6e0b8a !important; /* AUMENTADO */
        background-color: #FFFFFF !important; 
        border-radius: 0px !important;
        box-shadow: 4px 4px 0px #808080 !important; 
        padding: 15px !important;
        margin-bottom: 20px !important;
    }

    /* 8. Barra de Progresso Pixelada */
    .stProgress > div > div > div > div {
        background-color: #6e0b8a !important;
        border-radius: 0px !important;
    }
    .stProgress > div > div > div {
        background-color: #C0C0C0 !important;
        border: 3px solid #000000 !important; /* AUMENTADO */
        border-radius: 0px !important;
        height: 20px !important;
    }
    
    /* 9. Expanders Estilo Retrô */
    [data-testid="stExpander"] {
        border: 4px solid #6e0b8a !important; /* AUMENTADO */
        background-color: #FFFFFF !important;
        border-radius: 0px !important;
        box-shadow: 4px 4px 0px #808080 !important;
    }
    [data-testid="stExpander"] summary {
        background-color: #E8D5EB !important;
    }
    [data-testid="stExpander"] summary p {
        color: #6e0b8a !important;
        font-weight: bold !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    hr {
        margin: 10px 0 !important;
        border-top: 3px solid #808080 !important; /* AUMENTADO */
    }
    
    div[style*="background-color: transparent"] {
        border: none !important;
    }
    p, span, div { color: #000000; }
    </style>
    """, unsafe_allow_html=True)
