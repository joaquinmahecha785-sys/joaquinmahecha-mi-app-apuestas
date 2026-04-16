import streamlit as st

st.title("💰 App de Apuestas")

jugadores = ["Jugador A", "Jugador B"]

jugador_a = st.selectbox("Jugador A", jugadores)
jugador_b = st.selectbox("Jugador B", jugadores)

cuota = st.number_input("Cuota", min_value=1.0, value=2.0)
bankroll = st.number_input("Bankroll", min_value=1.0, value=100.0)

if st.button("Analizar"):
    prob = 0.55
    prob_casa = 1 / cuota

    st.write(f"Probabilidad modelo: {prob}")
    st.write(f"Probabilidad casa: {prob_casa}")

    if prob > prob_casa:
        st.success("✅ APOSTAR")
    else:
        st.error("❌ No hay valor")
