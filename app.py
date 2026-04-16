import streamlit as st

st.set_page_config(page_title="App de Apuestas")

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
        probabilidad = 0.55
        prob_casa = 1 / cuota

        st.write(f"Probabilidad modelo: {probabilidad:.2f}")
        st.write(f"Probabilidad casa: {prob_casa:.2f}")

        if probabilidad > prob_casa:
            st.success("✅ APOSTAR")
        else:
            st.error("❌ No hay valor")
