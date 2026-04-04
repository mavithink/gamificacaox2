import streamlit as st
import core
from datetime import datetime, timedelta

def renderizar(dados):
    st.title("Extras e Conquistas")
    agora_dt_br = datetime.utcnow() - timedelta(hours=3)
    hoje_dt = agora_dt_br.date()
    agora_time = agora_dt_br.time()
    limite = datetime.strptime("06:15", "%H:%M").time()

    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0; text-align: center;'>✨ Recompensa Especial</h3>", unsafe_allow_html=True)
        c_ac_1, c_ac_2, c_ac_3 = st.columns([1, 2, 1])
        with c_ac_2:
            if dados.get("ultimo_acordar_cedo") == str(hoje_dt):
                st.button("Acordar Cedo (Resgatado)", disabled=True, use_container_width=True)
            else:
                if st.button("Acordar Cedo (+25$/ +25XP)", type="primary", use_container_width=True):
                    if agora_time <= limite:
                        dados["ultimo_acordar_cedo"] = str(hoje_dt)
                        dados["conquistas"]["madrugador"]["ultima_data"] = str(hoje_dt)
                        dados["conquistas"]["madrugador"]["atual"] += 1
                        if dados["conquistas"]["madrugador"]["atual"] >= 10:
                            dados["saldo"] += 150
                            dados["conquistas"]["madrugador"]["completadas"] += 1
                            dados["conquistas"]["madrugador"]["data_conclusao"] = str(hoje_dt)
                            dados["conquistas"]["madrugador"]["atual"] = 0
                        core.alterar_valor(dados, "Acordar Cedo", 25, 25, "soma")
                    else: 
                        st.error(f"Passou do horário! O sistema registrou: {agora_time.strftime('%H:%M')}")
    
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>🎯 Missões Diárias</h3>", unsafe_allow_html=True)
        col_m1, col_m2, col_m3 = st.columns(3)
        colunas_missoes = [col_m1, col_m2, col_m3]

        for i, missao in enumerate(dados["missoes_diarias"]["missoes"]):
            with colunas_missoes[i]:
                st.markdown(f"""
                    <div style='background-color: #FFFFFF; border: 1px solid #000000; padding: 10px; margin-bottom: 5px;'>
                        <strong style='font-size: 18px; color: #000000;'>{missao['desc']}</strong><br>
                        <span style='font-size: 14px; color: #666666;'>Recompensa: +{missao['s']}$ | +{missao['x']}XP</span>
                    </div>
                """, unsafe_allow_html=True)
                if missao["concluida"]:
                    st.button("Concluída", disabled=True, key=f"btn_done_{i}", use_container_width=True)
                else:
                    if st.button("Concluir", key=f"btn_missao_{i}", use_container_width=True):
                        missao["concluida"] = True
                        core.alterar_valor(dados, "Missao Diaria", missao['s'], missao['x'], "soma")

    col_sorte, col_conquistas = st.columns(2)
    
    with col_sorte:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>🎲 Sua Sorte Diária</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style="text-align: center; padding: 15px; background-color: #E8D5EB; border: 1px solid #6e0b8a;">
                    <h4 style="margin: 0; color: #000000; font-size: 18px; border-bottom: none;">Previsão para {dados['sorte_dia']['data']}:</h4>
                    <p style="font-size: 22px; color: #6e0b8a; font-weight: bold; margin-top: 10px;">{dados['sorte_dia']['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

    with col_conquistas:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>🏆 Conquistas Únicas</h3>", unsafe_allow_html=True)
            
            mad_hoje = dados["conquistas"]["madrugador"]["data_conclusao"] == str(hoje_dt)
            mad_atual = 10 if mad_hoje else dados["conquistas"]["madrugador"]["atual"]
            st.markdown(f"<p style='font-weight: bold; margin-bottom: 0;'>Madrugador (10 dias antes das 06:15)</p>", unsafe_allow_html=True)
            st.progress(mad_atual / 10.0)
            st.caption(f"Progresso: {mad_atual} / 10 | Completadas: {dados['conquistas']['madrugador']['completadas']}")
            
            inc_hoje = dados["conquistas"]["incorruptivel"]["data_conclusao"] == str(hoje_dt)
            inc_atual = 3 if inc_hoje else dados["conquistas"]["incorruptivel"]["atual"]
            st.markdown(f"<p style='font-weight: bold; margin-bottom: 0; margin-top: 15px;'>Incorruptível (3 dias sem punição)</p>", unsafe_allow_html=True)
            st.progress(inc_atual / 3.0)
            st.caption(f"Progresso: {inc_atual} / 3 | Completadas: {dados['conquistas']['incorruptivel']['completadas']}")
