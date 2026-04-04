st.sidebar.divider()
with st.sidebar.expander("⚠️ Configurações e Reset"):
    st.warning("O botão abaixo apagará todos os seus dados permanentemente. Essa ação não pode ser desfeita.")
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
