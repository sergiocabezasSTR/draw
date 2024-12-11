import streamlit as st

# Lista inicial
if "participants" not in st.session_state:
    st.session_state.participants = []

# Función para agregar elementos a la lista
def add_item():
    item = st.session_state.new_item  # Obtener el valor del campo de entrada
    if item:  # Evitar agregar valores vacíos
        st.session_state.participants.append(item)
        st.session_state.new_item = ""  # Limpiar el campo de entrada

st.title("Agregar participantes")

# Campo de entrada para nuevos elementos
st.text_input("Nuevo participante:", key="new_item")

# Botón para agregar el elemento a la lista
st.button("Agregar", on_click=add_item)

# Botón para agregar el elemento a la lista
b1 = st.multiselect('BOMBO 1', options=st.session_state.participants)
b2 = st.multiselect('BOMBO 2', options=st.session_state.participants)
b3 = st.multiselect('BOMBO 3', options=st.session_state.participants)