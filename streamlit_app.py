import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="App PRO de Apuestas", layout="centered")

st.title("💰 App PRO de Apuestas")

# =========================
# ARCHIVOS
# =========================
if not os.path.exists("jugadores.json"):
    with open("jugadores.json", "w") as f:
        json.dump({}, f)

if not os.path.exists("historial.json"):
    with open("historial.json", "w") as f:
        json.dump([], f)

# =========================
# CARGAR DATOS
# =========================
with open("jugadores.json", "r") as f:
    jugadores = json.load(f)

with open("historial.json", "r") as f:
    historial = json.load(f)

# =========================
# AGREGAR JUGADOR
# =========================
st.subheader("➕ Agregar jugador")

col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre")

with col2:
    elo = st.number_input("ELO", value=1500)

racha = st.number_input("Racha", value=0)

if st.button("Guardar jugador"):
    if nombre != "":
        jugadores[nombre] = {"elo": elo, "racha": racha}
        with open("jugadores.json", "w") as f:
            json.dump(jugadores, f)
        st.success("Jugador guardado")

# =========================
# SELECCIÓN
# =========================
st.subheader("🎯 Análisis de apuesta")

if len(jugadores) < 2:
    st.warning("Agrega al menos 2 jugadores")
    st.stop()

lista = list(jugadores.keys())

jugador_a = st.selectbox("Jugador A", lista)
jugador_b = st.selectbox("Jugador B", lista)

cuota = st.number_input("Cuota", value=2.0)
bankroll = st.number_input("Bankroll", value=100.0)

# =========================
# PROBABILIDAD (ELO + RACHA)
# =========================
def probabilidad(elo_a, elo_b, racha_a, racha_b):
    base = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
    ajuste = (racha_a - racha_b) * 0.01
    return max(0, min(1, base + ajuste))

# =========================
# ANALIZAR
# =========================
if st.button("Analizar"):
    elo_a = jugadores[jugador_a]["elo"]
    elo_b = jugadores[jugador_b]["elo"]

    racha_a = jugadores[jugador_a]["racha"]
    racha_b = jugadores[jugador_b]["racha"]

    p = probabilidad(elo_a, elo_b, racha_a, racha_b)
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

    # =========================
    # GUARDAR EN HISTORIAL
    # =========================
    registro = {
        "jugador_a": jugador_a,
        "jugador_b": jugador_b,
        "probabilidad": round(p, 4),
        "valor": round(valor, 4),
        "cuota": cuota
    }

    historial.append(registro)

    with open("historial.json", "w") as f:
        json.dump(historial, f)

# =========================
# HISTORIAL
# =========================
st.subheader("📜 Historial")

if len(historial) > 0:
    df = pd.DataFrame(historial)
    st.dataframe(df)
else:
    st.write("Sin datos aún")

# =========================
# RANKING
# =========================
st.subheader("🏆 Ranking de jugadores")

ranking = []

for nombre, datos in jugadores.items():
    score = datos["elo"] + (datos["racha"] * 10)
    ranking.append({"Jugador": nombre, "Score": score})

df_rank = pd.DataFrame(ranking).sort_values(by="Score", ascending=False)

st.dataframe(df_rank)

# =========================
# GRÁFICO SIMPLE
# =========================
if len(historial) > 0:
    st.subheader("📈 Evolución del valor")
    valores = [h["valor"] for h in historial]
    st.line_chart(valores)
