import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Matriz de Partidos - Champions",
    layout="wide",  # "centered" para contenido centrado o "wide" para usar el ancho completo
    initial_sidebar_state="expanded"  # O "collapsed"
)

# Lista inicial
if "participants" not in st.session_state:
    st.session_state.participants = []

# Función para agregar elementos a la lista
def add_item():
    item = st.session_state.new_item  # Obtener el valor del campo de entrada
    if item:  # Evitar agregar valores vacíos
        st.session_state.participants.append(item)
        st.session_state.new_item = ""  # Limpiar el campo de entrada

# Asignar partidos
def asignar_partidos(equipos_bombo, otros_bombos):
    for equipo in equipos_bombo:
        # Partidos contra 2 equipos de su mismo bombo (1 casa, 1 fuera)
        mismos_bombo = [e for e in equipos_bombo if e != equipo]
        vs_mismos_bombo = random.sample(mismos_bombo, 2)
        partidos.loc[equipo, vs_mismos_bombo[0]] = "H"  # En casa
        partidos.loc[vs_mismos_bombo[0], equipo] = "A"  # Fuera
        partidos.loc[equipo, vs_mismos_bombo[1]] = "A"  # Fuera
        partidos.loc[vs_mismos_bombo[1], equipo] = "H"  # En casa

        # Partidos contra equipos de otros bombos (1 casa, 1 fuera por bombo)
        for otro_bombo in otros_bombos:
            vs_otro_bombo = random.sample(otro_bombo, 2)
            partidos.loc[equipo, vs_otro_bombo[0]] = "H"  # En casa
            partidos.loc[vs_otro_bombo[0], equipo] = "A"  # Fuera
            partidos.loc[equipo, vs_otro_bombo[1]] = "A"  # Fuera
            partidos.loc[vs_otro_bombo[1], equipo] = "H"  # En casa

st.title("TORNEO FIFA NAVIDAD - 21/12/2024")
st.subheader("Participantes")
c1, c2 = st.columns(2)

c1.write('Lista')
c1.dataframe(pd.DataFrame(st.session_state.participants, columns=['Nombre']), use_container_width=True)

c2.write("Agregar participantes")

# Campo de entrada para nuevos elementos
c2.text_input("Nuevo participante:", key="new_item")

# Botón para agregar el elemento a la lista
c2.button("Agregar", on_click=add_item, disabled=len(st.session_state.participants) >= 12)

# Botón para agregar el elemento a la lista
c2.write("Eliminar participantes")
row_to_delete = c2.selectbox("Selecciona el ID de la fila que deseas eliminar:", st.session_state.participants)

# Botón para eliminar
if c2.button("Eliminar"):
    st.session_state.participants.remove(row_to_delete)
    st.rerun()

st.subheader("Sorteo")
# Botón para agregar el elemento a la lista
b1 = st.multiselect('BOMBO 1', options=st.session_state.participants, max_selections=4)
b2 = st.multiselect('BOMBO 2', options=[
        item for item in st.session_state.participants if item not in b1
    ], max_selections=4)
b3 = st.multiselect('BOMBO 3', options=[
        item for item in st.session_state.participants if item not in (b1 + b2)
    ], max_selections=4)

av_sort = len(b1) == len(b2) == len(b3) == 4

# Combinar todos los equipos en una lista
todos_los_equipos = b1 + b2 + b3

# Realizar el sorteo para cada bombo
if st.button("Sortear", disabled=not av_sort):
    # Inicializar matriz de partidos (12x12)
    partidos = pd.DataFrame("", index=todos_los_equipos, columns=todos_los_equipos)
    asignar_partidos(b1, [b2, b3])
    asignar_partidos(b2, [b1, b3])
    asignar_partidos(b3, [b1, b2])

    # Mostrar la matriz en Streamlit
    st.title("Matriz de Partidos (Casa (H) y Fuera (A))")
    st.write("La matriz muestra 'H' si el equipo juega en casa y 'A' si juega fuera.")
    st.table(partidos)

# Lista de 12 equipos (puedes personalizarlos)
equipos = ['Equipo A', 'Equipo B', 'Equipo C', 'Equipo D', 'Equipo E', 'Equipo F', 'Equipo G', 'Equipo H', 
           'Equipo I', 'Equipo J', 'Equipo K', 'Equipo L']

# Dividir los equipos en 3 bombos (4 equipos por bombo)
bombos = {
    'Bombo 1': equipos[:4],
    'Bombo 2': equipos[4:8],
    'Bombo 3': equipos[8:]
}

# Función para generar los cruces
def generar_cruces(bombos):
    # Inicializar una matriz 12x12 de partidos (sin partidos iniciales)
    matriz_cruces = pd.DataFrame([[None]*12 for _ in range(12)], columns=equipos, index=equipos)

    for i, equipo in enumerate(equipos):
        # Obtener el bombo del equipo actual
        bombo_actual = None
        for bombo, lista_equipos in bombos.items():
            if equipo in lista_equipos:
                bombo_actual = lista_equipos
                break

        partidos_bombo_actual = 0
        partidos_otro_bombo = 0

        # Elegir 2 equipos del mismo bombo (incluyendo el equipo actual)
        rivales_bombo_actual = [x for x in bombo_actual if x != equipo]
        rivales_bombo_actual = random.sample(rivales_bombo_actual, 2)
        for rival in rivales_bombo_actual:
            # Asignar partidos de casa y fuera
            if random.choice([True, False]):
                matriz_cruces.at[equipo, rival] = 'Casa'
                matriz_cruces.at[rival, equipo] = 'Fuera'
                partidos_bombo_actual += 1
            else:
                matriz_cruces.at[equipo, rival] = 'Fuera'
                matriz_cruces.at[rival, equipo] = 'Casa'
                partidos_bombo_actual += 1

        # Ahora que tenemos los partidos dentro del mismo bombo, agregamos los partidos con equipos de otros bombos
        # Elegir 2 equipos de cada uno de los otros bombos
        for bombo, lista_equipos in bombos.items():
            if bombo != bombo_actual:
                rivales_bombo = random.sample(lista_equipos, 2)
                for rival in rivales_bombo:
                    if partidos_otro_bombo < 4:  # Asegurarse de que se jueguen 4 partidos contra otros bombos
                        if random.choice([True, False]):
                            matriz_cruces.at[equipo, rival] = 'Casa'
                            matriz_cruces.at[rival, equipo] = 'Fuera'
                        else:
                            matriz_cruces.at[equipo, rival] = 'Fuera'
                            matriz_cruces.at[rival, equipo] = 'Casa'
                        partidos_otro_bombo += 1

        # Verificar si el equipo ha jugado los 6 partidos (esto debería suceder automáticamente con las condiciones anteriores)
        if partidos_bombo_actual + partidos_otro_bombo != 6:
            raise ValueError(f"El equipo {equipo} no ha jugado 6 partidos.")

    return matriz_cruces

# Generar la matriz de cruces
matriz_cruces = generar_cruces(bombos)

# Mostrar la matriz en Streamlit
st.title('Matriz de Partidos de la Champions')
st.dataframe(matriz_cruces, use_container_width=True)