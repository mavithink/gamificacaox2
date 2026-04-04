import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import core
import mente_rotina
import loja
import extras
import cultura
import theme_oldweb

st.set_page_config(page_title="Gamificação", page_icon="🤖", layout="wide")

theme_oldweb.injetar_css_oldweb()

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

# Cartão da barra lateral claro com bordas old web
st.sidebar.markdown(f"""
    <div style="background-color: #FFFFFF; padding: 15px; border: 2px solid #3B5998; text-align: center; margin-top: 20px;">
        <p style="color: #000000; margin: 0 0 10px 0; font-size: 12px; font-weight: bold;">[ {data_formatada} ]</p>
        <h2 style="color: #3B5998; margin: 0; font-size: 24px; border-bottom: none;">Saldo: {dados['saldo']} $</h2>
        <hr style="border-top: 1px solid #3B5998; margin: 10px 0;">
        <p style="color: #000000; margin: 0; font-weight: bold; font-size: 14px;">⏱️ {horas_hoje:.1f}h estudadas</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.divider()
with st.sidebar.expander("Configurações e Reset"):
    st.warning("O botão abaixo apagará todos os seus dados permanentemente.")
    if st.button("Confirmar Reset Total", type="primary", use_container_width=True):
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
    st.title("Painel Principal")
    
    if p_hoje <= 0.0:
        st.error("AVISO: Você ainda não registrou nenhum tempo de estudo hoje! Se o dia virar sem estudos, uma penalidade de -50$ será aplicada.")

    # Status e Métricas em Tabela HTML Old Web
    st.markdown(f"""
        <table width="100%" border="1" cellpadding="5" cellspacing="0" bordercolor="#3B5998" style="margin-bottom: 20px; text-align: center; background-color: #FFFFFF; font-family: Verdana, sans-serif;">
            <tr bgcolor="#D8DFEA" style="color: #000000; font-weight: bold; font-size: 14px;">
                <td>Saldo</td>
                <td>XP</td>
                <td>Nível</td>
                <td>Cupons</td>
                <td>Streak</td>
            </tr>
            <tr style="font-size: 16px; font-weight: bold; color: #3B5998;">
                <td>{dados['saldo']} $</td>
                <td>{dados['xp']} / {core.XP_POR_NIVEL}</td>
                <td>{dados['nivel']}</td>
                <td>{dados['cupons']}</td>
                <td>{dados['streak']}</td>
            </tr>
        </table>
    """, unsafe_allow_html=True)
    st.progress(min(dados['xp'] / core.XP_POR_NIVEL, 1.0))
    st.divider()

    st.subheader("Presença nas Aulas")
    dia_semana = agora_br.weekday()
    
    if dia_semana >= 5:
        st.info("Não há aula hoje.")
    else:
        hoje_historico = dados.setdefault("historico_diario", {}).setdefault(hoje_str, {})
        foi_aula = hoje_historico.get("aula_confirmada", False)
        
        if foi_aula:
            st.success("Presença confirmada hoje! (+20$, +10XP)")
        else:
            st.warning("Você ainda não confirmou presença nas aulas de hoje. Se o dia virar, perderá 60$.")
            if st.button("Confirmar Presença na Aula (+20$ / +10XP)", use_container_width=True):
                hoje_historico["aula_confirmada"] = True
                core.alterar_valor(dados, "Presenca_Aula", 20, 10, "soma")

    # Horário de Aulas formatado claro
    st.subheader("Horário de Aulas da Semana")
    
    col_seg, col_ter, col_qua, col_qui, col_sex = st.columns(5)
    
    def card_aula(horario, materia, local):
        return f"""
        <div style="background-color: #FFFFFF; border: 1px solid #3B5998; padding: 5px; margin-bottom: 5px; font-size: 11px; text-align: center;">
            <div style="font-weight: bold; color: #3B5998; border-bottom: 1px dotted #A0A0A0; margin-bottom: 3px;">{horario}</div>
            <div style="color: #000000; font-weight: bold;">{materia}</div>
            <div style="color: #666666;">[{local}]</div>
        </div>
        """

    with col_seg:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #D8DFEA; border: 1px solid #3B5998; padding: 3px; margin-bottom: 10px; font-size: 12px;'>Segunda</div>", unsafe_allow_html=True)
        st.markdown(card_aula("08:00 - 10:00", "Sistemas Operacionais", "Auditório DC"), unsafe_allow_html=True)
        st.markdown(card_aula("16:00 - 18:00", "Algoritmos e Est. Dados 2", "AT4-68"), unsafe_allow_html=True)

    with col_ter:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #D8DFEA; border: 1px solid #3B5998; padding: 3px; margin-bottom: 10px; font-size: 12px;'>Terça</div>", unsafe_allow_html=True)
        st.markdown(card_aula("10:00 - 12:00", "Álgebra Linear 1", "AT9-218"), unsafe_allow_html=True)
        st.markdown(card_aula("16:00 - 18:00", "Matemática Discreta", "AT4-68"), unsafe_allow_html=True)

    with col_qua:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #D8DFEA; border: 1px solid #3B5998; padding: 3px; margin-bottom: 10px; font-size: 12px;'>Quarta</div>", unsafe_allow_html=True)
        st.markdown(card_aula("10:00 - 12:00", "Sistemas Operacionais", "Auditório DC"), unsafe_allow_html=True)

    with col_qui:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #D8DFEA; border: 1px solid #3B5998; padding: 3px; margin-bottom: 10px; font-size: 12px;'>Quinta</div>", unsafe_allow_html=True)
        st.markdown(card_aula("08:00 - 10:00", "Álgebra Linear 1", "AT7-164"), unsafe_allow_html=True)
        st.markdown(card_aula("14:00 - 16:00", "Matemática Discreta", "AT4-68"), unsafe_allow_html=True)
        st.markdown(card_aula("16:00 - 18:00", "Algoritmos e Est. Dados 2", "AT4-73"), unsafe_allow_html=True)

    with col_sex:
        st.markdown("<div style='text-align: center; font-weight: bold; background-color: #D8DFEA; border: 1px solid #3B5998; padding: 3px; margin-bottom: 10px; font-size: 12px;'>Sexta</div>", unsafe_allow_html=True)
        st.markdown(card_aula("10:00 - 12:00", "Sistemas Operacionais", "DC-LE-3"), unsafe_allow_html=True)
        st.markdown(card_aula("14:00 - 18:00", "Empreendedores em Inf.", "AT9-212"), unsafe_allow_html=True)

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
        st.markdown("<p style='text-align: center; color: #000000; font-weight: bold;'>Foco (Últimos 7 dias)</p>", unsafe_allow_html=True)
        st.bar_chart(df_grafico["Sessões Equivalentes"], color="#3B5998")
    with col_g2:
        st.markdown("<p style='text-align: center; color: #000000; font-weight: bold;'>Rendimento (Últimos 7 dias)</p>", unsafe_allow_html=True)
        st.line_chart(df_grafico["Moedas Geradas"], color="#3B5998")
        
    st.divider()
    st.markdown("<p style='text-align: center; color: #000000; font-weight: bold;'>Distribuição de Tarefas Concluídas (Geral)</p>", unsafe_allow_html=True)
    contadores = dados.get("contadores", {})
    df_contadores = pd.DataFrame(list(contadores.items()), columns=['Tarefa', 'Quantidade']).set_index('Tarefa')
    df_contadores = df_contadores[~df_contadores.index.str.startswith('Gasto_') & ~df_contadores.index.str.startswith('P_')]
    if not df_contadores.empty:
        st.bar_chart(df_contadores, color="#3B5998")

elif pagina == "Mente e Rotina":
    mente_rotina.renderizar(dados)
elif pagina == "Gastos":
    loja.renderizar(dados)
elif pagina == "Cultura":
    cultura.renderizar(dados)
elif pagina == "Extras":
    extras.renderizar(dados)
