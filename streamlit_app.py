import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="App DIOS de Apuestas", layout="centered")

st.title("🔥 App DIOS de Apuestas")

# =========================
# ARCHIVOS
# =========================
if not os.path.exists("jugadores.json"):
    with open("jugadores.json", "w") as f:
        json.dump({}, f)

if not os.path.exists("historial.json"):
    with open("historial.json", "w") as f:
        json.dump([], f)

if not os.path.exists("bankroll.json"):
    with open("bankroll.json", "w") as f:
        json.dump({"saldo": 100}, f)

# =========================
# CARGAR DATOS
# =========================
jugadores = json.load(open("jugadores.json"))
historial = json.load(open("historial.json"))
bankroll_data = json.load(open("bankroll.json"))

saldo = bankroll_data["saldo"]

st.metric("💰 Bankroll actual", f"${saldo:.2f}")

# =========================
# AGREGAR JUGADOR
# =========================
st.subheader("➕ Nuevo jugador")

nombre = st.text_input("Nombre jugador")
elo = st.number_input("ELO", value=1500)
racha = st.number_input("Racha", value=0)

if st.button("Guardar jugador"):
    if nombre != "":
        jugadores[nombre] = {"elo": elo, "racha": racha}
        json.dump(jugadores, open("jugadores.json", "w"))
        st.success("Jugador guardado")

# =========================
# VALIDACIÓN
# =========================
if len(jugadores) < 2:
    st.warning("Agrega al menos 2 jugadores")
    st.stop()

# =========================
# SELECCIÓN
# =========================
st.subheader("🎯 Nueva apuesta")

lista = list(jugadores.keys())

jugador_a = st.selectbox("Jugador A", lista)
jugador_b = st.selectbox("Jugador B", lista)

cuota = st.number_input("Cuota", value=2.0)

# =========================
# PROBABILIDAD PRO
# =========================
def probabilidad(elo_a, elo_b, racha_a, racha_b):
    base = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
    ajuste = (racha_a - racha_b) * 0.015
    return max(0, min(1, base + ajuste))

# =========================
# ANALIZAR
# =========================
if st.button("Analizar apuesta"):
    elo_a = jugadores[jugador_a]["elo"]
    elo_b = jugadores[jugador_b]["elo"]

    racha_a = jugadores[jugador_a]["racha"]
    racha_b = jugadores[jugador_b]["racha"]

    p = probabilidad(elo_a, elo_b, racha_a, racha_b)
    valor = (p * cuota) - 1

    st.subheader("📊 Resultado")

    st.write(f"Probabilidad: {p*100:.2f}%")
    st.write(f"Valor esperado: {valor:.2f}")

    # 🤖 RECOMENDACIÓN IA
    if p > 0.6 and valor > 0:
        st.success("🤖 IA: Apuesta FUERTE")
    elif p > 0.5:
        st.info("🤖 IA: Apuesta moderada")
    else:
        st.error("🤖 IA: No apostar")

    # Kelly
    if valor > 0:
        apuesta = saldo * (valor / cuota)
        st.write(f"💸 Apuesta sugerida: ${apuesta:.2f}")
    else:
        apuesta = 0

    # =========================
    # RESULTADO REAL
    # =========================
    resultado = st.radio("Resultado real", ["Pendiente", "Ganada", "Perdida"])

    if st.button("Guardar resultado"):
        if resultado != "Pendiente":

            if resultado == "Ganada":
                ganancia = apuesta * (cuota - 1)
                saldo += ganancia
            else:
                saldo -= apuesta

            # Guardar bankroll
            json.dump({"saldo": saldo}, open("bankroll.json", "w"))

            # Guardar historial
            historial.append({
                "jugador_a": jugador_a,
                "jugador_b": jugador_b,
                "probabilidad": round(p, 3),
                "valor": round(valor, 3),
                "cuota": cuota,
                "apuesta": round(apuesta, 2),
                "resultado": resultado,
                "saldo": round(saldo, 2)
            })

            json.dump(historial, open("historial.json", "w"))

            st.success("Resultado guardado 🔥")

# =========================
# HISTORIAL
# =========================
st.subheader("📜 Historial de apuestas")

if historial:
    df = pd.DataFrame(historial)
    st.dataframe(df)

    st.subheader("📈 Evolución del bankroll")
    st.line_chart(df["saldo"])
else:
    st.write("Sin apuestas aún")

# =========================
# RANKING PRO
# =========================
st.subheader("🏆 Ranking inteligente")

ranking = []

for nombre, datos in jugadores.items():
    score = datos["elo"] + (datos["racha"] * 15)
    ranking.append({"Jugador": nombre, "Score": score})

df_rank = pd.DataFrame(ranking).sort_values(by="Score", ascending=False)

st.dataframe(df_rank)
