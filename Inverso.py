import streamlit as st
import math

def decimales_a_gms(decimal):
    signo = -1 if decimal < 0 else 1
    decimal = abs(decimal)
    g = int(decimal)
    m = int((decimal - g) * 60)
    s = (decimal - g - m / 60) * 3600
    return signo * g, m, s

def obtener_parametros_datum(nombre):
    if nombre == 'Internacional':
        return 6378388, 1 / 297
    elif nombre == 'GRS 80':
        return 6378137, 1 / 298.257222101
    elif nombre == 'WGS84':
        return 6378137, 1 / 298.257223563
    else:
        return 6378137, 1 / 298.257223563

def obtener_cuadrante(X, Y):
    if X >= 0 and Y >= 0:
        return 1
    elif X < 0 and Y >= 0:
        return 2
    elif X < 0 and Y < 0:
        return 3
    elif X >= 0 and Y < 0:
        return 4

def inversas_interface():
    st.header("Coordenadas Geocéntricas Inversas (X, Y, Z → φ, λ, h)")
    st.markdown("---")

    datum = st.selectbox("Sistema de referencia (Datum):", ['Internacional', 'GRS 80', 'WGS84', 'Manual'])

    if datum == 'Manual':
        col1, col2 = st.columns(2)
        a_input = col1.text_input("Semieje mayor a (m):")
        f_input = col2.text_input("Achatamiento (1/f):")

        if not a_input.strip() or not f_input.strip():
            st.warning("Ingrese a y 1/f para usar el Datum Manual.")
            return

        try:
            a = float(a_input)
            f_inv = float(f_input)
            if f_inv == 0:
                st.error("El valor de 1/f no puede ser cero.")
                return
            f = 1 / f_inv
        except ValueError:
            st.error("Ingrese valores válidos para a y 1/f.")
            return
    else:
        a, f = obtener_parametros_datum(datum)

    e2 = 2 * f - f**2
    b = a * (1 - f)

    col1, col2, col3 = st.columns(3)
    x_input = col1.text_input("Coordenada X (m):")
    y_input = col2.text_input("Coordenada Y (m):")
    z_input = col3.text_input("Coordenada Z (m):")
    metodo = st.radio("Método de cálculo:", ["Iterativo", "Solución Exacta"])

    if st.button("Calcular"):
        try:
            X = float(x_input)
            Y = float(y_input)
            Z = float(z_input)

            p = math.sqrt(X**2 + Y**2)
            lon = math.atan2(Y, X)
            lon_deg = math.degrees(lon)
            lon_gms = decimales_a_gms(lon_deg)

            if metodo == "Iterativo":
                # Método clásico iterativo
                phi = math.atan2(Z, p * (1 - e2))
                for _ in range(5):
                    N = a / math.sqrt(1 - e2 * math.sin(phi)**2)
                    h = p / math.cos(phi) - N
                    phi = math.atan2(Z, p * (1 - e2 * N / (N + h)))

            else:
                # Método de solución exacta (Bowring / sin iterar)
                e2_p = (a**2 - b**2) / b**2
                theta = math.atan((Z * a) / (p * b))
                phi = math.atan((Z + e2_p * b * math.sin(theta)**3) / (p - e2 * a * math.cos(theta)**3))
                N = a / math.sqrt(1 - e2 * math.sin(phi)**2)
                h = p / math.cos(phi) - N

            phi_deg = math.degrees(phi)
            phi_gms = decimales_a_gms(phi_deg)
            cuadrante = obtener_cuadrante(X, Y)

            st.success("Cálculo completado:")
            st.code(
                f"φ = {phi_deg:.8f}° ({int(phi_gms[0])}° {int(phi_gms[1])}' {phi_gms[2]:.5f}\")\n"
                f"λ = {lon_deg:.8f}° ({int(lon_gms[0])}° {int(lon_gms[1])}' {lon_gms[2]:.5f}\")\n"
                f"h = {h:.8f} m\n"
                f"Cuadrante: {cuadrante}"
            )

        except Exception as e:
            st.error(f"Entrada inválida o incompleta: {e}")

