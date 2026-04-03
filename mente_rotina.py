import streamlit as st
import time
import uuid
import requests
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import core

FIREBASE_URL_TAREFAS = "https://gamix2-57898-default-rtdb.firebaseio.com/tarefas.json"

def carregar_tarefas():
    try:
        resposta = requests.get(FIREBASE_URL_TAREFAS)
        if resposta.status_code == 200 and resposta.json() is not None:
            return resposta.json()
    except Exception:
        pass
    return []

def salvar_tarefas(tarefas):
    requests.put(FIREBASE_URL_TAREFAS, json=tarefas)

def renderizar(dados):
    st.title("🧠 Mente e Rotina")
    sorte_ativa = dados.get("sorte_dia", {}).get("efeito")
    agora_br = datetime.utcnow() - timedelta(hours=3)
    hoje_str = str(agora_br.date())

    # Garantia de estrutura para limites diários
    if "limites_diarios" not in dados:
        dados["limites_diarios"] = {}
        
    if dados["limites_diarios"].get("agua_data") != hoje_str:
        dados["limites_diarios"]["agua_data"] = hoje_str
        dados["limites_diarios"]["agua_count"] = 0

    # ==========================================
    # HÁBITOS EM DESTAQUE
    # ==========================================
    st.markdown("""
        <div style="background-color: #1a1a2e; padding: 15px; border-radius: 10px; border-left: 5px solid #FFD700; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #FFD700;">🌟 Hábitos em Destaque</h3>
            <p style="margin: 5px 0 0 0; color: #8a8a9d; font-size: 14px;">Tarefas prioritárias para o seu dia.</p>
        </div>
    """, unsafe_allow_html=True)

    col_destaque1, col_destaque2 = st.columns(2)
    
    with col_destaque1:
        if dados["limites_diarios"].get("paginas") == hoje_str:
            st.button("📖 10 Páginas (Concluído)", disabled=True, use_container_width=True)
        else:
            if st.button("📖 Ler 10 Pág. (+10$/+15XP)", type="primary", use_container_width=True):
                dados["limites_diarios"]["paginas"] = hoje_str
                core.alterar_valor(dados, "Paginas", 10, 15, "soma")

    with col_destaque2:
        count_agua = dados["limites_diarios"].get("agua_count", 0)
        if count_agua >= 3:
            st.button("💧 Garrafa Cheia (3/3)", disabled=True, use_container_width=True)
        else:
            if st.button(f"💧 Encher Garrafa (+2$/+2XP) [{count_agua}/3]", type="primary", use_container_width=True):
                dados["limites_diarios"]["agua_count"] += 1
                core.alterar_valor(dados, "Garrafa de Agua", 2, 2, "soma")

    # ==========================================
    # ROTINA DIÁRIA (1X)
    # ==========================================
    st.markdown("""
        <div style="background-color: #1a1a2e; padding: 15px; border-radius: 10px; border-left: 5px solid #00E5FF; margin-bottom: 20px; margin-top: 10px;">
            <h3 style="margin: 0; color: #00E5FF;">📋 Rotina Diária</h3>
            <p style="margin: 5px 0 0 0; color: #8a8a9d; font-size: 14px;">Ações únicas diárias.</p>
        </div>
    """, unsafe_allow_html=True)

    col_rotina1, col_rotina2 = st.columns(2)
    
    with col_rotina1:
        if dados["limites_diarios"].get("agenda") == hoje_str:
            st.button("📅 Agenda Atualizada", disabled=True, use_container_width=True)
        else:
            if st.button("📅 Atualizar Agenda (+1$/+2XP)", use_container_width=True):
                dados["limites_diarios"]["agenda"] = hoje_str
                core.alterar_valor(dados, "Atualizar agenda", 1, 2, "soma")
                
    with col_rotina2:
        if dados["limites_diarios"].get("noticias") == hoje_str:
            st.button("📰 Notícias (Lido)", disabled=True, use_container_width=True)
        else:
            if st.button("📰 Ler Notícias (+5$/+15XP)", use_container_width=True):
                dados["limites_diarios"]["noticias"] = hoje_str
                core.alterar_valor(dados, "Noticias", 5, 15, "soma")

    # ==========================================
    # TAREFAS GERAIS
    # ==========================================
    with st.expander("🏠 Tarefas Gerais e Operacionais", expanded=False):
        config_ganhos = {
            "Pomodoro (Manual)": (15, 10), "Tópicos Concluídos": (30, 50),
            "Banho / Dentes": (5, 5), "Lixo": (5, 20),
            "Lavar roupas": (10, 10), "Limpar casa": (100, 100), "Fazer comida": (5, 5)
        }
        for nome, (s, x) in config_ganhos.items():
            s_final, x_final = s, x
            nome_chave = "Pomodoro" if "Pomodoro" in nome else nome
            if nome_chave == "Pomodoro" and sorte_ativa == "Dia de Sorte": s_final += 5
            if nome_chave == "Tópicos Concluídos" and sorte_ativa == "Foco Total": x_final *= 2
            if nome_chave in ["Lixo", "Lavar roupas", "Limpar casa"] and sorte_ativa == "Limpinho": s_final *= 2

            c_btn, c_rev, c_cap = st.columns([0.6, 0.1, 0.3])
            if c_btn.button(f"{nome} (+{s_final}$/ +{x_final}XP)", use_container_width=True, key=f"btn_{nome}"):
                core.alterar_valor(dados, nome_chave, s_final, x_final, "soma")
            if c_rev.button("➖", key=f"rev_{nome}", use_container_width=True):
                core.alterar_valor(dados, nome_chave, s_final, x_final, "subtracao")
            c_cap.caption(f"Registros: {dados['contadores'].get(nome_chave, 0)}")

    st.divider()

    # ==========================================
    # POMODORO / CRONÔMETRO PROGRESSIVO
    # ==========================================
    semana_passada_str = str(agora_br.date() - timedelta(days=7))
    p_hoje = dados["historico_diario"].get(hoje_str, {}).get("pomodoros", 0.0)
    p_passado = dados["historico_diario"].get(semana_passada_str, {}).get("pomodoros", 0.0)
    meta_ghost = min(p_passado + 1.0, 8.0)
    
    col_ghost1, col_ghost2 = st.columns(2)
    with col_ghost1:
        st.metric("Hoje (Sessões equivalentes)", f"{p_hoje:.1f}", f"{(p_hoje * 42) / 60:.1f} horas")
    with col_ghost2:
        st.metric("Ghost (Semana anterior)", f"{p_passado:.1f}", f"{(p_passado * 42) / 60:.1f} horas", delta_color="off")
        
    st.caption(f"Meta para vencer o Ghost hoje: **{meta_ghost:.1f} sessões equivalentes**. (+30$)")
    
    st.markdown("<h2 style='text-align: center;'>⏱️ Timer Progressivo</h2>", unsafe_allow_html=True)
    if st.session_state.inicio_cronometro is None:
        col_vazia1, col_btn_timer, col_vazia2 = st.columns([1, 1, 1])
        with col_btn_timer:
            if st.button("▶️ Iniciar Estudo", use_container_width=True):
                st.session_state.inicio_cronometro = time.time()
                st.rerun()
    else:
        components.html(f"""
        <div id="clock" style="color:#ff4b4b; font-size: 100px; text-align: center; font-family: sans-serif; font-weight: bold; margin-top: 20px;">00:00</div>
        <script>
            var start = {st.session_state.inicio_cronometro};
            setInterval(function() {{
                var now = Date.now() / 1000;
                var diff = Math.floor(now - start);
                var m = Math.floor(diff / 60).toString().padStart(2, '0');
                var s = (diff % 60).toString().padStart(2, '0');
                document.getElementById('clock').innerHTML = m + ":" + s;
            }}, 1000);
        </script>
        """, height=160)
        
        col_stop, col_cancel = st.columns(2)
        with col_stop:
            if st.button("⏹️ Concluir e Salvar", use_container_width=True):
                decorrido_segundos = time.time() - st.session_state.inicio_cronometro
                minutos_estudados = decorrido_segundos / 60.0
                st.session_state.inicio_cronometro = None
                
                fator_proporcao = minutos_estudados / 42.0
                s_base = 15
                if sorte_ativa == "Dia de Sorte":
                    s_base += 5
                    
                s_final = int(s_base * fator_proporcao)
                x_final = int(10 * fator_proporcao)
                
                core.alterar_valor(dados, "Pomodoro", s_final, x_final, "soma", qtd_sessoes=fator_proporcao, rerun=False)
                st.success(f"Concluído! {minutos_estudados:.1f} minutos registrados.")
                time.sleep(2)
                st.rerun()
        with col_cancel:
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.inicio_cronometro = None
                st.rerun()

    mes_atual = agora_br.strftime("%Y-%m")
    total_pomodoros_mes = sum(v.get("pomodoros", 0.0) for k, v in dados.get("historico_diario", {}).items() if k.startswith(mes_atual))
    horas_mes = (total_pomodoros_mes * 42) / 60

    st.markdown(f"""
        <div style="position: fixed; bottom: 70px; right: 10px; background-color: #1a1a2e; padding: 10px 15px; border-radius: 8px; border: 1px solid #00E5FF; z-index: 100; box-shadow: 0 4px 6px rgba(0,0,0,0.5);">
            <h5 style="margin:0; color:#00E5FF; font-size:14px;">📅 Mês Atual</h5>
            <h3 style="margin:0; color:white;">{horas_mes:.1f} horas</h3>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # TO-DO LIST
    # ==========================================
    st.divider()
    st.markdown("<h3 style='text-align: center;'>📝 Lista de Tarefas</h3>", unsafe_allow_html=True)

    if "tarefas" not in st.session_state:
        st.session_state.tarefas = carregar_tarefas()

    with st.expander("Adicionar Nova Tarefa", expanded=True):
        col_nome, col_data = st.columns([0.7, 0.3])
        with col_nome:
            nova_tarefa = st.text_input("Nome da tarefa:")
        with col_data:
            nova_data = st.date_input("Data:")
            
        col_pri, col_cor, col_btn = st.columns([0.4, 0.3, 0.3])
        with col_pri:
            nova_prioridade = st.selectbox("Prioridade (0 é mais urgente):", [0, 1, 2])
        with col_cor:
            nova_cor = st.color_picker("Cor da Etiqueta:", "#FF4B4B")
        with col_btn:
            st.write("") 
            st.write("")
            if st.button("Adicionar Tarefa", use_container_width=True):
                if nova_tarefa.strip():
                    st.session_state.tarefas.append({
                        "id": str(uuid.uuid4()),
                        "nome": nova_tarefa.strip(),
                        "data": str(nova_data),
                        "prioridade": nova_prioridade,
                        "cor": nova_cor
                    })
                    salvar_tarefas(st.session_state.tarefas)
                    st.rerun()

    if st.session_state.tarefas:
        ordenacao = st.radio("Ordenar por:", ["Adição", "Prioridade", "Data"], horizontal=True)
        tarefas_display = st.session_state.tarefas.copy()
        if ordenacao == "Prioridade":
            tarefas_display.sort(key=lambda x: x.get("prioridade", 2))
        elif ordenacao == "Data":
            tarefas_display.sort(key=lambda x: x.get("data", "9999-12-31"))
    else:
        tarefas_display = []

    tarefas_restantes = st.session_state.tarefas.copy()
    houve_alteracao = False

    st.write("")
    for tarefa in tarefas_display:
        t_id = tarefa["id"]
        nome = tarefa.get("nome", "")
        cor = tarefa.get("cor", "#ffffff")
        pri = tarefa.get("prioridade", 2)
        data_t = tarefa.get("data", "")
        
        col1, col2 = st.columns([0.90, 0.10])
        with col1:
            st.markdown(f"""
            <div style="border-left: 5px solid {cor}; padding-left: 10px; margin-bottom: 5px; background-color: #262730; padding: 10px; border-radius: 5px;">
                <strong style="font-size: 16px;">{nome}</strong><br>
                <span style="font-size: 13px; color: #8a8a9d;">Prioridade: {pri} | Data: {datetime.strptime(data_t, '%Y-%m-%d').strftime('%d/%m/%Y')}</span>
            </div>
            """, unsafe_allow_html=True)
            concluida = st.checkbox("Concluir", key=f"chk_{t_id}")
        with col2:
            st.write("")
            remover = st.button("🗑️", key=f"del_{t_id}", help="Remover tarefa")
        
        if concluida or remover:
            tarefas_restantes = [t for t in tarefas_restantes if t["id"] != t_id]
            houve_alteracao = True

    if houve_alteracao:
        st.session_state.tarefas = tarefas_restantes
        salvar_tarefas(st.session_state.tarefas)
        st.rerun()
