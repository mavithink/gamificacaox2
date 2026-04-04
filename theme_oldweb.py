import streamlit as st

def injetar_css_oldweb():
    """
    Injeta CSS customizado para emular a estética da web dos anos 2000,
    com bordas grossas e robustas nos contêineres de tópicos.
    """
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

    /* 2. Container Principal (Toda a página) */
    .block-container {
        background-color: #E9EAED; /* Levemente cinza para destacar as caixas brancas internas */
        border: 2px solid #000000; 
        padding: 10px 20px !important; /* Economia de espaço vertical e horizontal */
        box-shadow: 2px 2px 0px #808080; 
        margin-top: 10px;
    }

    /* 3. Cabeçalhos (Reduzidos e colados no conteúdo) */
    h1 { font-size: 28px !important; padding-bottom: 2px; }
    h2 { font-size: 24px !important; }
    h3, h4 { font-size: 22px !important; }
    
    h1, h2, h3, h4 {
        font-family: 'VT323', monospace !important;
        color: #6e0b8a !important; 
        font-weight: normal !important;
        border-bottom: 1px solid #6e0b8a; 
        margin-bottom: 10px !important;
        margin-top: 5px !important;
    }

    /* 4. Botões Estilo Clássico (Mais finos e compactos) */
    .stButton > button {
        background-color: #DFDFDF !important;
        border: 2px solid !important;
        border-color: #FFFFFF #404040 #404040 #FFFFFF !important; 
        border-radius: 0px !important; /* Bordas quadradas */
        color: #000000 !important;
        font-family: 'VT323', monospace !important;
        font-size: 18px !important;
        padding: 0px 5px !important; /* Botões mais achatados */
        min-height: 25px !important; /* Reduz altura mínima do Streamlit */
        box-shadow: none !important;
        transition: none !important; /* Remove animações modernas */
    }
    .stButton > button:active {
        border-color: #404040 #FFFFFF #FFFFFF #404040 !important; 
        background-color: #C0C0C0 !important;
    }
    
    /* Botão Primário (Em Destaque) */
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

    /* 7. Remoção de Espaços Fantasmas do Streamlit */
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    hr {
        margin: 10px 0 !important;
        border-color: #808080 !important;
    }

    /* 8. QUADROS (CONTAINERS) COM BORDAS MAIS GROSSAS */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 4px solid #6e0b8a !important; /* ESPESSURA AUMENTADA PARA 4PX */
        background-color: #FFFFFF !important; /* Fundo branco para destacar os dados */
        border-radius: 0px !important;
        box-shadow: 4px 4px 0px #808080 !important; /* Sombra Old Web */
        padding: 15px !important;
        margin-bottom: 20px !important;
    }

    /* 9. BARRA DE PROGRESSO PIXELADA */
    .stProgress > div > div > div > div {
        background-color: #6e0b8a !important;
        border-radius: 0px !important;
    }
    .stProgress > div > div > div {
        background-color: #C0C0C0 !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        height: 20px !important;
    }
    
    /* 10. Expanders Estilo Retrô */
    [data-testid="stExpander"] {
        border: 2px solid #6e0b8a !important;
        background-color: #FFFFFF !important;
        border-radius: 0px !important;
        box-shadow: 2px 2px 0px #808080 !important;
    }
    [data-testid="stExpander"] summary {
        background-color: #E8D5EB !important;
    }
    [data-testid="stExpander"] summary p {
        color: #6e0b8a !important;
        font-weight: bold !important;
    }

    /* Anulando estilos residuais */
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
