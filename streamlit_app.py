import streamlit as st

st.set_page_config(page_title="App PRO Apuestas")

st.title("💰 App PRO de Apuestas")

# =========================
# DATOS
# =========================
jugadores = {
    "Ondrej Fiklik": {"elo": 1590, "historial": ["W","W","L","W","W"]},
    "Miloslav Lubas": {"elo": 1540, "historial": ["L","W","L","W","L"]},
    "Petr David": {"elo": 1600, "historial": ["W","W","W","L","W"]},
    "Tomas Konecny": {"elo": 1620, "historial": ["W","L","W","W","W"]},
    "Jiri Martinko": {"elo": 1580, "historial": ["L","L","W","W","L"]}
}

# =========================
# FUNCIONES
# =========================
def calcular_forma(historial):
    puntos = 0
    peso = 1
    for r in reversed(historial):
        if r == "W":
            puntos += peso
        peso += 1
    return puntos

def calcular_probabilidad(a, b):
    elo_a = jugadores[a]["elo"]
    elo_b = jugadores[b]["elo"]

    forma_a = calcular_forma(jugadores[a]["historial"])
    forma_b = calcular_forma(jugadores[b]["historial"])

    base = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
    ajuste = (forma_a - forma_b) * 0.02

    return max(0.01, min(0.99, base + ajuste))

def calcular_valor(prob, cuota):
    return (prob * cuota) - 1

def calcular_apuesta(bankroll, prob, cuota):
    valor = calcular_valor(prob, cuota)
    if valor <= 0:
        return 0
    kelly = valor / (cuota - 1)
    return bankroll * kelly

# =========================
# UI
# =========================
jugador_a = st.selectbox("Jugador A", list(jugadores.keys()))
jugador_b = st.selectbox("Jugador B", list(jugadores.keys()))

cuota = st.number_input("Cuota", value=2.0)
bankroll = st.number_input("Bankroll", value=100.0)

if st.button("Analizar"):
    prob = calcular_probabilidad(jugador_a, jugador_b)
    valor = calcular_valor(prob, cuota)
    apuesta = calcular_apuesta(bankroll, prob, cuota)

    st.subheader("Resultado")

    st.write(f"Probabilidad: {prob*100:.2f}%")
    st.write(f"Valor esperado: {valor:.2f}")

    if valor > 0:
        st.success("Apuesta con valor ✅")
        st.write(f"Apuesta recomendada: ${apuesta:.2f}")
    else:
        st.error("No apostar ❌")
