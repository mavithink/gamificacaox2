import streamlit as st
import core

def renderizar(dados):
    st.title("🎭 Cultura Mensal")
    st.markdown("Registre os filmes e livros consumidos neste mês. Os bônus são creditados automaticamente no primeiro dia do mês seguinte.")
    
    qtd_filmes = len(dados['cultura']['filmes'])
    qtd_livros = len(dados['cultura']['livros'])

    if qtd_filmes == 0:
        st.warning("Aviso: Se nenhum filme for registrado até o final do mês, haverá uma penalidade de -200$.")
    if qtd_livros == 0:
        st.warning("Aviso: Se nenhum livro for registrado até o final do mês, haverá uma penalidade de -200$.")

    col_filmes, col_livros = st.columns(2)
    
    with col_filmes:
        st.subheader(f"🎬 Filmes Assistidos ({qtd_filmes})")
        with st.form("form_filme", clear_on_submit=True):
            nome_f = st.text_input("Nome do Filme")
            nota_f = st.slider("Nota", 1, 5, 3, key="nota_f")
            sub_f = st.form_submit_button("Adicionar Filme")
            if sub_f and nome_f.strip():
                dados["cultura"]["filmes"].append({"nome": nome_f.strip(), "nota": nota_f})
                core.salvar_dados(dados)
                st.rerun()
                
        for f in dados["cultura"]["filmes"]:
            st.markdown(f"- **{f['nome']}** {'⭐' * f['nota']}")

    with col_livros:
        st.subheader(f"📚 Livros Lidos ({qtd_livros})")
        with st.form("form_livro", clear_on_submit=True):
            nome_l = st.text_input("Nome do Livro")
            nota_l = st.slider("Nota", 1, 5, 3, key="nota_l")
            sub_l = st.form_submit_button("Adicionar Livro")
            if sub_l and nome_l.strip():
                dados["cultura"]["livros"].append({"nome": nome_l.strip(), "nota": nota_l})
                core.salvar_dados(dados)
                st.rerun()
                
        for l in dados["cultura"]["livros"]:
            st.markdown(f"- **{l['nome']}** {'⭐' * l['nota']}")
            
    st.divider()
    prev_s = (qtd_filmes * 20) + (qtd_livros * 50)
    prev_x = (qtd_filmes * 20) + (qtd_livros * 50)
    penalidade_prevista = 0
    if qtd_filmes == 0: penalidade_prevista += 200
    if qtd_livros == 0: penalidade_prevista += 200

    if penalidade_prevista > 0:
        st.info(f"**Bônus Acumulado:** +{prev_s}$ e +{prev_x}XP | **Penalidades Previstas:** -{penalidade_prevista}$")
    else:
        st.info(f"**Bônus Acumulado para o fim do mês:** +{prev_s}$ e +{prev_x}XP")
