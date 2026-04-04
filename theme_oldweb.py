import streamlit as st

def injetar_css_oldweb():
    st.markdown("""
    <style>
    /* Importando a fonte Pixel Art (VT323) */
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    /* 1. Reset Global e Fundo */
    .stApp {
        background-color: #C0C0C0; /* Cinza clássico Windows 95/98 */
        font-family: 'VT323', monospace !important;
        color: #000000 !important;
        font-size: 18px !important; /* Fonte pixelada precisa ser um pouco maior para leitura */
    }

    /* 2. Container Principal (Mais estreito e compacto) */
    .block-container {
        background-color: #ffffff;
        border: 2px solid #000000; 
        padding: 10px 15px !important; /* Economia de espaço vertical e horizontal */
        box-shadow: 2px 2px 0px #808080; 
        margin-top: 10px;
    }

    /* 3. Cabeçalhos (Reduzidos e colados no conteúdo) */
    h1 { font-size: 24px !important; padding-bottom: 2px; }
    h2 { font-size: 20px !important; }
    h3, h4 { font-size: 18px !important; }
    
    h1, h2, h3, h4 {
        font-family: 'VT323', monospace !important;
        color: #000080 !important; /* Azul marinho clássico */
        font-weight: normal !important;
        border-bottom: 1px solid #000080; 
        margin-bottom: 5px !important;
        margin-top: 5px !important;
    }

    /* 4. Botões Estilo Clássico (Mais finos e compactos) */
    .stButton > button {
        background-color: #DFDFDF !important;
        border: 2px solid !important;
        border-color: #FFFFFF #404040 #404040 #FFFFFF !important; 
        border-radius: 0px !important; 
        color: #000000 !important;
        font-family: 'VT323', monospace !important;
        font-size: 16px !important;
        padding: 0px 5px !important; /* Botões mais achatados */
        min-height: 25px !important; /* Reduz altura mínima do Streamlit */
        box-shadow: none !important;
        transition: none !important; 
    }
    .stButton > button:active {
        border-color: #404040 #FFFFFF #FFFFFF #404040 !important; 
        background-color: #C0C0C0 !important;
    }
    .stButton > button[kind="primary"] {
        background-color: #000080 !important;
        color: #FFFFFF !important;
        border-color: #8B9DC3 #000000 #000000 #8B9DC3 !important;
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
        color: #000080 !important;
        text-decoration: underline; 
        cursor: pointer;
    }

    /* 6. Entradas de Dados e Métricas */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 0px !important;
        border: 1px solid #000000 !important;
        font-family: 'VT323', monospace !important;
        color: #000000 !important;
        background-color: #FFFFFF !important;
        padding: 2px !important;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'VT323', monospace !important;
        font-size: 24px !important;
    }

    /* 7. Remoção de Espaços Fantasmas do Streamlit */
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
