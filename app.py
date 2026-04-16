import streamlit as st

st.set_page_config(page_title="App de Apuestas", layout="centered")

st.title("💰 App de Apuestas")

# Jugadores
jugadores = ["Jugador A", "Jugador B", "Jugador C"]

jugador_a = st.selectbox("Jugador A", jugadores)
jugador_b = st.selectbox("Jugador B", jugadores)

cuota = st.number_input("Cuota", value=2.0)
bankroll = st.number_input("Bankroll", value=100.0)

if st.button("Analizar"):
    if jugador_a == jugador_b:
        st.warning("Selecciona jugadores diferentes")
    else:
        probabilidad = 1 / cuota
        apuesta = bankroll * 0.05

        st.success(f"Probabilidad implícita: {probabilidad:.2%}")
        st.info(f"Apuesta recomendada: ${apuesta:.2f}")
