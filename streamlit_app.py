import json
import streamlit as st import streamlit as st

st.title("💰 App PRO de Apuestas")

# Base de jugadores (mejorada)
jugadores = {
    "Jugador A": {"elo": 1500, "racha": 3},
    "Jugador B": {"elo": 1450, "racha": -1},
    "Jugador C": {"elo": 1550, "racha": 5},
}

# Selección
jugador_a = st.selectbox("Jugador A", list(jugadores.keys()))
jugador_b = st.selectbox("Jugador B", list(jugadores.keys()))

cuota = st.number_input("Cuota", value=2.0)
bankroll = st.number_input("Bankroll", value=100.0)

# Ajuste por racha
def elo_ajustado(elo, racha):
    return elo + (racha * 20)

# Probabilidad
def probabilidad(elo_a, elo_b):
    return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

# Botón
if st.button("Analizar"):
    elo_a = elo_ajustado(jugadores[jugador_a]["elo"], jugadores[jugador_a]["racha"])
    elo_b = elo_ajustado(jugadores[jugador_b]["elo"], jugadores[jugador_b]["racha"])

    prob = probabilidad(elo_a, elo_b)

    valor = (prob * cuota) - 1

    # Kelly conservador (50%)
    kelly = ((prob * cuota) - 1) / (cuota - 1)
    apuesta = bankroll * max(kelly * 0.5, 0)

    st.subheader("Resultado")

    st.write(f"Probabilidad ajustada: {prob:.2%}")
    st.write(f"Valor esperado: {valor:.2f}")

    if valor > 0:
        st.success("✅ Apuesta con valor")
        st.write(f"Apuesta recomendada: ${apuesta:.2f}")
    else:
        st.error("❌ No vale la pena apostar")
st.subheader("➕ Agregar jugador")

if "jugadores" not in st.session_state:
    st.session_state.jugadores = {
        "Jugador A": {"elo": 1500, "racha": 3},
        "Jugador B": {"elo": 1450, "racha": -1},
    }

nombre = st.text_input("Nombre del jugador")
elo = st.number_input("ELO", value=1500)
racha = st.number_input("Racha", value=0)

if st.button("Agregar jugador"):
    if nombre != "":
        st.session_state.jugadores[nombre] = {
            "elo": elo,
            "racha": racha
        }
        st.success(f"{nombre} agregado correctamente")
        
