import streamlit as st
import pandas as pd
import random
from itertools import combinations

st.set_page_config(
    page_title="Matriz de Partidos - Champions",
    layout="wide",  # "centered" para contenido centrado o "wide" para usar el ancho completo
    initial_sidebar_state="expanded"  # O "collapsed"
)

# Lista inicial
if "participants" not in st.session_state:
    st.session_state.participants = []

# Función para verificar que ningún equipo juegue dos veces
def es_valida(seleccion):
    equipos_usados = set()
    for partido in seleccion:
        equipo1, equipo2 = partido
        if equipo1 in equipos_usados or equipo2 in equipos_usados:
            return False
        equipos_usados.add(equipo1)
        equipos_usados.add(equipo2)
    return True

def generar_jornadas(partidos):
    jornadas = []

    parts = partidos.copy()

    while len(parts) > 0:
        # Buscar todas las combinaciones de 6 partidos
        combinaciones = combinations(parts, 6)

        # Filtrar las combinaciones válidas
        selecciones_validas = [seleccion for seleccion in combinaciones if es_valida(seleccion)]

        # Mostrar los resultados
        if selecciones_validas:
            for seleccion in selecciones_validas[:1]:  # Mostrar solo la primera solución válida
                jornadas.append(seleccion)

        for i in seleccion:
            parts.remove(i)

    
    return jornadas

# Función para agregar elementos a la lista
def add_item():
    item = st.session_state.new_item  # Obtener el valor del campo de entrada
    if item:  # Evitar agregar valores vacíos
        st.session_state.participants.append(item)
        st.session_state.new_item = ""  # Limpiar el campo de entrada

# Función para generar los cruces
def generar_cruces(bombos):
    # Inicializar una matriz 12x12 de partidos (sin partidos iniciales)
    matriz_cruces = pd.DataFrame([[None]*12 for _ in range(12)], columns=st.session_state.participants, index=st.session_state.participants)

    for b in bombos:
        a = random.sample(b, 4)
        for i, j in enumerate(a):
            matriz_cruces.loc[a[i],a[(i + 1) % len(a)]] = 'X' 

    comb = [(bombos[0], bombos[1]), (bombos[0], bombos[2],), (bombos[1],bombos[2])]

    for b1, b2 in comb:
        # Selección aleatoria de 4 equipos de cada bombo
        a = random.sample(b1, 4)
        b = random.sample(b2, 4)

        # Bucle para generar y mostrar los partidos
        for i in range(len(a)):
            matriz_cruces.loc[a[i], b[i]] = 'X'
            if i < len(a) - 1:
                matriz_cruces.loc[b[i], a[i+1]] = 'X'
            else:
                matriz_cruces.loc[b[i],a[0]] = 'X'

    return matriz_cruces

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
    # Generar la matriz de cruces
    matriz_cruces = generar_cruces([b1,b2,b3])

    # Mostrar la matriz en Streamlit
    st.title('Matriz de Partidos de la Champions')
    st.dataframe(matriz_cruces, height=460, use_container_width=True)

    sedes = ['PS5', 'PS4 - 24', 'PS4 - 23']
    random.shuffle(sedes)

    st.title('Distribución de sedes')
    st.write(f'Bombo 1 vs Bombo 1: Sede {sedes[0]}')
    st.write(f'Bombo 1 vs Bombo 2: Sede {sedes[2]}')
    st.write(f'Bombo 1 vs Bombo 3: Sede {sedes[1]}')
    st.write(f'Bombo 2 vs Bombo 2: Sede {sedes[1]}')
    st.write(f'Bombo 2 vs Bombo 3: Sede {sedes[0]}')
    st.write(f'Bombo 3 vs Bombo 3: Sede {sedes[2]}')

    partidos = [
        (fila, columna) 
        for fila, columna in matriz_cruces.where(matriz_cruces == "X").stack().index
    ]   

    st.title('Jornadas')
    #partidos = [('A', 'D'), ('A', 'E'), ('A', 'L'), ('B', 'C'), ('B', 'H'), ('B', 'J'), ('C', 'A'), ('C', 'G'), ('C', 'I'), ('D', 'B'), ('D', 'F'), ('D', 'K'), ('E', 'C'), ('E', 'H'), ('E', 'I'), ('F', 'A'), ('F', 'E'), ('F', 'K'), ('G', 'B'), ('G', 'F'), ('G', 'J'), ('H', 'D'), ('H', 'G'), ('H', 'L'), ('I', 'D'), ('I', 'G'), ('I', 'K'), ('J', 'A'), ('J', 'F'), ('J', 'I'), ('K', 'B'), ('K', 'H'), ('K', 'L'), ('L', 'C'), ('L', 'E'), ('L', 'J')]
    jornadas = generar_jornadas(partidos)

    for i, x in enumerate(jornadas):
        st.subheader(f"Jornada {i+1}")
        for j in x:
            st.write(f'{j[0]} - {j[1]}')

