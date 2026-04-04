import requests
import random
import time
import streamlit as st
from datetime import datetime, timedelta

FIREBASE_URL_DADOS = "https://gamix2-57898-default-rtdb.firebaseio.com/status_usuario.json"
XP_POR_NIVEL = 300

def carregar_dados():
    import streamlit as st
    agora_br = datetime.utcnow() - timedelta(hours=3)
    try:
        resposta = requests.get(FIREBASE_URL_DADOS, timeout=10)
        resposta.raise_for_status() 
        dados_firebase = resposta.json()

        if dados_firebase is not None:
            dados = dados_firebase
            novas_chaves = {
                "streak": 0,
                "ultima_atividade": str(agora_br.date() - timedelta(days=1)),
                "ultimo_registro_full": str(agora_br),
                "ultimo_acordar_cedo": str(agora_br.date() - timedelta(days=1)),
                "ultimo_ghost_check": str(agora_br.date() - timedelta(days=1)),
                "ultima_verificacao_estudo": str(agora_br.date()),
                "ultima_verificacao_aula": str(agora_br.date()),
                "contadores": {},
                "sorte_dia": {"data": "", "efeito": None},
                "ultima_punicao_data": "",
                "historico_diario": {},
                "missoes_diarias": {"data": "", "missoes": []},
                "limites_diarios": {"noticias": "", "paginas": ""},
                "cultura": {
                    "mes_referencia": agora_br.strftime("%Y-%m"),
                    "filmes": [],
                    "livros": []
                }
            }
            for k, v in novas_chaves.items():
                if k not in dados: dados[k] = v
            
            if "cultura" not in dados:
                dados["cultura"] = {"mes_referencia": agora_br.strftime("%Y-%m"), "filmes": [], "livros": []}
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
                    "madrugador": {"atual": 0, "total": 10, "completadas": 0, "ultima_data": str(agora_br.date() - timedelta(days=1)), "data_conclusao": ""},
                    "incorruptivel": {"atual": 0, "total": 3, "completadas": 0, "ultima_verificacao": str(agora_br.date()), "data_conclusao": ""}
                }
            return dados
        else:
            pass 

    except requests.exceptions.RequestException:
        st.error("🚨 Falha de conexão com o banco de dados. Para evitar a sobrescrita por um perfil zerado, o sistema foi paralisado. Recarregue a página.")
        st.stop()
    except Exception as e:
        st.error(f"🚨 Erro crítico ao processar dados: {e}")
        st.stop()
        
    return {
        "saldo": 0, "xp": 0, "nivel": 1, "cupons": 0, "contadores": {}, "streak": 0,
        "ultima_atividade": str(agora_br.date() - timedelta(days=1)),
        "ultimo_registro_full": str(agora_br),
        "ultimo_acordar_cedo": str(agora_br.date() - timedelta(days=1)),
        "ultimo_ghost_check": str(agora_br.date() - timedelta(days=1)),
        "ultima_verificacao_estudo": str(agora_br.date()),
        "ultima_verificacao_aula": str(agora_br.date()),
        "sorte_dia": {"data": "", "efeito": None},
        "ultima_punicao_data": "",
        "historico_diario": {},
        "missoes_diarias": {"data": "", "missoes": []},
        "limites_diarios": {"noticias": "", "paginas": ""},
        "cultura": {
            "mes_referencia": agora_br.strftime("%Y-%m"),
            "filmes": [],
            "livros": []
        },
        "conquistas": {
            "madrugador": {"atual": 0, "total": 10, "completadas": 0, "ultima_data": str(agora_br.date() - timedelta(days=1)), "data_conclusao": ""},
            "incorruptivel": {"atual": 0, "total": 3, "completadas": 0, "ultima_verificacao": str(agora_br.date()), "data_conclusao": ""}
        }
    }

def salvar_dados(dados):
    """ Tenta salvar no Firebase. Se falhar após 3 tentativas, trava a tela. """
    for _ in range(3):
        try:
            resposta = requests.put(FIREBASE_URL_DADOS, json=dados, timeout=5)
            if resposta.status_code == 200:
                return True
        except Exception:
            time.sleep(0.5)
            
    st.error("🚨 **FALHA DE SINCRONIZAÇÃO:** O servidor não confirmou o recebimento dos dados. Não recarregue a página, aguarde alguns segundos e tente clicar novamente na sua ação.")
    st.stop()
    return False

def verificar_estagnacao(dados, session_state):
    agora = datetime.utcnow() - timedelta(hours=3)
    ultima = datetime.fromisoformat(dados["ultimo_registro_full"])
    estagnado = agora - ultima > timedelta(hours=24)
    if estagnado:
        if session_state.get('punicao_aplicada') != ultima:
            dados["saldo"] = int(dados["saldo"] * 0.9)
            dados["xp"] = int(dados["xp"] * 0.9)
            dados["ultima_punicao_data"] = str(agora.date())
            dados["conquistas"]["incorruptivel"]["atual"] = 0
            session_state['punicao_aplicada'] = ultima
            salvar_dados(dados)
    return estagnado

def verificar_penalidade_estudo(dados):
    agora_br = datetime.utcnow() - timedelta(hours=3)
    hoje = agora_br.date()
    ultima_verif_str = dados.get("ultima_verificacao_estudo", str(hoje))
    ultima_verif = datetime.strptime(ultima_verif_str, "%Y-%m-%d").date()
    
    avisos = []
    if ultima_verif < hoje:
        while ultima_verif < hoje:
            dia_str = str(ultima_verif)
            p_dia = dados.get("historico_diario", {}).get(dia_str, {}).get("pomodoros", 0.0)
            if p_dia <= 0.0:
                dados["saldo"] -= 50
                avisos.append(f"⚠️ Penalidade aplicada: Você não registrou nenhum estudo no dia {dia_str}. (-50$)")
            ultima_verif += timedelta(days=1)
        dados["ultima_verificacao_estudo"] = str(hoje)
        salvar_dados(dados)
    return avisos

def verificar_penalidade_aula(dados):
    agora_br = datetime.utcnow() - timedelta(hours=3)
    hoje = agora_br.date()
    ultima_verif_str = dados.get("ultima_verificacao_aula", str(hoje))
    ultima_verif = datetime.strptime(ultima_verif_str, "%Y-%m-%d").date()
    
    avisos = []
    if ultima_verif < hoje:
        while ultima_verif < hoje:
            if ultima_verif.weekday() < 5: 
                dia_str = str(ultima_verif)
                foi_aula = dados.get("historico_diario", {}).get(dia_str, {}).get("aula_confirmada", False)
                if not foi_aula:
                    dados["saldo"] -= 60
                    avisos.append(f"⚠️ Penalidade aplicada: Falta não justificada/ausência de check-in na aula do dia {dia_str}. (-60$)")
            ultima_verif += timedelta(days=1)
        dados["ultima_verificacao_aula"] = str(hoje)
        salvar_dados(dados)
    return avisos

def verificar_ghost(dados):
    hoje = (datetime.utcnow() - timedelta(hours=3)).date()
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
    hoje = (datetime.utcnow() - timedelta(hours=3)).date()
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
    hoje = (datetime.utcnow() - timedelta(hours=3)).date()
    ultima_str = dados["conquistas"]["madrugador"]["ultima_data"]
    ultima = datetime.strptime(ultima_str, "%Y-%m-%d").date()
    if hoje > ultima + timedelta(days=1):
        dados["conquistas"]["madrugador"]["atual"] = 0

def verificar_mes_cultura(dados, session_state):
    mes_atual = (datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m")
    if dados["cultura"]["mes_referencia"] != mes_atual:
        qtd_filmes = len(dados["cultura"]["filmes"])
        qtd_livros = len(dados["cultura"]["livros"])
        
        bonus_s = 0
        bonus_x = 0
        penalidade_s = 0

        if qtd_filmes > 0:
            bonus_s += qtd_filmes * 20
            bonus_x += qtd_filmes * 20
        else:
            penalidade_s += 200

        if qtd_livros > 0:
            bonus_s += qtd_livros * 50
            bonus_x += qtd_livros * 50
        else:
            penalidade_s += 200

        dados["saldo"] += (bonus_s - penalidade_s)
        dados["xp"] += bonus_x

        session_state["msg_cultura"] = f"Mês encerrado! Bônus: +{bonus_s}$, +{bonus_x}XP. Penalidades aplicadas: -{penalidade_s}$."
        
        dados["cultura"]["filmes"] = []
        dados["cultura"]["livros"] = []
        dados["cultura"]["mes_referencia"] = mes_atual
        salvar_dados(dados)

def aplicar_sorte_diaria(dados):
    hoje = str((datetime.utcnow() - timedelta(hours=3)).date())
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
    hoje = str((datetime.utcnow() - timedelta(hours=3)).date())
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
            {"desc": "Assista a um vídeo técnico sobre C++ ou Java", "s": 15, "x": 20},
            {"desc": "Faça um commit em um projeto pessoal", "s": 25, "x": 30},
            {"desc": "Leia um artigo sobre Cybersegurança ou Redes", "s": 15, "x": 20},
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

def alterar_valor(dados, chave, v_saldo, v_xp, operacao="soma", qtd_sessoes=1.0, rerun=True):
    hoje_str = str((datetime.utcnow() - timedelta(hours=3)).date())
    if hoje_str not in dados["historico_diario"]:
        dados["historico_diario"][hoje_str] = {"pomodoros": 0.0, "moedas_ganhas": 0}

    if operacao == "soma":
        hoje = (datetime.utcnow() - timedelta(hours=3)).date()
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
        dados["ultimo_registro_full"] = str(datetime.utcnow() - timedelta(hours=3))
        
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

    if salvar_dados(dados) and rerun:
        st.rerun()
