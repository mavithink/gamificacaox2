import streamlit as st
import core
from datetime import datetime

def renderizar(dados):
    st.title("Loja e Gastos")
    
    if type(dados.get("sorte_dia")) is not dict:
        dados["sorte_dia"] = {"data": "", "efeito": None}
    if type(dados.get("contadores")) is not dict:
        dados["contadores"] = {}
        
    sorte_ativa = dados["sorte_dia"].get("efeito")
    qtd_cupons = dados.get('cupons', 0)
    
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>🎫 Cupons de Desconto</h3>", unsafe_allow_html=True)
        aplicar_desconto = False
        if qtd_cupons > 0:
            aplicar_desconto = st.checkbox(f"Ativar Cupom (20% OFF) - Possui: {qtd_cupons}")
        else:
            st.write("Você não possui cupons no momento.")

    col_loja, col_punicao = st.columns(2)

    with col_loja:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>🛍️ Itens Disponíveis</h3>", unsafe_allow_html=True)
            
            # Dicionário atualizado com os novos itens solicitados
            itens_loja = {
                "60m de Jogo": 30, 
                "Delivery": 250, 
                "Cosmético": 1200, 
                "Ver filme": 50,
                "1 Episódio Série": 10,
                "1 Capítulo Novel": 4,
                "10 Capítulos Novel": 36
            }
            
            for item, preco_base in itens_loja.items():
                preco_final = preco_base
                
                # Regras de modificadores de preço
                if sorte_ativa == "Inflação": 
                    preco_final = int(preco_final * 1.2)
                if item == "Ver filme" and sorte_ativa == "Dia de Cinema": 
                    preco_final = 30
                if aplicar_desconto: 
                    preco_final = int(preco_final * 0.8)

                if st.button(f"{item} (-{preco_final}$)", use_container_width=True):
                    if dados.get('saldo', 0) >= preco_final:
                        dados['saldo'] -= preco_final
                        if aplicar_desconto: 
                            dados['cupons'] -= 1
                        
                        chave_contador = f"Gasto_{item.replace(' ', '_')}"
                        dados["contadores"][chave_contador] = dados["contadores"].get(chave_contador, 0) + 1
                        core.salvar_dados(dados)
                        st.rerun()
                    else: 
                        st.error("Saldo insuficiente!")
                
                chave_exibicao = f"Gasto_{item.replace(' ', '_')}"
                st.caption(f"Comprados: {dados['contadores'].get(chave_exibicao, 0)}")

    with col_punicao:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>⚠️ Punições</h3>", unsafe_allow_html=True)
            punicoes = {"Rede Social": 25, "Gasto Inútil": 100}
            for p, v in punicoes.items():
                v_final = v * 3 if sorte_ativa == "Não faça isso" else v
                if st.button(f"{p} (-{v_final}$)", use_container_width=True):
                    dados['saldo'] = dados.get('saldo', 0) - v_final
                    chave_p = f"P_{p.replace(' ', '_')}"
                    dados["contadores"][chave_p] = dados["contadores"].get(chave_p, 0) + 1
                    dados["ultima_punicao_data"] = str(datetime.utcnow().date())
                    
                    if "conquistas" not in dados:
                        dados["conquistas"] = {}
                    if "incorruptivel" not in dados["conquistas"]:
                        dados["conquistas"]["incorruptivel"] = {"atual": 0}
                        
                    dados["conquistas"]["incorruptivel"]["atual"] = 0
                    core.salvar_dados(dados)
                    st.rerun()
                st.caption(f"Ocorrências: {dados['contadores'].get(f'P_{p.replace(' ', '_')}', 0)}")
