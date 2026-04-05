import streamlit as st
import core
from datetime import datetime, timedelta

def renderizar(dados):
    st.title("Loja e Gastos")
    
    agora_br = datetime.utcnow() - timedelta(hours=3)
    hoje_str = agora_br.strftime("%d/%m/%Y")
    
    if type(dados.get("sorte_dia")) is not dict:
        dados["sorte_dia"] = {"data": "", "efeito": None}
    if type(dados.get("contadores")) is not dict:
        dados["contadores"] = {}
        
    sorte_ativa = dados["sorte_dia"].get("efeito")
    qtd_cupons = dados.get('cupons', 0)
    
    col_loja, col_direita = st.columns([1.3, 1])

    with col_direita:
        # ==========================================
        # 1. CUPONS DE DESCONTO
        # ==========================================
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>🎫 Cupons de Desconto</h3>", unsafe_allow_html=True)
            aplicar_desconto = False
            if qtd_cupons > 0:
                aplicar_desconto = st.checkbox(f"Ativar Cupom (20% OFF) - Possui: {qtd_cupons}")
                if aplicar_desconto:
                    st.markdown("<div style='color: #6e0b8a; font-weight: bold; font-family: \"VT323\", monospace; font-size: 20px;'>[ Cupom Ativado! Preços reduzidos. ]</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='font-family: \"VT323\", monospace; font-size: 18px;'>Você não possui cupons no momento.</div>", unsafe_allow_html=True)
                st.caption("Suba de nível para ganhar cupons.")

        # ==========================================
        # 2. PUNIÇÕES
        # ==========================================
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>⚠️ Punições</h3>", unsafe_allow_html=True)
            punicoes = {"Rede Social": 25, "Gasto Inútil": 100}
            
            st.markdown("""
            <div style='display: flex; font-weight: bold; border-bottom: 2px solid #000000; padding-bottom: 5px; margin-bottom: 10px; font-family: "VT323", monospace; font-size: 20px;'>
                <div style='flex: 2;'>Infração</div>
                <div style='flex: 1; text-align: center;'>Multa</div>
                <div style='flex: 1; text-align: center;'>Ação</div>
            </div>
            """, unsafe_allow_html=True)

            for p, v in punicoes.items():
                v_final = v * 3 if sorte_ativa == "Não faça isso" else v
                chave_p = f"P_{p.replace(' ', '_')}"
                
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.markdown(f"<div style='margin-top: 2px; font-family: \"VT323\", monospace;'><strong style='font-size: 20px;'>{p}</strong><br><span style='font-size: 16px; color: #666666;'>Ocorrências: {dados['contadores'].get(chave_p, 0)}</span></div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<div style='margin-top: 2px; text-align: center; color: #b30000; font-weight: bold; font-family: \"VT323\", monospace; font-size: 26px;'>-{v_final}$</div>", unsafe_allow_html=True)
                with c3:
                    if st.button("Assumir", key=f"btn_{chave_p}", use_container_width=True):
                        dados['saldo'] = dados.get('saldo', 0) - v_final
                        dados["contadores"][chave_p] = dados["contadores"].get(chave_p, 0) + 1
                        dados["ultima_punicao_data"] = str(datetime.utcnow().date())
                        
                        if "conquistas" not in dados:
                            dados["conquistas"] = {}
                        if "incorruptivel" not in dados["conquistas"]:
                            dados["conquistas"]["incorruptivel"] = {"atual": 0}
                            
                        dados["conquistas"]["incorruptivel"]["atual"] = 0
                        core.salvar_dados(dados)
                        st.rerun()
                st.markdown("<hr style='margin: 5px 0; border-top: 1px dotted #808080;'>", unsafe_allow_html=True)

        # ==========================================
        # 3. INFLUÊNCIA DA SORTE DO DIA
        # ==========================================
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>🎲 Influência do Dia</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-family: \"VT323\", monospace; font-size: 18px; margin-bottom: 8px;'>Data Atual: <strong>{hoje_str}</strong></div>", unsafe_allow_html=True)
            
            if sorte_ativa == "Inflação":
                st.markdown("<div style='color: #b30000; font-family: \"VT323\", monospace; font-size: 22px; font-weight: bold; background-color: #ffcccc; padding: 5px; border: 2px solid #b30000; text-align: center;'>[!] INFLAÇÃO ATIVA<br>Todos os preços sofreram aumento de +20%</div>", unsafe_allow_html=True)
            elif sorte_ativa == "Dia de Cinema":
                st.markdown("<div style='color: #000080; font-family: \"VT323\", monospace; font-size: 22px; font-weight: bold; background-color: #ccccff; padding: 5px; border: 2px solid #000080; text-align: center;'>[+] DIA DE CINEMA<br>Assistir a um filme custa apenas 30$</div>", unsafe_allow_html=True)
            elif sorte_ativa == "Não faça isso":
                st.markdown("<div style='color: #b30000; font-family: \"VT323\", monospace; font-size: 22px; font-weight: bold; background-color: #ffcccc; padding: 5px; border: 2px solid #b30000; text-align: center;'>[!] NÃO FAÇA ISSO<br>As Punições estão cobrando o triplo (x3)</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #000000; font-family: \"VT323\", monospace; font-size: 20px; font-weight: bold; background-color: #DFDFDF; padding: 5px; border: 2px solid #000000; text-align: center;'>Status Normal<br>Sem alterações no mercado hoje.</div>", unsafe_allow_html=True)

    with col_loja:
        # ==========================================
        # 4. ITENS DA LOJA
        # ==========================================
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>🛍️ Itens Disponíveis</h3>", unsafe_allow_html=True)
            
            itens_loja = {
                "60m de Jogo": 30, 
                "Delivery": 250, 
                "Cosmético": 1200, 
                "Ver filme": 50,
                "1 Episódio Série": 10,
                "1 Capítulo Novel": 4,
                "10 Capítulos Novel": 36
            }
            
            st.markdown("""
            <div style='display: flex; font-weight: bold; border-bottom: 2px solid #000000; padding-bottom: 5px; margin-bottom: 10px; font-family: "VT323", monospace; font-size: 20px;'>
                <div style='flex: 2;'>Item</div>
                <div style='flex: 1; text-align: center;'>Preço</div>
                <div style='flex: 1; text-align: center;'>Ação</div>
            </div>
            """, unsafe_allow_html=True)
            
            for item, preco_base in itens_loja.items():
                preco_final = preco_base
                
                if sorte_ativa == "Inflação": 
                    preco_final = int(preco_final * 1.2)
                if item == "Ver filme" and sorte_ativa == "Dia de Cinema": 
                    preco_final = 30
                if aplicar_desconto: 
                    preco_final = int(preco_final * 0.8)

                chave_contador = f"Gasto_{item.replace(' ', '_')}"
                
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.markdown(f"<div style='margin-top: 2px; font-family: \"VT323\", monospace;'><strong style='font-size: 20px;'>{item}</strong><br><span style='font-size: 16px; color: #666666;'>Comprados: {dados['contadores'].get(chave_contador, 0)}</span></div>", unsafe_allow_html=True)
                with c2:
                    cor_preco = "#6e0b8a" if aplicar_desconto or (item == "Ver filme" and sorte_ativa == "Dia de Cinema") else "#000000"
                    st.markdown(f"<div style='margin-top: 2px; text-align: center; color: {cor_preco}; font-weight: bold; font-family: \"VT323\", monospace; font-size: 26px;'>{preco_final}$</div>", unsafe_allow_html=True)
                with c3:
                    if st.button("Comprar", key=f"buy_{chave_contador}", use_container_width=True):
                        if dados.get('saldo', 0) >= preco_final:
                            dados['saldo'] -= preco_final
                            if aplicar_desconto: 
                                dados['cupons'] -= 1
                            
                            dados["contadores"][chave_contador] = dados["contadores"].get(chave_contador, 0) + 1
                            core.salvar_dados(dados)
                            st.rerun()
                        else: 
                            st.error("Saldo insuficiente!")
                
                st.markdown("<hr style='margin: 5px 0; border-top: 1px dotted #808080;'>", unsafe_allow_html=True)
