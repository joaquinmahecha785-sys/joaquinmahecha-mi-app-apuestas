import streamlit as st
import json
import os

st.set_page_config(page_title="App PRO de Apuestas", layout="centered")

st.title("💰 App PRO de Apuestas")

# =====================================
# 📁 Cargar o crear JSON
# =====================================
if not os.path.exists("jugadores.json"):
    jugadores = {
        "Jugador A": {"elo": 1500, "historial": ["W", "L", "W"]},
        "Jugador B": {"elo": 1450, "historial": ["L", "L", "W"]}
    }
    with open("jugadores.json", "w") as f:
        json.dump(jugadores, f, indent=4)
else:
    with open("jugadores.json", "r") as f:
        jugadores = json.load(f)

# =====================================
# 🛠️ ARREGLAR DATOS AUTOMÁTICAMENTE
# =====================================
for nombre in jugadores:
    if "historial" not in jugadores[nombre] or not isinstance(jugadores[nombre]["historial"], list):
        jugadores[nombre]["historial"] = []
    if "elo" not in jugadores[nombre]:
        jugadores[nombre]["elo"] = 1500

# =====================================
# 📊 FUNCIONES PRO
# =====================================
def calcular_winrate(historial):
    if not historial or not isinstance(historial, list):
        return 0
    return historial.count("W") / len(historial)

def calcular_probabilidad(a, b):
    elo_a = jugadores[a]["elo"]
    elo_b = jugadores[b]["elo"]

    base = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

    forma_a = calcular_winrate(jugadores[a].get("historial", [])[-5:])
    forma_b = calcular_winrate(jugadores[b].get("historial", [])[-5:])

    ajuste = (forma_a - forma_b) * 0.2

    return max(0.01, min(0.99, base + ajuste))

# =====================================
# ➕ AGREGAR JUGADOR
# =====================================
st.subheader("➕ Agregar jugador")

nuevo = st.text_input("Nombre")

if st.button("Agregar"):
    if nuevo and nuevo not in jugadores:
        jugadores[nuevo] = {"elo": 1500, "historial": []}
        with open("jugadores.json", "w") as f:
            json.dump(jugadores, f, indent=4)
        st.success("Jugador agregado")
    else:
        st.warning("Nombre inválido o repetido")

# =====================================
# 🏆 RANKING (CORREGIDO)
# =====================================
st.subheader("🏆 Ranking")

ranking = sorted(
    jugadores.items(),
    key=lambda x: calcular_winrate(x[1].get("historial", [])),
    reverse=True
)

for i, (nombre, data) in enumerate(ranking[:5], start=1):
    winrate = calcular_winrate(data.get("historial", []))
    st.write(f"{i}. {nombre} - {round(winrate*100,1)}%")

# =====================================
# ⚔️ PARTIDO
# =====================================
st.subheader("⚔️ Analizar partido")

lista = list(jugadores.keys())

jugador_a = st.selectbox("Jugador A", lista)
jugador_b = st.selectbox("Jugador B", lista)

cuota = st.number_input("Cuota", value=2.0)
bankroll = st.number_input("Bankroll", value=100.0)

# =====================================
# 📈 FORMA
# =====================================
def mostrar_forma(nombre):
    historial = jugadores.get(nombre, {}).get("historial", [])

    st.write(f"Forma de {nombre}")

    if not historial:
        st.info("Sin datos")
        return

    valores = [1 if x == "W" else 0 for x in historial[-10:]]

    st.line_chart(valores)

    winrate = calcular_winrate(historial)
    st.write(f"Winrate: {round(winrate*100,2)}%")

st.subheader("📊 Forma reciente")
mostrar_forma(jugador_a)
mostrar_forma(jugador_b)

# =====================================
# 🎯 ANÁLISIS
# =====================================
if st.button("Analizar"):
    prob = calcular_probabilidad(jugador_a, jugador_b)

    valor = (prob * cuota) - 1
    apuesta = bankroll * valor if valor > 0 else 0

    st.subheader("Resultado")
    st.write(f"Probabilidad: {round(prob*100,2)}%")
    st.write(f"Valor esperado: {round(valor,2)}")

    if valor > 0:
        st.success("✅ Apuesta con valor")
        st.write(f"Apuesta recomendada: ${round(apuesta,2)}")
    else:
        st.error("❌ No apostar")

# =====================================
# 📌 REGISTRAR RESULTADO
# =====================================
st.subheader("📌 Registrar resultado")

jugador_res = st.selectbox("Jugador", lista)
resultado = st.selectbox("Resultado", ["W", "L"])

if st.button("Guardar resultado"):
    jugadores[jugador_res]["historial"].append(resultado)

    jugadores[jugador_res]["historial"] = jugadores[jugador_res]["historial"][-20:]

    with open("jugadores.json", "w") as f:
        json.dump(jugadores, f, indent=4)

    st.success("Guardado correctamente")
