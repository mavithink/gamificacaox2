import requests
import streamlit as st
import json
import os
import random
import time
import pandas as pd
from datetime import datetime, timedelta
from todo_list import renderizar_todo_list

DATA_FILE = "status_usuario.json"
XP_POR_NIVEL = 300

FIREBASE_URL_DADOS = "https://gamix2-57898-default-rtdb.firebaseio.com/status_usuario.json"

def carregar_dados():
    try:
        resposta = requests.get(FIREBASE_URL_DADOS)
        if resposta.status_code == 200 and resposta.json() is not None:
            dados = resposta.json()
            novas_chaves = {
                "streak": 0,
                "ultima_atividade": str(datetime.now().date() - timedelta(days=1)),
                "ultimo_registro_full": str(datetime.now()),
                "ultimo_acordar_cedo": str(datetime.now().date() - timedelta(days=1)),
                "ultimo_ghost_check": str(datetime.now().date() - timedelta(days=1)),
                "contadores": {},
                "sorte_dia": {"data": "", "efeito": None},
                "ultima_punicao_data": "",
                "historico_diario": {},
                "missoes_diarias": {"data": "", "missoes": []},
                "limites_diarios": {"noticias": "", "paginas": ""},
                "cultura": {
                    "mes_referencia": datetime.now().strftime("%Y-%m"),
                    "filmes": [],
                    "livros": []
                }
            }
            for k, v in novas_chaves.items():
                if k not in dados: dados[k] = v
            
            # Restauração estrutural contra deleção de listas vazias pelo Firebase
            if "cultura" not in dados:
                dados["cultura"] = {"mes_referencia": datetime.now().strftime("%Y-%m"), "filmes": [], "livros": []}
            if "filmes" not in dados["cultura"]:
                dados["cultura"]["filmes"] = []
            if "livros" not in dados["cultura"]:
                dados["cultura"]["livros"] = []
            if "missoes_diarias" not in dados:
                dados["missoes_diarias"] = {"data": "", "missoes": []}
            if "missoes" not in dados["missoes_diarias"]:
                dados["missoes_diarias"]["missoes"] = []
                
            if "conquistas" not in dados:
                dados["conquistas"] = {
                    "madrugador": {"atual": 0, "total": 10, "completadas": 0, "ultima_data": str(datetime.now().date() - timedelta(days=1)), "data_conclusao": ""},
                    "incorruptivel": {"atual": 0, "total": 3, "completadas": 0, "ultima_verificacao": str(datetime.now().date()), "data_conclusao": ""}
                }
            return dados
    except Exception:
        pass
        
    return {
        "saldo": 0, "xp": 0, "nivel": 1, "cupons": 0, "contadores": {}, "streak": 0,
        "ultima_atividade": str(datetime.now().date() - timedelta(days=1)),
        "ultimo_registro_full": str(datetime.now()),
        "ultimo_acordar_cedo": str(datetime.now().date() - timedelta(days=1)),
        "ultimo_ghost_check": str(datetime.now().date() - timedelta(days=1)),
        "sorte_dia": {"data": "", "efeito": None},
        "ultima_punicao_data": "",
        "historico_diario": {},
        "missoes_diarias": {"data": "", "missoes": []},
        "limites_diarios": {"noticias": "", "paginas": ""},
        "cultura": {
            "mes_referencia": datetime.now().strftime("%Y-%m"),
            "filmes": [],
            "livros": []
        },
        "conquistas": {
            "madrugador": {"atual": 0, "total": 10, "completadas": 0, "ultima_data": str(datetime.now().date() - timedelta(days=1)), "data_conclusao": ""},
            "incorruptivel": {"atual": 0, "total": 3, "completadas": 0, "ultima_verificacao": str(datetime.now().date()), "data_conclusao": ""}
        }
    }
        
        
def salvar_dados(dados):
    requests.put(FIREBASE_URL_DADOS, json=dados)

def verificar_estagnacao(dados):
    agora = datetime.now()
    ultima = datetime.fromisoformat(dados["ultimo_registro_full"])
    estagnado = agora - ultima > timedelta(hours=24)
    if estagnado:
        if st.session_state.get('punicao_aplicada') != ultima:
            dados["saldo"] = int(dados["saldo"] * 0.9)
            dados["xp"] = int(dados["xp"] * 0.9)
            dados["ultima_punicao_data"] = str(agora.date())
            dados["conquistas"]["incorruptivel"]["atual"] = 0
            st.session_state['punicao_aplicada'] = ultima
            salvar_dados(dados)
    return estagnado

def verificar_ghost(dados):
    hoje = datetime.now().date()
    ultimo_check_str = dados.get("ultimo_ghost_check", str(hoje - timedelta(days=1)))
    ultimo_check = datetime.strptime(ultimo_check_str, "%Y-%m-%d").date()
    
    avisos = []
    if ultimo_check < hoje:
        while ultimo_check < hoje:
            dia_str = str(ultimo_check)
            dia_semana_passada = str(ultimo_check - timedelta(days=7))
            
            p_atual = dados["historico_diario"].get(dia_str, {}).get("pomodoros", 0.0)
            p_passado = dados["historico_diario"].get(dia_semana_passada, {}).get("pomodoros", 0.0)
            
            meta = min(p_passado + 1.0, 8.0)
            
            if p_atual >= meta and p_atual > 0:
                dados["saldo"] += 30
                avisos.append(f"👻 Ghost derrotado em {dia_str}! Você fez {p_atual:.1f} sessões. Bônus de +30$ creditado.")
                
            ultimo_check += timedelta(days=1)
            
        dados["ultimo_ghost_check"] = str(hoje)
        salvar_dados(dados)
    return avisos

def atualizar_incorruptivel(dados):
    hoje = datetime.now().date()
    ultima_verif_str = dados["conquistas"]["incorruptivel"].get("ultima_verificacao", str(hoje))
    ultima_verif = datetime.strptime(ultima_verif_str, "%Y-%m-%d").date()
    
    while ultima_verif < hoje:
        ultima_verif += timedelta(days=1)
        if dados.get("ultima_punicao_data") != str(ultima_verif):
            dados["conquistas"]["incorruptivel"]["atual"] += 1
        else:
            dados["conquistas"]["incorruptivel"]["atual"] = 0
        
        if dados["conquistas"]["incorruptivel"]["atual"] >= 3:
            dados["saldo"] += 10
            dados["xp"] += 10
            dados["conquistas"]["incorruptivel"]["completadas"] += 1
            dados["conquistas"]["incorruptivel"]["data_conclusao"] = str(ultima_verif)
            dados["conquistas"]["incorruptivel"]["atual"] = 0
            
    dados["conquistas"]["incorruptivel"]["ultima_verificacao"] = str(hoje)

def verificar_reset_madrugador(dados):
    hoje = datetime.now().date()
    ultima_str = dados["conquistas"]["madrugador"]["ultima_data"]
    ultima = datetime.strptime(ultima_str, "%Y-%m-%d").date()
    if hoje > ultima + timedelta(days=1):
        dados["conquistas"]["madrugador"]["atual"] = 0

def verificar_mes_cultura(dados):
    mes_atual = datetime.now().strftime("%Y-%m")
    if dados["cultura"]["mes_referencia"] != mes_atual:
        qtd_filmes = len(dados["cultura"]["filmes"])
        qtd_livros = len(dados["cultura"]["livros"])
        
        if qtd_filmes > 0 or qtd_livros > 0:
            bonus_s = (qtd_filmes * 20) + (qtd_livros * 50)
            bonus_x = (qtd_filmes * 20) + (qtd_livros * 50)
            dados["saldo"] += bonus_s
            dados["xp"] += bonus_x
            st.session_state["msg_cultura"] = f"Mês encerrado! Bônus de Cultura recebido: +{bonus_s}$ e +{bonus_x}XP ({qtd_filmes} filmes, {qtd_livros} livros)."
        
        dados["cultura"]["filmes"] = []
        dados["cultura"]["livros"] = []
        dados["cultura"]["mes_referencia"] = mes_atual
        salvar_dados(dados)

def aplicar_sorte_diaria(dados):
    hoje = str(datetime.now().date())
    if dados["sorte_dia"]["data"] != hoje:
        opcoes = [
            ("Dia de Sorte", "🍀 +5 moedas por cada Pomodoro hoje"),
            ("Inflação", "💸 Itens da loja custam 20% a mais"),
            ("Foco Total", "🧠 Tópicos concluídos dão o dobro de XP"),
            ("Limpinho", "🧹 Tarefas de limpeza dão o dobro de moedas"),
            ("Dia de Cinema", "🍿 Assistir a um filme custa apenas 30 moedas"),
            ("Não faça isso", "🚫 Punições retiram o triplo de moedas")
        ]
        sorteio = random.choice(opcoes)
        dados["sorte_dia"] = {"data": hoje, "efeito": sorteio[0], "desc": sorteio[1]}
        salvar_dados(dados)

def gerar_missoes_diarias(dados):
    hoje = str(datetime.now().date())
    if dados.get("missoes_diarias", {}).get("data") != hoje:
        pool_missoes = [
            {"desc": "Faça 3 Pomodoros hoje", "s": 20, "x": 15},
            {"desc": "Sobreviva o dia sem gastar na Loja", "s": 15, "x": 20},
            {"desc": "Adicione ou conclua 2 tarefas da To-Do List", "s": 10, "x": 10},
            {"desc": "Beba 2 litros de água", "s": 5, "x": 5},
            {"desc": "Leia algum artigo de tecnologia", "s": 10, "x": 10},
            {"desc": "Leia 10 páginas de um livro/artigo não obrigatório", "s": 15, "x": 15},
            {"desc": "Organize e limpe sua mesa de estudos", "s": 10, "x": 10},
            {"desc": "Revise anotações antigas por 20 min", "s": 20, "x": 20},
            {"desc": "Aprenda um atalho novo no teclado ou IDE", "s": 10, "x": 15},
            {"desc": "Assista a um vídeo técnico sobre Python", "s": 15, "x": 20},
            {"desc": "Faça um commit em um projeto pessoal", "s": 25, "x": 30},
            {"desc": "Leia um artigo sobre Análise de Dados ou IA", "s": 15, "x": 20},
            {"desc": "Fique 4 horas seguidas sem abrir Redes Sociais", "s": 20, "x": 20},
            {"desc": "Faça um resumo de 1 página sobre um tópico recente", "s": 15, "x": 25},
            {"desc": "Planeje o dia de amanhã na To-Do List", "s": 10, "x": 10},
            {"desc": "Assista a um filme hoje", "s": 20, "x": 20},
            {"desc": "Leia mais 5 páginas", "s": 15, "x": 15}
        ]
        sorteadas = random.sample(pool_missoes, 3)
        for m in sorteadas:
            m["concluida"] = False
            
        dados["missoes_diarias"] = {"data": hoje, "missoes": sorteadas}
        salvar_dados(dados)

def alterar_valor(dados, chave, v_saldo, v_xp, operacao="soma", qtd_sessoes=1.0):
    hoje_str = str(datetime.now().date())
    if hoje_str not in dados["historico_diario"]:
        dados["historico_diario"][hoje_str] = {"pomodoros": 0.0, "moedas_ganhas": 0}

    if operacao == "soma":
        hoje = datetime.now().date()
        ultima = datetime.strptime(dados["ultima_atividade"], "%Y-%m-%d").date()
        if dados["streak"] == 0 or hoje == ultima + timedelta(days=1):
            dados["streak"] += 1
            dados["ultima_atividade"] = str(hoje)
            if dados["streak"] % 10 == 0:
                dados["saldo"] += 200
                dados["xp"] += 150
        elif hoje > ultima + timedelta(days=1):
            dados["streak"] = 1
            dados["ultima_atividade"] = str(hoje)
        
        dados['saldo'] += v_saldo
        dados['xp'] += v_xp
        dados["contadores"][chave] = dados["contadores"].get(chave, 0) + 1
        dados["ultimo_registro_full"] = str(datetime.now())
        
        dados["historico_diario"][hoje_str]["moedas_ganhas"] += v_saldo
        if chave == "Pomodoro":
            dados["historico_diario"][hoje_str]["pomodoros"] += qtd_sessoes

    elif operacao == "subtracao":
        if dados["contadores"].get(chave, 0) > 0:
            dados['saldo'] -= v_saldo
            dados['xp'] -= v_xp
            dados["contadores"][chave] -= 1
            
            dados["historico_diario"][hoje_str]["moedas_ganhas"] -= v_saldo
            if chave == "Pomodoro":
                dados["historico_diario"][hoje_str]["pomodoros"] = max(0.0, dados["historico_diario"][hoje_str]["pomodoros"] - qtd_sessoes)

    salvar_dados(dados)
    st.rerun()

# Inicialização e Checagens Diárias
st.set_page_config(page_title="G", page_icon="🤖", layout="wide")

if 'dados' not in st.session_state:
    st.session_state.dados = carregar_dados()

dados = st.session_state.dados
estagnado = verificar_estagnacao(dados)

avisos_ghost = verificar_ghost(dados)
for aviso in avisos_ghost:
    st.success(aviso)

atualizar_incorruptivel(dados)
verificar_reset_madrugador(dados)
verificar_mes_cultura(dados)
aplicar_sorte_diaria(dados)
gerar_missoes_diarias(dados)
sorte_ativa = dados["sorte_dia"]["efeito"]

if "msg_cultura" in st.session_state:
    st.success(st.session_state["msg_cultura"])
    del st.session_state["msg_cultura"]

# Navegação Lateral
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Ir para:", ["Painel Principal", "Estudo", "Cultura"])

if pagina == "Estudo":
    st.title("📚 Painel de Estudo")
    
    hoje_str = str(datetime.now().date())
    semana_passada_str = str(datetime.now().date() - timedelta(days=7))
    
    p_hoje = dados["historico_diario"].get(hoje_str, {}).get("pomodoros", 0.0)
    p_passado = dados["historico_diario"].get(semana_passada_str, {}).get("pomodoros", 0.0)
    
    meta_ghost = min(p_passado + 1.0, 8.0)
    horas_hoje = (p_hoje * 42) / 60
    horas_passado = (p_passado * 42) / 60
    
    col_ghost1, col_ghost2 = st.columns(2)
    with col_ghost1:
        st.metric("Hoje (Sessões equivalentes)", f"{p_hoje:.1f}", f"{horas_hoje:.1f} horas")
    with col_ghost2:
        st.metric("Ghost: Mesmo dia da sem. anterior", f"{p_passado:.1f}", f"{horas_passado:.1f} horas", delta_color="off")
        
    st.caption(f"Meta para vencer o Ghost hoje: **{meta_ghost:.1f} sessões equivalentes**. (Recompensa: +30$)")
    st.divider()

    st.markdown("<h2 style='text-align: center;'>⏱️ Timer Pomodoro</h2>", unsafe_allow_html=True)
    
    c_time_sel1, c_time_sel2, c_time_sel3 = st.columns([1, 1, 1])
    with c_time_sel2:
        tempo_minutos = st.number_input("Duração da sessão (minutos)", min_value=1, max_value=300, value=42, step=1)
        
    st.markdown("<p style='text-align: center; color: #8a8a9d;'>Mantenha esta página aberta. Sair da aba cancelará a contagem.</p>", unsafe_allow_html=True)
    
    placeholder = st.empty()
    placeholder.markdown(f"<h1 style='text-align: center; font-size: 100px; padding: 30px 0;'>{tempo_minutos:02d}:00</h1>", unsafe_allow_html=True)
    
    col_vazia1, col_btn_timer, col_vazia2 = st.columns([1, 1, 1])
    with col_btn_timer:
        iniciar = st.button("Iniciar Foco", use_container_width=True)
        
    if iniciar:
        tempo_total = int(tempo_minutos * 60)
        for i in range(tempo_total, -1, -1):
            mins, secs = divmod(i, 60)
            placeholder.markdown(f"<h1 style='text-align: center; font-size: 100px; padding: 30px 0; color: #ff4b4b;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
        fator_proporcao = tempo_minutos / 42.0
        
        s_base = 15
        if sorte_ativa == "Dia de Sorte":
            s_base += 5
            
        s_final = int(s_base * fator_proporcao)
        x_final = int(10 * fator_proporcao)
        
        alterar_valor(dados, "Pomodoro", s_final, x_final, "soma", qtd_sessoes=fator_proporcao)
        placeholder.markdown("<h1 style='text-align: center; font-size: 60px; padding: 30px 0; color: #00E676;'>Concluído!</h1>", unsafe_allow_html=True)
        time.sleep(2)
        st.rerun()

    renderizar_todo_list()

    mes_atual = datetime.now().strftime("%Y-%m")
    total_pomodoros_mes = sum(v.get("pomodoros", 0.0) for k, v in dados.get("historico_diario", {}).items() if k.startswith(mes_atual))
    horas_mes = (total_pomodoros_mes * 42) / 60

    st.markdown(f"""
        <div style="position: fixed; bottom: 70px; right: 10px; background-color: #1a1a2e; padding: 10px 15px; border-radius: 8px; border: 1px solid #00E5FF; z-index: 100; box-shadow: 0 4px 6px rgba(0,0,0,0.5);">
            <h5 style="margin:0; color:#00E5FF; font-size:14px;">📅 Mês Atual</h5>
            <h3 style="margin:0; color:white;">{horas_mes:.1f} horas</h3>
        </div>
    """, unsafe_allow_html=True)


elif pagina == "Cultura":
    st.title("🎭 Cultura Mensal")
    st.markdown("Registre os filmes e livros consumidos neste mês. Os bônus são creditados automaticamente no primeiro dia do mês seguinte.")
    
    col_filmes, col_livros = st.columns(2)
    
    with col_filmes:
        st.subheader(f"🎬 Filmes Assistidos ({len(dados['cultura']['filmes'])})")
        with st.form("form_filme", clear_on_submit=True):
            nome_f = st.text_input("Nome do Filme")
            nota_f = st.slider("Nota", 1, 5, 3, key="nota_f")
            sub_f = st.form_submit_button("Adicionar Filme")
            if sub_f and nome_f.strip():
                dados["cultura"]["filmes"].append({"nome": nome_f.strip(), "nota": nota_f})
                salvar_dados(dados)
                st.rerun()
                
        for f in dados["cultura"]["filmes"]:
            st.markdown(f"- **{f['nome']}** {'⭐' * f['nota']}")

    with col_livros:
        st.subheader(f"📚 Livros Lidos ({len(dados['cultura']['livros'])})")
        with st.form("form_livro", clear_on_submit=True):
            nome_l = st.text_input("Nome do Livro")
            nota_l = st.slider("Nota", 1, 5, 3, key="nota_l")
            sub_l = st.form_submit_button("Adicionar Livro")
            if sub_l and nome_l.strip():
                dados["cultura"]["livros"].append({"nome": nome_l.strip(), "nota": nota_l})
                salvar_dados(dados)
                st.rerun()
                
        for l in dados["cultura"]["livros"]:
            st.markdown(f"- **{l['nome']}** {'⭐' * l['nota']}")
            
    st.divider()
    prev_s = (len(dados['cultura']['filmes']) * 20) + (len(dados['cultura']['livros']) * 50)
    prev_x = (len(dados['cultura']['filmes']) * 20) + (len(dados['cultura']['livros']) * 50)
    st.info(f"**Bônus Acumulado para o fim do mês:** +{prev_s}$ e +{prev_x}XP")

elif pagina == "Painel Principal":
    st.title("🎮 Sistema de Gamificação")

    st.markdown(f"""
    <style>
    .metric-container {{ display: flex; justify-content: space-between; gap: 15px; margin-bottom: 20px; }}
    .metric-card {{ flex: 1; background-color: #1a1a2e; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #2e2e48; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
    .metric-card h4 {{ margin: 0; color: #8a8a9d; font-size: 14px; text-transform: uppercase; letter-spacing: 1.5px; }}
    .metric-card h2 {{ margin: 10px 0 0 0; font-size: 32px; font-weight: 800; }}
    .card-saldo h2 {{ color: #FFD700; text-shadow: 0 0 10px rgba(255, 215, 0, 0.3); }}
    .card-xp h2 {{ color: #00E5FF; text-shadow: 0 0 10px rgba(0, 229, 255, 0.3); }}
    .card-nivel h2 {{ color: #B388FF; text-shadow: 0 0 10px rgba(179, 136, 255, 0.3); }}
    .card-cupons h2 {{ color: #00E676; text-shadow: 0 0 10px rgba(0, 230, 118, 0.3); }}
    .card-streak h2 {{ color: #ff4b4b; text-shadow: 0 0 10px rgba(255, 75, 75, 0.3); }}
    </style>

    <div class="metric-container">
        <div class="metric-card card-saldo"><h4>Saldo 💰</h4><h2>{dados['saldo']} $</h2></div>
        <div class="metric-card card-xp"><h4>XP ⚡</h4><h2>{dados['xp']} / {XP_POR_NIVEL}</h2></div>
        <div class="metric-card card-nivel"><h4>Nível 🌟</h4><h2>{dados['nivel']}</h2></div>
        <div class="metric-card card-cupons"><h4>Cupons 🎫</h4><h2>{dados['cupons']}</h2></div>
        <div class="metric-card card-streak"><h4>Streak 🔥</h4><h2>{dados['streak']}</h2></div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(min(dados['xp'] / XP_POR_NIVEL, 1.0))
    st.divider()

    aplicar_desconto = st.toggle("Ativar Cupom (20% OFF)") if dados['cupons'] > 0 else False

    col_ganhos, col_gastos, col_punicao = st.columns(3)

    with col_ganhos:
        st.subheader("📈 Ganhos")
        config_ganhos = {
            "Pomodoro (Manual)": (15, 10), "Tópicos Concluídos": (30, 50),
            "Banho / Dentes": (5, 5), "Lixo": (5, 20),
            "Lavar roupas": (10, 10), "Limpar casa": (100, 100), "Fazer comida": (5, 5),
            "Atualizar agenda": (1, 2)
        }
        for nome, (s, x) in config_ganhos.items():
            s_final, x_final = s, x
            nome_chave = "Pomodoro" if "Pomodoro" in nome else nome
            if nome_chave == "Pomodoro" and sorte_ativa == "Dia de Sorte": s_final += 5
            if nome_chave == "Tópicos Concluídos" and sorte_ativa == "Foco Total": x_final *= 2
            if nome_chave in ["Lixo", "Lavar roupas", "Limpar casa"] and sorte_ativa == "Limpinho": s_final *= 2

            c_btn, c_rev = st.columns([0.8, 0.2])
            if c_btn.button(f"{nome} (+{s_final}$/ +{x_final}XP)", use_container_width=True):
                alterar_valor(dados, nome_chave, s_final, x_final, "soma")
            if c_rev.button("➖", key=f"rev_{nome}", use_container_width=True):
                alterar_valor(dados, nome_chave, s_final, x_final, "subtracao")
            st.caption(f"Concluídos: {dados['contadores'].get(nome_chave, 0)}")

        st.markdown("##### 📚 Culturais Diários (1x)")
        hoje_str = str(datetime.now().date())
        c_not, c_pag = st.columns(2)
        
        with c_not:
            if dados["limites_diarios"]["noticias"] == hoje_str:
                st.button("📰 Notícias", disabled=True, use_container_width=True)
            else:
                if st.button("📰 Notícias (+5$/+15XP)", use_container_width=True):
                    dados["limites_diarios"]["noticias"] = hoje_str
                    alterar_valor(dados, "Noticias", 5, 15, "soma")
        with c_pag:
            if dados["limites_diarios"]["paginas"] == hoje_str:
                st.button("📖 10 Páginas", disabled=True, use_container_width=True)
            else:
                if st.button("📖 10 Pág. (+10$/+15XP)", use_container_width=True):
                    dados["limites_diarios"]["paginas"] = hoje_str
                    alterar_valor(dados, "Paginas", 10, 15, "soma")

    with col_gastos:
        st.subheader("🛒 Loja")
        itens_loja = {"60m de Jogo": 30, "Delivery": 250, "Cosmético": 1200, "Ver filme": 50}
        for item, preco_base in itens_loja.items():
            preco_final = preco_base
            if sorte_ativa == "Inflação": preco_final = int(preco_final * 1.2)
            if item == "Ver filme" and sorte_ativa == "Dia de Cinema": preco_final = 30
            if aplicar_desconto: preco_final = int(preco_final * 0.8)

            if st.button(f"{item} (-{preco_final}$)", use_container_width=True):
                if dados['saldo'] >= preco_final:
                    dados['saldo'] -= preco_final
                    if aplicar_desconto: dados['cupons'] -= 1
                    dados["contadores"][f"Gasto_{item}"] = dados["contadores"].get(f"Gasto_{item}", 0) + 1
                    salvar_dados(dados)
                    st.rerun()
                else: st.error("Saldo insuficiente!")
            st.caption(f"Requisitados: {dados['contadores'].get(f'Gasto_{item}', 0)}")

    with col_punicao:
        st.subheader("⚠️ Punições")
        punicoes = {"Rede Social": 25, "Gasto Inútil": 100}
        for p, v in punicoes.items():
            v_final = v * 3 if sorte_ativa == "Não faça isso" else v
            if st.button(f"{p} (-{v_final}$)", use_container_width=True):
                dados['saldo'] -= v_final
                dados["contadores"][f"P_{p}"] = dados["contadores"].get(f"P_{p}", 0) + 1
                dados["ultima_punicao_data"] = str(datetime.now().date())
                dados["conquistas"]["incorruptivel"]["atual"] = 0
                salvar_dados(dados)
                st.rerun()
            st.caption(f"Ocorrências: {dados['contadores'].get(f'P_{p}', 0)}")

    # ACORDAR CEDO
    st.divider()
    hoje_dt = datetime.now().date()
    agora = datetime.now().time()
    limite = datetime.strptime("06:15", "%H:%M").time()

    c_ac_1, c_ac_2, c_ac_3 = st.columns([1, 2, 1])
    with c_ac_2:
        st.markdown("<h3 style='text-align: center; color: #FFD700;'>✨ Recompensa Especial ✨</h3>", unsafe_allow_html=True)
        if dados.get("ultimo_acordar_cedo") == str(hoje_dt):
            st.button("☀️ Acordar Cedo (Resgatado)", disabled=True, use_container_width=True)
        else:
            if st.button("☀️ Acordar Cedo (+25$/ +25XP)", use_container_width=True):
                if agora <= limite:
                    dados["ultimo_acordar_cedo"] = str(hoje_dt)
                    
                    # A lógica da conquista deve vir antes de alterar_valor
                    dados["conquistas"]["madrugador"]["ultima_data"] = str(hoje_dt)
                    dados["conquistas"]["madrugador"]["atual"] += 1
                    if dados["conquistas"]["madrugador"]["atual"] >= 10:
                        dados["saldo"] += 150
                        dados["conquistas"]["madrugador"]["completadas"] += 1
                        dados["conquistas"]["madrugador"]["data_conclusao"] = str(hoje_dt)
                        dados["conquistas"]["madrugador"]["atual"] = 0
                    
                    alterar_valor(dados, "Acordar Cedo", 25, 25, "soma")
            else: 
                st.error("Passou do horário!")

    # MISSÕES DIÁRIAS
    st.divider()
    st.markdown("<h3 style='text-align: center;'>🎯 Missões Diárias</h3>", unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)
    colunas_missoes = [col_m1, col_m2, col_m3]

    for i, missao in enumerate(dados["missoes_diarias"]["missoes"]):
        with colunas_missoes[i]:
            st.markdown(f"<div style='background-color: #262730; padding: 15px; border-radius: 8px; height: 100%;'>", unsafe_allow_html=True)
            st.markdown(f"**{missao['desc']}**")
            st.caption(f"Recompensa: +{missao['s']}$ | +{missao['x']}XP")
            
            if missao["concluida"]:
                st.success("✅ Concluída!")
            else:
                if st.button("Concluir", key=f"btn_missao_{i}", use_container_width=True):
                    missao["concluida"] = True
                    alterar_valor(dados, "Missao Diaria", missao['s'], missao['x'], "soma")
            st.markdown("</div>", unsafe_allow_html=True)

    # SORTE DIÁRIA E CONQUISTAS ÚNICAS
    st.divider()
    col_sorte, col_conquistas = st.columns(2)

    with col_sorte:
        st.markdown(f"""
            <div style="text-align: center; padding: 20px; border: 2px dashed #4e4e4e; border-radius: 10px;">
                <h4 style="margin: 0;">🎲 Sua Sorte Diária em {dados['sorte_dia']['data']}:</h4>
                <p style="font-size: 1.2em; color: #00ffcc; font-weight: bold;">{dados['sorte_dia']['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_conquistas:
        st.subheader("🏆 Conquistas Únicas")
        
        mad_hoje = dados["conquistas"]["madrugador"]["data_conclusao"] == str(hoje_dt)
        mad_atual = 10 if mad_hoje else dados["conquistas"]["madrugador"]["atual"]
        mad_color = "#FFD700" if mad_hoje else "white"
        
        st.markdown(f"<p style='color: {mad_color}; font-weight: bold; margin-bottom: 0;'>🌅 Madrugador (Acordar antes das 06:15 por 10 dias)</p>", unsafe_allow_html=True)
        st.progress(mad_atual / 10.0)
        st.caption(f"Progresso: {mad_atual} / 10 | Completadas: {dados['conquistas']['madrugador']['completadas']}")
        
        inc_hoje = dados["conquistas"]["incorruptivel"]["data_conclusao"] == str(hoje_dt)
        inc_atual = 3 if inc_hoje else dados["conquistas"]["incorruptivel"]["atual"]
        inc_color = "#FFD700" if inc_hoje else "white"
        
        st.markdown(f"<p style='color: {inc_color}; font-weight: bold; margin-bottom: 0; margin-top: 15px;'>🛡️ Incorruptível (3 dias sem punição)</p>", unsafe_allow_html=True)
        st.progress(inc_atual / 3.0)
        st.caption(f"Progresso: {inc_atual} / 3 | Completadas: {dados['conquistas']['incorruptivel']['completadas']}")

    # SEÇÃO DE GRÁFICOS SEMANAIS
    st.divider()
    inicio_semana = hoje_dt - timedelta(days=6)
    st.markdown(f"<h3 style='text-align: center;'>📊 Resumo da Semana ({inicio_semana.strftime('%d/%m')} a {hoje_dt.strftime('%d/%m')})</h3>", unsafe_allow_html=True)

    dias_pt = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    dados_grafico = []

    for i in range(7):
        dia_atual = inicio_semana + timedelta(days=i)
        dia_str = str(dia_atual)
        nome_dia = dias_pt[dia_atual.weekday()]
        
        historico = dados.get("historico_diario", {}).get(dia_str, {"pomodoros": 0.0, "moedas_ganhas": 0})
        dados_grafico.append({
            "Dia": f"{dia_atual.strftime('%d/%m')} - {nome_dia}",
            "Pomodoros (Sessões)": historico["pomodoros"],
            "Moedas Geradas": historico["moedas_ganhas"]
        })

    df_grafico = pd.DataFrame(dados_grafico).set_index("Dia")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("<p style='text-align: center; color: #ff4b4b; font-weight: bold;'>🍅 Sessões Equivalentes Realizadas</p>", unsafe_allow_html=True)
        st.bar_chart(df_grafico["Pomodoros (Sessões)"], color="#ff4b4b")

    with col_g2:
        st.markdown("<p style='text-align: center; color: #FFD700; font-weight: bold;'>💰 Moedas Geradas</p>", unsafe_allow_html=True)
        st.bar_chart(df_grafico["Moedas Geradas"], color="#FFD700")

if dados['xp'] >= XP_POR_NIVEL:
    dados['xp'] -= XP_POR_NIVEL
    dados['nivel'] += 1
    dados['cupons'] += 1
    salvar_dados(dados)
    st.rerun()

st.sidebar.divider()
if st.sidebar.button("Resetar Tudo"):
    st.session_state.dados = {
        "saldo": 0, "xp": 0, "nivel": 1, "cupons": 0, "contadores": {}, "streak": 0,
        "ultima_atividade": str(datetime.now().date() - timedelta(days=1)),
        "ultimo_registro_full": str(datetime.now()),
        "ultimo_acordar_cedo": str(datetime.now().date() - timedelta(days=1)),
        "ultimo_ghost_check": str(datetime.now().date() - timedelta(days=1)),
        "sorte_dia": {"data": "", "efeito": None},
        "ultima_punicao_data": "",
        "historico_diario": {},
        "missoes_diarias": {"data": "", "missoes": []},
        "limites_diarios": {"noticias": "", "paginas": ""},
        "cultura": {
            "mes_referencia": datetime.now().strftime("%Y-%m"),
            "filmes": [],
            "livros": []
        },
        "conquistas": {
            "madrugador": {"atual": 0, "total": 10, "completadas": 0, "ultima_data": str(datetime.now().date() - timedelta(days=1)), "data_conclusao": ""},
            "incorruptivel": {"atual": 0, "total": 3, "completadas": 0, "ultima_verificacao": str(datetime.now().date()), "data_conclusao": ""}
        }
    }
    salvar_dados(st.session_state.dados)
    st.rerun()

st.markdown(f"""
    <div style="position: fixed; bottom: 10px; right: 10px; background-color: #262730; padding: 10px; border-radius: 5px; border: 1px solid #464b5d; z-index: 100;">🎫 Cupons: {dados['cupons']}</div>
    """, unsafe_allow_html=True)
