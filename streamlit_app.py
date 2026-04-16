import streamlit as st
import json
import os

st.set_page_config(page_title="App PRO Apuestas", layout="centered")

st.title("🔥 App PRO con Forma Real")

# =========================
# CREAR ARCHIVO SI NO EXISTE
# =========================
if not os.path.exists("jugadores.json"):
    jugadores = {
        "Jugador A": {"elo": 1500, "historial": [1,0,1,1,0]},
        "Jugador B": {"elo": 1450, "historial": [0,1,0,0,1]}
    }
    json.dump(jugadores, open("jugadores.json", "w"))

# =========================
# CARGAR
# =========================
jugadores = json.load(open("jugadores.json"))

# =========================
# FUNCIONES
# =========================
def calcular_forma(historial):
    ultimos = historial[-5:]
    return sum(ultimos)

def probabilidad(elo_a, elo_b, forma_a, forma_b):
    base = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
    ajuste = (forma_a - forma_b) * 0.03
    return max(0, min(1, base + ajuste))

def mostrar_forma(nombre):
    historial = jugadores[nombre]["historial"][-5:]
    texto = ""
    for r in historial:
        if r == 1:
            texto += "🟢 "
        else:
            texto += "🔴 "
    st.write(f"{nombre}: {texto}")

# =========================
# AGREGAR JUGADOR
# =========================
st.subheader("➕ Nuevo jugador")

nombre = st.text_input("Nombre")
elo = st.number_input("ELO", value=1500)

if st.button("Guardar jugador"):
    if nombre != "":
        jugadores[nombre] = {"elo": elo, "historial": []}
        json.dump(jugadores, open("jugadores.json", "w"))
        st.success("Jugador creado")

# =========================
# VALIDACIÓN
# =========================
if len(jugadores) < 2:
    st.warning("Agrega al menos 2 jugadores")
    st.stop()

# =========================
# SELECCIÓN
# =========================
st.subheader("🎯 Análisis")

lista = list(jugadores.keys())

jugador_a = st.selectbox("Jugador A", lista)
jugador_b = st.selectbox("Jugador B", lista)

cuota = st.number_input("Cuota", value=2.0)

# =========================
# MOSTRAR FORMA
# =========================
st.subheader("📊 Forma reciente")

mostrar_forma(jugador_a)
mostrar_forma(jugador_b)

# =========================
# CALCULAR
# =========================
if st.button("Analizar"):
    forma_a = calcular_forma(jugadores[jugador_a]["historial"])
    forma_b = calcular_forma(jugadores[jugador_b]["historial"])

    elo_a = jugadores[jugador_a]["elo"]
    elo_b = jugadores[jugador_b]["elo"]

    p = probabilidad(elo_a, elo_b, forma_a, forma_b)
    valor = (p * cuota) - 1

    st.subheader("📈 Resultado")
    st.write(f"Probabilidad: {p*100:.2f}%")
    st.write(f"Valor esperado: {valor:.2f}")

    if valor > 0:
        st.success("✅ Apuesta con valor")
    else:
        st.error("❌ No apostar")

# =========================
# REGISTRAR PARTIDO
# =========================
st.subheader("📝 Registrar resultado")

jugador = st.selectbox("Jugador", lista)
resultado = st.radio("Resultado", ["Ganó", "Perdió"])

if st.button("Guardar resultado"):
    if resultado == "Ganó":
        jugadores[jugador]["historial"].append(1)
    else:
        jugadores[jugador]["historial"].append(0)

    json.dump(jugadores, open("jugadores.json", "w"))
    st.success("Resultado guardado")
