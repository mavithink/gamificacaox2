import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import core
import mente_rotina
import loja
import extras
import cultura

st.set_page_config(page_title="Gamificação", page_icon="🤖", layout="wide")

if 'dados' not in st.session_state:
    st.session_state.dados = core.carregar_dados()

if "inicio_cronometro" not in st.session_state:
    st.session_state.inicio_cronometro = None

dados = st.session_state.dados

core.verificar_estagnacao(dados, st.session_state)

for aviso in core.verificar_penalidade_estudo(dados):
    st.error(aviso)

for aviso in core.verificar_penalidade_aula(dados):
    st.error(aviso)

for aviso in core.verificar_ghost(dados):
    st.success(aviso)

core.atualizar_incorruptivel(dados)
core.verificar_reset_madrugador(dados)
core.verificar_mes_cultura(dados, st.session_state)
core.aplicar_sorte_diaria(dados)
core.gerar_missoes_diarias(dados)

if "msg_cultura" in st.session_state:
    st.warning(st.session_state["msg_cultura"])
    del st.session_state["msg_cultura"]

if dados['xp'] >= core.XP_POR_NIVEL:
    dados['xp'] -= core.XP_POR_NIVEL
    dados['nivel'] += 1
    dados['cupons'] += 1
    core.salvar_dados(dados)
    st.rerun()

st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Ir para:", ["Painel Principal", "Mente e Rotina", "Gastos", "Cultura", "Extras"])

agora_br = datetime.utcnow() - timedelta(hours=3)
hoje_str = str(agora_br.date())
p_hoje = dados.get("historico_diario", {}).get(hoje_str, {}).get("pomodoros", 0.0)
horas_hoje = (p_hoje * 42) / 60
data_formatada = agora_br.strftime("%d/%m/%Y")

st.sidebar.markdown(f"""
    <div style="background-color: #1a1a2e; padding: 20px; border-radius: 12px; border: 2px solid #464b5d; text-align: center; margin-top: 40px; box-shadow: 0 8px 16px rgba(0,0,0,0.5);">
        <p style="color: #8a8a9d; margin: 0 0 10px 0; font-size: 14px; font-weight: bold; letter-spacing: 2px;">{data_formatada}</p>
        <h2 style="color: #FFD700; margin: 0; font-size: 36px; text-shadow: 0 0 15px rgba(255, 215, 0, 0.4);">💰 {dados['saldo']} $</h2>
        <hr style="border-color: #2e2e48; margin: 15px 0;">
        <h4 style="color: #00E5FF; margin: 0; text-shadow: 0 0 10px rgba(0, 229, 255, 0.4);">⏱️ {horas_hoje:.1f}h estudadas</h4>
    </div>
""", unsafe_allow_html=True)

st.sidebar.divider()
if st.sidebar.button("Resetar Tudo"):
    agora_reset = datetime.utcnow() - timedelta(hours=3)
    st.session_state.dados = {
        "saldo": 0, "xp": 0, "nivel": 1, "cupons": 0, "contadores": {}, "streak": 0,
        "ultima_atividade": str(agora_reset.date() - timedelta(days=1)),
        "ultimo_registro_full": str(agora_reset),
        "ultimo_acordar_cedo": str(agora_reset.date() - timedelta(days=1)),
        "ultimo_ghost_check": str(agora_reset.date() - timedelta(days=1)),
        "ultima_verificacao_estudo": str(agora_reset.date()),
        "ultima_verificacao_aula": str(agora_reset.date()),
        "sorte_dia": {"data": "", "efeito": None},
        "ultima_punicao_data": "",
        "historico_diario": {},
        "missoes_diarias": {"data": "", "missoes": []},
        "limites_diarios": {"noticias": "", "paginas": ""},
        "cultura": {"mes_referencia": agora_reset.strftime("%Y-%m"), "filmes": [], "livros": []},
        "conquistas": {
            "madrugador": {"atual": 0, "total": 10, "completadas": 0, "ultima_data": str(agora_reset.date() - timedelta(days=1)), "data_conclusao": ""},
            "incorruptivel": {"atual": 0, "total": 3, "completadas": 0, "ultima_verificacao": str(agora_reset.date()), "data_conclusao": ""}
        }
    }
    core.salvar_dados(st.session_state.dados)
    st.rerun()

if pagina == "Painel Principal":
    st.title("📊 Painel Principal")
    
    if p_hoje <= 0.0:
        st.error("🚨 **AVISO URGENTE:** Você ainda não registrou nenhum tempo de estudo hoje! Se o dia virar sem estudos, uma penalidade de -50$ será aplicada.")

    st.markdown(f"""
    <style>
    .metric-container {{ display: flex; justify-content: space-between; gap: 15px; margin-bottom: 20px; }}
    .metric-card {{ flex: 1; background-color: #1a1a2e; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #2e2e48; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
    .metric-card h4 {{ margin: 0; color: #8a8a9d; font-size: 14px; text-transform: uppercase; letter-spacing: 1.5px; }}
    .metric-card h2 {{ margin: 10px 0 0 0; font-size: 32px; font-weight: 800; }}
    .card-saldo h2 {{ color: #FFD700; }}
    .card-xp h2 {{ color: #00E5FF; }}
    .card-nivel h2 {{ color: #B388FF; }}
    .card-cupons h2 {{ color: #00E676; }}
    .card-streak h2 {{ color: #ff4b4b; }}
    </style>
    <div class="metric-container">
        <div class="metric-card card-saldo"><h4>Saldo 💰</h4><h2>{dados['saldo']} $</h2></div>
        <div class="metric-card card-xp"><h4>XP ⚡</h4><h2>{dados['xp']} / {core.XP_POR_NIVEL}</h2></div>
        <div class="metric-card card-nivel"><h4>Nível 🌟</h4><h2>{dados['nivel']}</h2></div>
        <div class="metric-card card-cupons"><h4>Cupons 🎫</h4><h2>{dados['cupons']}</h2></div>
        <div class="metric-card card-streak"><h4>Streak 🔥</h4><h2>{dados['streak']}</h2></div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(min(dados['xp'] / core.XP_POR_NIVEL, 1.0))
    st.divider()

    st.subheader("🎓 Presença nas Aulas")
    dia_semana = agora_br.weekday()
    
    if dia_semana >= 5:
        st.info("Não há aula hoje.")
    else:
        hoje_historico = dados.setdefault("historico_diario", {}).setdefault(hoje_str, {})
        foi_aula = hoje_historico.get("aula_confirmada", False)
        
        if foi_aula:
            st.success("✅ Presença confirmada hoje! (+20$, +10XP)")
        else:
            st.warning("⚠️ Você ainda não confirmou presença nas aulas de hoje. Se o dia virar, perderá 60$.")
            if st.button("Confirmar Presença na Aula (+20$ / +10XP)", use_container_width=True):
                hoje_historico["aula_confirmada"] = True
                core.alterar_valor(dados, "Presenca_Aula", 20, 10, "soma")

    # ==========================================
    # NOVO QUADRO DE HORÁRIOS (MINIMALISTA)
    # ==========================================
    st.markdown("<h3 style='text-align: center; margin-top: 30px; margin-bottom: 20px;'>📅 Horário de Aulas da Semana</h3>", unsafe_allow_html=True)
    
    col_seg, col_ter, col_qua, col_qui, col_sex = st.columns(5)
    
    def card_aula(horario, materia, local, cor_borda):
        return f"""
        <div style="background-color: #1a1a2e; padding: 12px 8px; border-radius: 8px; border-top: 4px solid {cor_borda}; margin-bottom: 12px; font-size: 13px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
            <div style="color: #FFD700; font-weight: bold; margin-bottom: 6px;">{horario}</div>
            <div style="color: white; font-weight: 600; line-height: 1.3; margin-bottom: 6px;">{materia}</div>
            <div style="color: #8a8a9d; font-size: 11px;">📍 {local}</div>
        </div>
        """

    with col_seg:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #2e2e48; padding: 8px; border-radius: 5px; margin-bottom: 15px;'>Segunda</div>", unsafe_allow_html=True)
        st.markdown(card_aula("08:00 - 10:00", "Sistemas Operacionais", "Auditório DC", "#ff4b4b"), unsafe_allow_html=True)
        st.markdown(card_aula("16:00 - 18:00", "Algoritmos e Est. Dados 2", "AT4-68", "#00E5FF"), unsafe_allow_html=True)

    with col_ter:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #2e2e48; padding: 8px; border-radius: 5px; margin-bottom: 15px;'>Terça</div>", unsafe_allow_html=True)
        st.markdown(card_aula("10:00 - 12:00", "Álgebra Linear 1", "AT9-218", "#B388FF"), unsafe_allow_html=True)
        st.markdown(card_aula("16:00 - 18:00", "Matemática Discreta", "AT4-68", "#00E676"), unsafe_allow_html=True)

    with col_qua:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #2e2e48; padding: 8px; border-radius: 5px; margin-bottom: 15px;'>Quarta</div>", unsafe_allow_html=True)
        st.markdown(card_aula("10:00 - 12:00", "Sistemas Operacionais", "Auditório DC", "#ff4b4b"), unsafe_allow_html=True)

    with col_qui:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #2e2e48; padding: 8px; border-radius: 5px; margin-bottom: 15px;'>Quinta</div>", unsafe_allow_html=True)
        st.markdown(card_aula("08:00 - 10:00", "Álgebra Linear 1", "AT7-164", "#B388FF"), unsafe_allow_html=True)
        st.markdown(card_aula("14:00 - 16:00", "Matemática Discreta", "AT4-68", "#00E676"), unsafe_allow_html=True)
        st.markdown(card_aula("16:00 - 18:00", "Algoritmos e Est. Dados 2", "AT4-73", "#00E5FF"), unsafe_allow_html=True)

    with col_sex:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #2e2e48; padding: 8px; border-radius: 5px; margin-bottom: 15px;'>Sexta</div>", unsafe_allow_html=True)
        st.markdown(card_aula("10:00 - 12:00", "Sistemas Operacionais", "DC-LE-3", "#ff4b4b"), unsafe_allow_html=True)
        st.markdown(card_aula("14:00 - 18:00", "Empreendedores em Inf.", "AT9-212", "#FFD700"), unsafe_allow_html=True)

    st.divider()

    st.subheader("Estatísticas e Resumos")
    inicio_semana = agora_br.date() - timedelta(days=6)
    
    dias_pt = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    dados_grafico = []
    for i in range(7):
        dia_atual = inicio_semana + timedelta(days=i)
        dia_str = str(dia_atual)
        nome_dia = dias_pt[dia_atual.weekday()]
        historico = dados.get("historico_diario", {}).get(dia_str, {"pomodoros": 0.0, "moedas_ganhas": 0})
        dados_grafico.append({
            "Dia": f"{dia_atual.strftime('%d/%m')} - {nome_dia}",
            "Sessões Equivalentes": historico["pomodoros"],
            "Moedas Geradas": historico["moedas_ganhas"]
        })

    df_grafico = pd.DataFrame(dados_grafico).set_index("Dia")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("<p style='text-align: center; color: #ff4b4b; font-weight: bold;'>🍅 Foco (Últimos 7 dias)</p>", unsafe_allow_html=True)
        st.bar_chart(df_grafico["Sessões Equivalentes"], color="#ff4b4b")
    with col_g2:
        st.markdown("<p style='text-align: center; color: #FFD700; font-weight: bold;'>💰 Rendimento (Últimos 7 dias)</p>", unsafe_allow_html=True)
        st.line_chart(df_grafico["Moedas Geradas"], color="#FFD700")
        
    st.divider()
    st.markdown("<p style='text-align: center; color: #00E5FF; font-weight: bold;'>📈 Distribuição de Tarefas Concluídas (Geral)</p>", unsafe_allow_html=True)
    contadores = dados.get("contadores", {})
    df_contadores = pd.DataFrame(list(contadores.items()), columns=['Tarefa', 'Quantidade']).set_index('Tarefa')
    df_contadores = df_contadores[~df_contadores.index.str.startswith('Gasto_') & ~df_contadores.index.str.startswith('P_')]
    if not df_contadores.empty:
        st.bar_chart(df_contadores, color="#00E5FF")

elif pagina == "Mente e Rotina":
    mente_rotina.renderizar(dados)
elif pagina == "Gastos":
    loja.renderizar(dados)
elif pagina == "Cultura":
    cultura.renderizar(dados)
elif pagina == "Extras":
    extras.renderizar(dados)
