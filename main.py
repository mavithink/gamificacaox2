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

# Cartão da barra lateral mais robusto
st.sidebar.markdown(f"""
    <div style="background-color: #FFFFFF; padding: 15px; border: 4px solid #6e0b8a; text-align: center; margin-top: 20px; box-shadow: 4px 4px 0px #808080;">
        <p style="color: #000000; margin: 0 0 10px 0; font-size: 16px; font-weight: bold;">[ {data_formatada} ]</p>
        <h2 style="color: #6e0b8a; margin: 0; font-size: 28px; border-bottom: none;">Saldo: {dados['saldo']} $</h2>
        <hr style="border-top: 3px solid #6e0b8a; margin: 10px 0;">
        <p style="color: #000000; margin: 0; font-weight: bold; font-size: 18px;">⏱️ {horas_hoje:.1f}h estudadas</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.divider()
with st.sidebar.expander("Configurações e Reset"):
    st.warning("O botão abaixo apagará todos os dados.")
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
        st.error("AVISO: Você ainda não registrou nenhum tempo de estudo hoje! Penalidade de -50$ pendente.")

    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>Dados do Jogador</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <table width="100%" border="3" cellpadding="5" cellspacing="0" bordercolor="#6e0b8a" style="margin-bottom: 15px; text-align: center; background-color: #FFFFFF; font-family: 'VT323', monospace;">
                <tr bgcolor="#E8D5EB" style="color: #000000; font-weight: bold; font-size: 18px;">
                    <td>Saldo</td>
                    <td>XP</td>
                    <td>Nível</td>
                    <td>Cupons</td>
                    <td>Streak</td>
                </tr>
                <tr style="font-size: 22px; font-weight: bold; color: #6e0b8a;">
                    <td>{dados['saldo']} $</td>
                    <td>{dados['xp']} / {core.XP_POR_NIVEL}</td>
                    <td>{dados['nivel']}</td>
                    <td>{dados['cupons']}</td>
                    <td>{dados['streak']}</td>
                </tr>
            </table>
        """, unsafe_allow_html=True)
        st.markdown("<div style='font-size: 16px; margin-bottom: 5px; font-weight: bold;'>Progresso para o Próximo Nível:</div>", unsafe_allow_html=True)
        st.progress(min(dados['xp'] / core.XP_POR_NIVEL, 1.0))

    col_presenca, col_horario = st.columns([1, 2.5])
    
    with col_presenca:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>Presença nas Aulas</h3>", unsafe_allow_html=True)
            dia_semana = agora_br.weekday()
            
            if dia_semana >= 5:
                st.markdown('<div style="border: 3px solid #000000; background-color: #E9EAED; padding: 10px; font-family: \'VT323\', monospace;">Não há aula hoje.</div>', unsafe_allow_html=True)
            else:
                hoje_historico = dados.setdefault("historico_diario", {}).setdefault(hoje_str, {})
                foi_aula = hoje_historico.get("aula_confirmada", False)
                
                if foi_aula:
                    st.markdown('<div style="border: 3px solid #6e0b8a; background-color: #E8D5EB; color: #6e0b8a; padding: 10px; margin-bottom: 10px; font-family: \'VT323\', monospace; font-weight: bold;">[+] Presença confirmada! (+20$, +10XP)</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="border: 3px solid #000000; background-color: #DFDFDF; color: #000000; padding: 10px; margin-bottom: 10px; font-family: \'VT323\', monospace;">[!] Confirme presença ou perderá 60$.</div>', unsafe_allow_html=True)
                    if st.button("Confirmar Presença (+20$ / +10XP)", use_container_width=True):
                        hoje_historico["aula_confirmada"] = True
                        core.alterar_valor(dados, "Presenca_Aula", 20, 10, "soma")

    with col_horario:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>Horário da Semana</h3>", unsafe_allow_html=True)
            c_seg, c_ter, c_qua, c_qui, c_sex = st.columns(5)
            
            def card_aula(horario, materia, local):
                return f"""
                <div style="background-color: #FFFFFF; border: 3px solid #6e0b8a; padding: 4px; margin-bottom: 5px; text-align: center; font-family: 'VT323', monospace;">
                    <div style="font-weight: bold; color: #6e0b8a; border-bottom: 2px dotted #000000; margin-bottom: 3px; font-size: 16px;">{horario}</div>
                    <div style="color: #000000; font-size: 16px; font-weight: bold;">{materia}</div>
                    <div style="color: #666666; font-size: 14px;">[{local}]</div>
                </div>
                """

            with c_seg:
                st.markdown("<div style='text-align: center; font-weight: bold; background-color: #E8D5EB; border: 3px solid #6e0b8a; padding: 2px; margin-bottom: 8px; font-size: 18px;'>Seg</div>", unsafe_allow_html=True)
                st.markdown(card_aula("08:00-10:00", "Sist. Operacionais", "Auditório DC"), unsafe_allow_html=True)
                st.markdown(card_aula("16:00-18:00", "Algoritmos 2", "AT4-68"), unsafe_allow_html=True)

            with c_ter:
                st.markdown("<div style='text-align: center; font-weight: bold; background-color: #E8D5EB; border: 3px solid #6e0b8a; padding: 2px; margin-bottom: 8px; font-size: 18px;'>Ter</div>", unsafe_allow_html=True)
                st.markdown(card_aula("10:00-12:00", "Álgebra Linear 1", "AT9-218"), unsafe_allow_html=True)
                st.markdown(card_aula("16:00-18:00", "Mat. Discreta", "AT4-68"), unsafe_allow_html=True)

            with c_qua:
                st.markdown("<div style='text-align: center; font-weight: bold; background-color: #E8D5EB; border: 3px solid #6e0b8a; padding: 2px; margin-bottom: 8px; font-size: 18px;'>Qua</div>", unsafe_allow_html=True)
                st.markdown(card_aula("10:00-12:00", "Sist. Operacionais", "Auditório DC"), unsafe_allow_html=True)

            with c_qui:
                st.markdown("<div style='text-align: center; font-weight: bold; background-color: #E8D5EB; border: 3px solid #6e0b8a; padding: 2px; margin-bottom: 8px; font-size: 18px;'>Qui</div>", unsafe_allow_html=True)
                st.markdown(card_aula("08:00-10:00", "Álgebra Linear 1", "AT7-164"), unsafe_allow_html=True)
                st.markdown(card_aula("14:00-16:00", "Mat. Discreta", "AT4-68"), unsafe_allow_html=True)
                st.markdown(card_aula("16:00-18:00", "Algoritmos 2", "AT4-73"), unsafe_allow_html=True)

            with c_sex:
                st.markdown("<div style='text-align: center; font-weight: bold; background-color: #E8D5EB; border: 3px solid #6e0b8a; padding: 2px; margin-bottom: 8px; font-size: 18px;'>Sex</div>", unsafe_allow_html=True)
                st.markdown(card_aula("10:00-12:00", "Sist. Operacionais", "DC-LE-3"), unsafe_allow_html=True)
                st.markdown(card_aula("14:00-18:00", "Empreendedores", "AT9-212"), unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>Estatísticas e Resumos</h3>", unsafe_allow_html=True)
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
                "Sessões": historico["pomodoros"],
                "Moedas": historico["moedas_ganhas"]
            })

        df_grafico = pd.DataFrame(dados_grafico).set_index("Dia")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("<p style='text-align: center; color: #000000; font-weight: bold;'>Foco (Sessões - Últimos 7 dias)</p>", unsafe_allow_html=True)
            st.bar_chart(df_grafico["Sessões"], color="#6e0b8a")
        with col_g2:
            st.markdown("<p style='text-align: center; color: #000000; font-weight: bold;'>Rendimento (Moedas - Últimos 7 dias)</p>", unsafe_allow_html=True)
            st.line_chart(df_grafico["Moedas"], color="#6e0b8a")
            
        st.markdown("<p style='text-align: center; color: #000000; font-weight: bold; margin-top: 15px;'>Distribuição de Tarefas Concluídas</p>", unsafe_allow_html=True)
        contadores = dados.get("contadores", {})
        df_contadores = pd.DataFrame(list(contadores.items()), columns=['Tarefa', 'Quantidade']).set_index('Tarefa')
        df_contadores = df_contadores[~df_contadores.index.str.startswith('Gasto_') & ~df_contadores.index.str.startswith('P_')]
        if not df_contadores.empty:
            st.bar_chart(df_contadores, color="#6e0b8a")

elif pagina == "Mente e Rotina":
    mente_rotina.renderizar(dados)
elif pagina == "Gastos":
    loja.renderizar(dados)
elif pagina == "Cultura":
    cultura.renderizar(dados)
elif pagina == "Extras":
    extras.renderizar(dados)
