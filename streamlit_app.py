# =====================================
# 📊 DATOS DE JUGADORES (EJEMPLO REAL)
# =====================================
jugadores = {
    "Ondrej Fiklik": {"elo": 1590, "historial": ["W","W","L","W","W"]},
    "Miloslav Lubas": {"elo": 1540, "historial": ["L","W","L","W","L"]},
    "Petr David": {"elo": 1600, "historial": ["W","W","W","L","W"]},
    "Tomas Konecny": {"elo": 1620, "historial": ["W","L","W","W","W"]},
    "Jiri Martinko": {"elo": 1580, "historial": ["L","L","W","W","L"]}
}

# =====================================
# 🧠 1. FORMA PONDERADA (CLAVE)
# =====================================
def calcular_forma(historial):
    puntos = 0
    peso = 1

    # últimos partidos pesan más
    for resultado in reversed(historial):
        if resultado == "W":
            puntos += peso
        peso += 1

    return puntos


# =====================================
# 📈 2. PROBABILIDAD (ELO + FORMA)
# =====================================
def calcular_probabilidad(jugador_a, jugador_b):
    elo_a = jugadores[jugador_a]["elo"]
    elo_b = jugadores[jugador_b]["elo"]

    forma_a = calcular_forma(jugadores[jugador_a]["historial"])
    forma_b = calcular_forma(jugadores[jugador_b]["historial"])

    # probabilidad base ELO
    base = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

    # ajuste por forma
    ajuste = (forma_a - forma_b) * 0.02

    prob = base + ajuste

    # limitar entre 1% y 99%
    return max(0.01, min(0.99, prob))


# =====================================
# 💰 3. VALOR ESPERADO
# =====================================
def calcular_valor(probabilidad, cuota):
    return (probabilidad * cuota) - 1


# =====================================
# 💸 4. APUESTA (KELLY SIMPLIFICADO)
# =====================================
def calcular_apuesta(bankroll, probabilidad, cuota):
    valor = calcular_valor(probabilidad, cuota)

    if valor <= 0:
        return 0

    kelly = valor / (cuota - 1)
    return bankroll * kelly


# =====================================
# 🔍 5. ANÁLISIS COMPLETO
# =====================================
def analizar_partido(jugador_a, jugador_b, cuota, bankroll):

    prob = calcular_probabilidad(jugador_a, jugador_b)
    valor = calcular_valor(prob, cuota)
    apuesta = calcular_apuesta(bankroll, prob, cuota)

    print("=====================================")
    print(f"Partido: {jugador_a} vs {jugador_b}")
    print(f"Probabilidad: {prob*100:.2f}%")
    print(f"Valor esperado: {valor:.2f}")

    if valor > 0:
        print("✅ Apuesta con valor")
        print(f"Apuesta recomendada: ${apuesta:.2f}")
    else:
        print("❌ No apostar")

    print("=====================================")


# =====================================
# ▶️ EJEMPLO DE USO
# =====================================
analizar_partido(
    "Ondrej Fiklik",
    "Miloslav Lubas",
    cuota=2.0,
    bankroll=100
)
