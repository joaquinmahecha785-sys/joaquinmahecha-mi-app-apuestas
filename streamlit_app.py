import streamlit as st
import json
import os

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="App PRO de Apuestas", layout="centered")

st.title("💰 App PRO de Apuestas")

# =========================
# CARGAR O CREAR JUGADORES
# =========================
if not os.path.exists("jugadores.json"):
    jugadores = {
        "Jugador A": {"elo": 1500, "racha": 0},
        "Jugador B": {"elo": 1450, "racha": 0}
    }
    with open("jugadores.json", "w") as f:
        json.dump(jugadores, f)
else:
    with open("jugadores.json", "r") as f:
        jugadores = json.load(f)

# =========================
# AGREGAR JUGADORES
# =========================
st.subheader("➕ Agregar nuevo jugador")

nombre = st.text_input("Nombre del jugador")
elo = st.number_input("ELO", value=1500)
racha = st.number_input("Racha", value=0)

if st.button("Guardar jugador"):
    if nombre != "":
        jugadores[nombre] = {"elo": elo, "racha": racha}
        with open("jugadores.json", "w") as f:
            json.dump(jugadores, f)
        st.success("Jugador guardado ✅")

# =========================
# SELECCIÓN
# =========================
st.subheader("🎯 Seleccionar jugadores")

lista_jugadores = list(jugadores.keys())

jugador_a = st.selectbox("Jugador A", lista_jugadores)
jugador_b = st.selectbox("Jugador B", lista_jugadores)

cuota = st.number_input("Cuota", value=2.0)
bankroll = st.number_input("Bankroll", value=100.0)

# =========================
# CÁLCULO
# =========================
def probabilidad(elo_a, elo_b):
    return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

if st.button("Analizar"):
    elo_a = jugadores[jugador_a]["elo"]
    elo_b = jugadores[jugador_b]["elo"]

    p = probabilidad(elo_a, elo_b)
    valor = (p * cuota) - 1

    st.subheader("📊 Resultado")
    st.write(f"Probabilidad: {p*100:.2f}%")
    st.write(f"Valor esperado: {valor:.2f}")

    if valor > 0:
        apuesta = bankroll * (valor / cuota)
        st.success("✅ Apuesta con valor")
        st.write(f"Apuesta recomendada: ${apuesta:.2f}")
    else:
        st.error("❌ No apostar")
