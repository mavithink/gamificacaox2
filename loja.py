import streamlit as st
import core
from datetime import datetime

def renderizar(dados):
    st.title("🛒 Loja e Gastos")
    
    # 1. Blindagem contra conversões acidentais do Firebase (Garante que sempre será dicionário)
    if type(dados.get("sorte_dia")) is not dict:
        dados["sorte_dia"] = {"data": "", "efeito": None}
    if type(dados.get("contadores")) is not dict:
        dados["contadores"] = {}
        
    sorte_ativa = dados["sorte_dia"].get("efeito")
    
    # 2. Substituição do st.toggle por st.checkbox (100% de compatibilidade)
    qtd_cupons = dados.get('cupons', 0)
    aplicar_desconto = False
    if qtd_cupons > 0:
        aplicar_desconto = st.checkbox(f"Ativar Cupom (20% OFF) - Possui: {qtd_cupons}")

    col_loja, col_punicao = st.columns(2)

    with col_loja:
        st.subheader("Itens Disponíveis")
        itens_loja = {"60m de Jogo": 30, "Delivery": 250, "Cosmético": 1200, "Ver filme": 50, "1 Ep": 10}
        for item, preco_base in itens_loja.items():
            preco_final = preco_base
            if sorte_ativa == "Inflação": preco_final = int(preco_final * 1.2)
            if item == "Ver filme" and sorte_ativa == "Dia de Cinema": preco_final = 30
            if aplicar_desconto: preco_final = int(preco_final * 0.8)

            if st.button(f"{item} (-{preco_final}$)", use_container_width=True):
                if dados.get('saldo', 0) >= preco_final:
                    dados['saldo'] -= preco_final
                    if aplicar_desconto: dados['cupons'] -= 1
                    
                    # Registro seguro do gasto
                    dados["contadores"][f"Gasto_{item}"] = dados["contadores"].get(f"Gasto_{item}", 0) + 1
                    core.salvar_dados(dados)
                    st.rerun()
                else: 
                    st.error("Saldo insuficiente!")
            
            # Leitura segura para o texto de caption
            st.caption(f"Requisitados: {dados['contadores'].get(f'Gasto_{item}', 0)}")

    with col_punicao:
        st.subheader("⚠️ Punições")
        punicoes = {"Rede Social": 25, "Gasto Inútil": 100}
        for p, v in punicoes.items():
            v_final = v * 3 if sorte_ativa == "Não faça isso" else v
            if st.button(f"{p} (-{v_final}$)", use_container_width=True):
                dados['saldo'] = dados.get('saldo', 0) - v_final
                dados["contadores"][f"P_{p}"] = dados["contadores"].get(f"P_{p}", 0) + 1
                dados["ultima_punicao_data"] = str(datetime.utcnow().date())
                
                # Proteção estrutural de conquistas
                if "conquistas" not in dados:
                    dados["conquistas"] = {}
                if "incorruptivel" not in dados["conquistas"]:
                    dados["conquistas"]["incorruptivel"] = {"atual": 0}
                    
                dados["conquistas"]["incorruptivel"]["atual"] = 0
                core.salvar_dados(dados)
                st.rerun()
            st.caption(f"Ocorrências: {dados['contadores'].get(f'P_{p}', 0)}")
