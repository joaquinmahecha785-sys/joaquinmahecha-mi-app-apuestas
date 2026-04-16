import streamlit as st
import json
import os

st.set_page_config(page_title="App PRO de Apuestas", layout="centered")

st.title("💰 App PRO de Apuestas")

# =====================================
# 📁 Cargar o crear archivo jugadores.json
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
# ➕ Agregar nuevo jugador
# =====================================
st.subheader("➕ Agregar jugador")

nuevo_nombre = st.text_input("Nombre del jugador")

if st.button("Agregar jugador"):
    if nuevo_nombre and nuevo_nombre not in jugadores:
        jugadores[nuevo_nombre] = {
            "elo": 1500,
            "historial": []
        }
        with open("jugadores.json", "w") as f:
            json.dump(jugadores, f, indent=4)
        st.success(f"{nuevo_nombre} agregado")
    else:
        st.warning("Nombre inválido o ya existe")

# =====================================
# 📊 Selección de jugadores
# =====================================
st.subheader("⚔️ Partido")

lista_jugadores = list(jugadores.keys())

jugador_a = st.selectbox("Jugador A", lista_jugadores)
jugador_b = st.selectbox("Jugador B", lista_jugadores)

cuota = st.number_input("Cuota", value=2.0)
bankroll = st.number_input("Bankroll", value=100.0)

# =====================================
# 📈 Mostrar forma reciente
# =====================================
def mostrar_forma(nombre):
    if nombre not in jugadores:
        st.warning(f"No hay datos para {nombre}")
        return

    historial = jugadores[nombre].get("historial", [])

    st.write(f"Forma de {nombre}:")

    if not historial:
        st.info("Sin historial aún")
        return

    for r in historial[-5:]:
        if r == "W":
            st.success("✅ Victoria")
        else:
            st.error("❌ Derrota")

# Mostrar forma
st.subheader("📊 Forma reciente")
mostrar_forma(jugador_a)
mostrar_forma(jugador_b)

# =====================================
# 🧠 Cálculo simple (puedes mejorar luego)
# =====================================
def calcular_probabilidad(a, b):
    elo_a = jugadores[a]["elo"]
    elo_b = jugadores[b]["elo"]

    prob = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
    return prob

# =====================================
# 🎯 Análisis
# =====================================
if st.button("Analizar"):
    prob = calcular_probabilidad(jugador_a, jugador_b)

    valor_esperado = (prob * cuota) - 1
    apuesta = bankroll * (valor_esperado / cuota) if valor_esperado > 0 else 0

    st.subheader("Resultado")
    st.write(f"Probabilidad de ganar: {round(prob*100,2)}%")
    st.write(f"Valor esperado: {round(valor_esperado,2)}")

    if valor_esperado > 0:
        st.success("✅ Apuesta con valor")
        st.write(f"Apuesta recomendada: ${round(apuesta,2)}")
    else:
        st.error("❌ No apostar")

# =====================================
# ➕ Agregar resultado (mejora PRO)
# =====================================
st.subheader("📌 Registrar resultado")

resultado_jugador = st.selectbox("Jugador", lista_jugadores)
resultado = st.selectbox("Resultado", ["W", "L"])

if st.button("Guardar resultado"):
    jugadores[resultado_jugador]["historial"].append(resultado)

    # Limitar a últimos 10
    jugadores[resultado_jugador]["historial"] = jugadores[resultado_jugador]["historial"][-10:]

    with open("jugadores.json", "w") as f:
        json.dump(jugadores, f, indent=4)

    st.success("Resultado guardado")
