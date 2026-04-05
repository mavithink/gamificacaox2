import streamlit as st
import time
import uuid
import requests
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import core

FIREBASE_URL_TAREFAS = "https://gamix2-57898-default-rtdb.firebaseio.com/tarefas.json"

def formatar_horas(horas_decimais):
    h = int(horas_decimais)
    m = int(round((horas_decimais - h) * 60))
    if m == 60:
        h += 1
        m = 0
    return f"{h}h{m:02d}"

def carregar_tarefas():
    try:
        resposta = requests.get(FIREBASE_URL_TAREFAS)
        if resposta.status_code == 200 and resposta.json() is not None:
            return resposta.json()
    except Exception:
        pass
    return []

def salvar_tarefas(tarefas):
    for _ in range(3):
        try:
            resposta = requests.put(FIREBASE_URL_TAREFAS, json=tarefas, timeout=5)
            if resposta.status_code == 200:
                return True
        except Exception:
            time.sleep(0.5)
            
    st.error("🚨 FALHA AO SALVAR: As alterações na lista de tarefas não chegaram ao servidor.")
    st.stop()
    return False

def botao_concluido(texto):
    """Renderiza um bloco HTML simulando um botão pressionado em roxo leve."""
    st.markdown(f"""
<div style="background-color: #E8D5EB; border: 3px solid #6e0b8a; color: #6e0b8a; font-family: 'VT323', monospace; font-size: 20px; text-align: center; font-weight: bold; padding: 2px 0;">
{texto}
</div>
    """, unsafe_allow_html=True)

def renderizar(dados):
    if "tarefas" not in st.session_state:
        st.session_state.tarefas = carregar_tarefas()

    sorte_ativa = dados.get("sorte_dia", {}).get("efeito")
    agora_br = datetime.utcnow() - timedelta(hours=3)
    hoje_str = str(agora_br.date())
    mes_atual = agora_br.strftime("%Y-%m")
    inicio_semana = agora_br.date() - timedelta(days=6)

    # ==========================================
    # CÁLCULOS DO HEADER SUPERIOR
    # ==========================================
    saldo_atual = dados.get("saldo", 0)
    tarefas_a_fazer = len(st.session_state.tarefas)
    
    total_pomodoros_mes = sum(v.get("pomodoros", 0.0) for k, v in dados.get("historico_diario", {}).items() if k.startswith(mes_atual))
    horas_mes_dec = (total_pomodoros_mes * 42) / 60
    
    total_pomodoros_semana = sum(dados.get("historico_diario", {}).get(str(inicio_semana + timedelta(days=i)), {}).get("pomodoros", 0.0) for i in range(7))
    horas_semana_dec = (total_pomodoros_semana * 42) / 60
    
    tarefas_semana = sum(dados.get("historico_diario", {}).get(str(inicio_semana + timedelta(days=i)), {}).get("tarefas_concluidas", 0) for i in range(7))

    # HEADER SUPERIOR (TÍTULO + DECORAÇÃO + DADOS)
    # ATENÇÃO: Todo o HTML colado na margem esquerda para evitar erro de Code Block do Markdown
    st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #6e0b8a; margin-bottom: 15px; padding-bottom: 10px;">
<h1 style="margin: 0; border: none; padding: 0; color: #6e0b8a; white-space: nowrap;">🧠 Mente e Rotina</h1>
<div style="flex-grow: 1; text-align: center; color: #6e0b8a; font-size: 24px; padding: 0 15px; letter-spacing: 5px;">✦ • ✦ • ✦</div>
<div style="display: flex; gap: 8px; flex-wrap: wrap; font-family: 'VT323', monospace; font-size: 18px; color: #000000; justify-content: flex-end;">
<div style="background-color: #E8D5EB; border: 2px solid #6e0b8a; padding: 2px 8px;"><strong>Saldo:</strong> {saldo_atual}$</div>
<div style="background-color: #FFFFFF; border: 2px solid #000000; padding: 2px 8px;"><strong>To-Do:</strong> {tarefas_a_fazer} pendentes</div>
<div style="background-color: #FFFFFF; border: 2px solid #000000; padding: 2px 8px;"><strong>H. Semana:</strong> {formatar_horas(horas_semana_dec)}</div>
<div style="background-color: #FFFFFF; border: 2px solid #000000; padding: 2px 8px;"><strong>H. Mês:</strong> {formatar_horas(horas_mes_dec)}</div>
<div style="background-color: #FFFFFF; border: 2px solid #000000; padding: 2px 8px;"><strong>Tarefas (Sem):</strong> {tarefas_semana} concluídas</div>
</div>
</div>
    """, unsafe_allow_html=True)

    if "limites_diarios" not in dados:
        dados["limites_diarios"] = {}
        
    if dados["limites_diarios"].get("agua_data") != hoje_str:
        dados["limites_diarios"]["agua_data"] = hoje_str
        dados["limites_diarios"]["agua_count"] = 0

    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>🌟 Hábitos em Destaque</h3>", unsafe_allow_html=True)
        col_destaque1, col_destaque2 = st.columns(2)
        
        with col_destaque1:
            if dados["limites_diarios"].get("paginas") == hoje_str:
                botao_concluido("[✓] 10 Páginas (Concluído)")
            else:
                if st.button("Ler 10 Pág. (+10$/+15XP)", type="primary", use_container_width=True):
                    dados["limites_diarios"]["paginas"] = hoje_str
                    core.alterar_valor(dados, "Paginas", 10, 15, "soma")

        with col_destaque2:
            count_agua = dados["limites_diarios"].get("agua_count", 0)
            if count_agua >= 3:
                botao_concluido("[✓] Garrafa Cheia (3/3)")
            else:
                if st.button(f"Encher Garrafa (+2$/+2XP) [{count_agua}/3]", type="primary", use_container_width=True):
                    dados["limites_diarios"]["agua_count"] += 1
                    core.alterar_valor(dados, "Garrafa_Agua", 2, 2, "soma")

    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>📋 Rotina Diária</h3>", unsafe_allow_html=True)
        col_rotina1, col_rotina2 = st.columns(2)
        
        with col_rotina1:
            if dados["limites_diarios"].get("agenda") == hoje_str:
                botao_concluido("[✓] Agenda Atualizada")
            else:
                if st.button("Atualizar Agenda (+1$/+2XP)", use_container_width=True):
                    dados["limites_diarios"]["agenda"] = hoje_str
                    core.alterar_valor(dados, "Atualizar_Agenda", 1, 2, "soma")
                    
        with col_rotina2:
            if dados["limites_diarios"].get("noticias") == hoje_str:
                botao_concluido("[✓] Notícias (Lido)")
            else:
                if st.button("Ler Notícias (+5$/+15XP)", use_container_width=True):
                    dados["limites_diarios"]["noticias"] = hoje_str
                    core.alterar_valor(dados, "Noticias", 5, 15, "soma")

    with st.container(border=True):
        with st.expander("Tarefas Gerais e Operacionais", expanded=False):
            config_ganhos = {
                "Banho / Higiene Pessoal": ("Higiene_Pessoal", 5, 5),
                "Tirar o Lixo": ("Lixo", 5, 20),
                "Lavar Roupas": ("Lavar_Roupas", 10, 10),
                "Limpar a Casa": ("Limpar_Casa", 100, 100),
                "Fazer Comida": ("Fazer_Comida", 5, 5)
            }
            
            for display_name, (nome_chave, s, x) in config_ganhos.items():
                s_final, x_final = s, x
                if sorte_ativa == "Limpinho" and nome_chave in ["Lixo", "Lavar_Roupas", "Limpar_Casa"]: 
                    s_final *= 2

                c_btn, c_rev, c_cap = st.columns([0.6, 0.1, 0.3])
                
                if c_btn.button(f"{display_name} (+{s_final}$ / +{x_final}XP)", use_container_width=True):
                    core.alterar_valor(dados, nome_chave, s_final, x_final, "soma")
                    
                if c_rev.button("-", key=f"rev_{nome_chave}", use_container_width=True):
                    core.alterar_valor(dados, nome_chave, s_final, x_final, "subtracao")
                    
                c_cap.caption(f"Registros: {dados['contadores'].get(nome_chave, 0)}")

    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>⏱️ Timer Progressivo</h3>", unsafe_allow_html=True)
        semana_passada_str = str(agora_br.date() - timedelta(days=7))
        p_hoje = dados["historico_diario"].get(hoje_str, {}).get("pomodoros", 0.0)
        p_passado = dados["historico_diario"].get(semana_passada_str, {}).get("pomodoros", 0.0)
        meta_ghost = min(p_passado + 1.0, 8.0)
        horas_hoje_dec = (p_hoje * 42) / 60
        
        col_info, col_timer = st.columns([1, 1])
        
        with col_info:
            st.markdown(f"""
<table width="100%" border="3" cellpadding="5" cellspacing="0" bordercolor="#000000" style="text-align: center; font-size: 18px; font-family: 'VT323', monospace;">
<tr bgcolor="#E8D5EB" style="font-weight: bold;">
<td>Sessões Hoje</td>
<td>Horas Hoje</td>
<td>Horas Mês</td>
</tr>
<tr>
<td>{p_hoje:.1f}</td>
<td>{formatar_horas(horas_hoje_dec)}</td>
<td>{formatar_horas(horas_mes_dec)}</td>
</tr>
<tr bgcolor="#E8D5EB" style="font-weight: bold;">
<td>Sessões Ghost</td>
<td colspan="2">Meta Ghost</td>
</tr>
<tr>
<td>{p_passado:.1f}</td>
<td colspan="2">{meta_ghost:.1f}</td>
</tr>
</table>
            """, unsafe_allow_html=True)
            
        with col_timer:
            if st.session_state.inicio_cronometro is None:
                st.markdown("""<div style="color:#6e0b8a; font-size: 80px; text-align: center; font-family: 'VT323', monospace; font-weight: bold; margin-bottom: 10px;">00:00</div>""", unsafe_allow_html=True)
                if st.button("Iniciar Estudo", use_container_width=True):
                    st.session_state.inicio_cronometro = time.time()
                    st.rerun()
            else:
                decorrido_inicial = max(0, int(time.time() - st.session_state.inicio_cronometro))
                components.html(f"""
                <div id="clock" style="color:#6e0b8a; font-size: 80px; text-align: center; font-family: 'VT323', monospace; font-weight: bold;">00:00</div>
                <script>
                    var diff = {decorrido_inicial};
                    function atualizarRelogio() {{
                        var m = Math.floor(diff / 60).toString().padStart(2, '0');
                        var s = (diff % 60).toString().padStart(2, '0');
                        document.getElementById('clock').innerHTML = m + ":" + s;
                        diff++;
                    }}
                    atualizarRelogio(); 
                    setInterval(atualizarRelogio, 1000);
                </script>
                """, height=100)
                
                col_stop, col_cancel = st.columns(2)
                with col_stop:
                    if st.button("Concluir e Salvar", use_container_width=True):
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
                    if st.button("Cancelar", use_container_width=True):
                        st.session_state.inicio_cronometro = None
                        st.rerun()
            
            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
            
            s_base_sessao = 15
            if sorte_ativa == "Dia de Sorte":
                s_base_sessao += 5
            if st.button(f"Concluir 1 Sessão (Manual) (+{s_base_sessao}$ / +10XP)", use_container_width=True):
                core.alterar_valor(dados, "Pomodoro", s_base_sessao, 10, "soma", qtd_sessoes=1.0)
                
            x_base_topico = 15
            if sorte_ativa == "Foco Total":
                x_base_topico *= 2
            if st.button(f"Concluir 1 Tópico (+10$ / +{x_base_topico}XP)", use_container_width=True):
                core.alterar_valor(dados, "Topico", 10, x_base_topico, "soma")

    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>📝 Lista de Tarefas</h3>", unsafe_allow_html=True)

        with st.expander("Adicionar Nova Tarefa", expanded=True):
            col_nome, col_data = st.columns([0.7, 0.3])
            with col_nome:
                nova_tarefa = st.text_input("Nome:")
            with col_data:
                nova_data = st.date_input("Data:")
                
            col_pri, col_btn = st.columns([0.5, 0.5])
            with col_pri:
                nova_prioridade = st.selectbox("Prioridade (0 é urgente):", [0, 1, 2])
            with col_btn:
                st.write("") 
                if st.button("Adicionar Tarefa", use_container_width=True):
                    if nova_tarefa.strip():
                        st.session_state.tarefas.append({
                            "id": str(uuid.uuid4()),
                            "nome": nova_tarefa.strip(),
                            "data": str(nova_data),
                            "prioridade": nova_prioridade,
                            "cor": "#6e0b8a" 
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
            pri = tarefa.get("prioridade", 2)
            data_t = tarefa.get("data", "")
            
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.markdown(f"""
<div style="border: 2px solid #000000; border-left: 8px solid #6e0b8a; padding: 5px 10px; margin-bottom: 2px; background-color: #FFFFFF;">
<strong style="font-size: 18px;">{nome}</strong><br>
<span style="font-size: 16px; color: #666;">Pri: {pri} | {datetime.strptime(data_t, '%Y-%m-%d').strftime('%d/%m/%Y')}</span>
</div>
                """, unsafe_allow_html=True)
                concluida = st.checkbox("Concluir", key=f"chk_{t_id}")
            with col2:
                st.write("")
                remover = st.button("X", key=f"del_{t_id}", help="Remover tarefa")
            
            if concluida or remover:
                tarefas_restantes = [t for t in tarefas_restantes if t["id"] != t_id]
                houve_alteracao = True
                
                if concluida:
                    hoje_hist = dados.setdefault("historico_diario", {}).setdefault(hoje_str, {})
                    hoje_hist["tarefas_concluidas"] = hoje_hist.get("tarefas_concluidas", 0) + 1
                    core.salvar_dados(dados)

        if houve_alteracao:
            st.session_state.tarefas = tarefas_restantes
            salvar_tarefas(st.session_state.tarefas)
            st.rerun()
