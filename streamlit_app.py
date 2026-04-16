import streamlit as st
import json
import os

st.set_page_config(page_title="App PRO de Apuestas", layout="centered")

st.title("💰 App PRO de Apuestas")

# ==========================
# Cargar o crear jugadores.json automáticamente
# ==========================
if not os.path.exists("jugadores.json"):
    jugadores = {
        "Jugador A": {"elo": 1500, "racha": 0},
        "Jugador B": {"elo": 1450, "racha": 0}
    }
    with open("jugadores.json", "w") as f:
        json.dump(jugadores, f)
else:
    try:
        with open("jugadores.json", "r") as f:
            jugadores = json.load(f)
    except:
        jugadores = {}

# ==========================
# Validación si no hay jugadores
# ==========================
if len(jugadores) == 0:
    st.warning("No hay jugadores guardados. Agrega uno abajo 👇")

# ==========================
# Selección de jugadores
# ==========================
st.subheader("🎮 Selección de jugadores")

lista_jugadores = list(jugadores.keys())

if len(lista_jugadores) > 0:
    jugador_a = st.selectbox("Jugador A", lista_jugadores)
    jugador_b = st.selectbox("Jugador B", lista_jugadores)
else:
    jugador_a = None
    jugador_b = None

# ==========================
# Inputs
# ==========================
st.subheader("📊 Datos de apuesta")

cuota = st.number_input("Cuota", value=2.00)
bankroll = st.number_input("Bankroll", value=100.00)

# ==========================
# Cálculo
# ==========================
if jugador_a and jugador_b:

    if jugador_a != jugador_b:

        elo_a = jugadores[jugador_a]["elo"]
        elo_b = jugadores[jugador_b]["elo"]

        racha_a = jugadores[jugador_a]["racha"]
        racha_b = jugadores[jugador_b]["racha"]

        # Probabilidad con ELO
        prob = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

        # Ajuste por racha
        prob += (racha_a - racha_b) * 0.01

        prob = max(0, min(prob, 1))

        # Valor esperado
        valor_esperado = (prob * cuota) - 1

        # Kelly
        kelly = ((prob * cuota) - 1) / (cuota - 1)
        kelly = max(0, kelly)

        apuesta = bankroll * kelly

        # ==========================
        # Mostrar resultado
        # ==========================
        st.subheader("📈 Resultado")

        st.write(f"Probabilidad de ganar: {prob*100:.2f}%")
        st.write(f"Valor esperado: {valor_esperado:.2f}")

        if valor_esperado > 0:
            st.success("✅ Apuesta con valor")
        else:
            st.error("❌ Apuesta sin valor")

        st.write(f"Apuesta recomendada: ${apuesta:.2f}")

    else:
        st.warning("Selecciona jugadores diferentes")

# ==========================
# Agregar jugadores
# ==========================
st.subheader("➕ Agregar jugador")

nombre_nuevo = st.text_input("Nombre del jugador")
elo_nuevo = st.number_input("ELO inicial", value=1500)
racha_nueva = st.number_input("Racha", value=0)

if st.button("Guardar jugador"):

    if nombre_nuevo.strip() != "":
        jugadores[nombre_nuevo] = {
            "elo": elo_nuevo,
            "racha": racha_nueva
        }

        with open("jugadores.json", "w") as f:
            json.dump(jugadores, f, indent=4)

        st.success(f"Jugador {nombre_nuevo} guardado ✅")
        st.rerun()

    else:
        st.error("Escribe un nombre válido")
