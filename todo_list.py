import requests
import streamlit as st
import json
import os
import uuid
from datetime import datetime

ARQUIVO_TAREFAS = "tarefas.json"


FIREBASE_URL_TAREFAS = "https://gamix2-57898-default-rtdb.firebaseio.com/tarefas.json"

def carregar_tarefas():
    try:
        resposta = requests.get(FIREBASE_URL_TAREFAS)
        if resposta.status_code == 200 and resposta.json() is not None:
            return resposta.json()
    except Exception:
        pass
    return []

def salvar_tarefas(tarefas):
    requests.put(FIREBASE_URL_TAREFAS, json=tarefas)


def renderizar_todo_list():
    st.divider()
    st.markdown("<h3 style='text-align: center;'>📝 Lista de Tarefas</h3>", unsafe_allow_html=True)

    if "tarefas" not in st.session_state:
        st.session_state.tarefas = carregar_tarefas()

    with st.expander("Adicionar Nova Tarefa", expanded=True):
        col_nome, col_data = st.columns([0.7, 0.3])
        with col_nome:
            nova_tarefa = st.text_input("Nome da tarefa:")
        with col_data:
            nova_data = st.date_input("Data:")
            
        col_pri, col_cor, col_btn = st.columns([0.4, 0.3, 0.3])
        with col_pri:
            nova_prioridade = st.selectbox("Prioridade (0 é mais urgente):", [0, 1, 2])
        with col_cor:
            nova_cor = st.color_picker("Cor da Etiqueta:", "#FF4B4B")
        with col_btn:
            st.write("") 
            st.write("")
            if st.button("Adicionar Tarefa", use_container_width=True):
                if nova_tarefa.strip():
                    st.session_state.tarefas.append({
                        "id": str(uuid.uuid4()),
                        "nome": nova_tarefa.strip(),
                        "data": str(nova_data),
                        "prioridade": nova_prioridade,
                        "cor": nova_cor
                    })
                    salvar_tarefas(st.session_state.tarefas)
                    st.rerun()

    st.write("")
    
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
        cor = tarefa.get("cor", "#ffffff")
        pri = tarefa.get("prioridade", 2)
        data_t = tarefa.get("data", "")
        
        col1, col2 = st.columns([0.90, 0.10])
        with col1:
            html_tarefa = f"""
            <div style="border-left: 5px solid {cor}; padding-left: 10px; margin-bottom: 5px; background-color: #262730; padding: 10px; border-radius: 5px;">
                <strong style="font-size: 16px;">{nome}</strong><br>
                <span style="font-size: 13px; color: #8a8a9d;">Prioridade: {pri} | Data: {datetime.strptime(data_t, '%Y-%m-%d').strftime('%d/%m/%Y')}</span>
            </div>
            """
            st.markdown(html_tarefa, unsafe_allow_html=True)
            concluida = st.checkbox("Concluir", key=f"chk_{t_id}")
            
        with col2:
            st.write("")
            remover = st.button("🗑️", key=f"del_{t_id}", help="Remover tarefa")
        
        if concluida or remover:
            tarefas_restantes = [t for t in tarefas_restantes if t["id"] != t_id]
            houve_alteracao = True

    if houve_alteracao:
        st.session_state.tarefas = tarefas_restantes
        salvar_tarefas(st.session_state.tarefas)
        st.rerun()