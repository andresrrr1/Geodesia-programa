import streamlit as st
import math

def gms_a_decimales(g, m, s):
    signo = -1 if g < 0 else 1
    return signo * (abs(g) + m / 60 + s / 3600)

def decimales_a_gms(decimal):
    signo = -1 if decimal < 0 else 1
    decimal = abs(decimal)
    g = int(decimal)
    m = int((decimal - g) * 60)
    s = (decimal - g - m / 60) * 3600
    return signo * g, m, s

def directas_interface():
    st.header("Coordenadas Geocéntricas Directas (φ, λ, h → X, Y, Z )")
    st.markdown("---")

    # DATUM
    datum = st.selectbox("Sistema de referencia (Datum):", ['Internacional', 'GRS 80', 'WGS84', 'Manual'])

    if datum == 'Manual':
        col1, col2 = st.columns(2)
        a_input = col1.text_input("Semieje mayor a (m):")
        f_input = col2.text_input("Achatamiento (1/f):")
        if not a_input.strip() or not f_input.strip():
            st.warning("Ingrese ambos valores para a y 1/f.")
            return
        try:
            a = float(a_input)
            f_inv = float(f_input)
            if f_inv == 0:
                st.error("El valor de 1/f no puede ser cero.")
                return
            f = 1 / f_inv
        except ValueError:
            st.error("Valores inválidos para a o 1/f.")
            return
    else:
        a, f = obtener_parametros_datum(datum)

    b = a * (1 - f)
    e2 = 2 * f - f**2

    # ENTRADA DE φ y λ
    formato = st.radio("Formato de entrada:", ['GMS', 'Decimal'])

    col1, col2 = st.columns(2)
    direccion_phi = col1.radio("Dirección latitud:", ['Norte (N)', 'Sur (S)'])
    direccion_lon = col2.radio("Dirección longitud:", ['Este (E)', 'Oeste (W)'])
    signo_phi = 1 if direccion_phi.startswith('N') else -1
    signo_lon = 1 if direccion_lon.startswith('E') else -1

    if formato == 'Decimal':
        phi_dec = st.text_input("Latitud φ (decimal):")
        lon_dec = st.text_input("Longitud λ (decimal):")
        try:
            phi = signo_phi * float(phi_dec)
            lon = signo_lon * float(lon_dec)
        except:
            st.error("Entradas inválidas.")
            return
    else:
        st.markdown("### Latitud φ (GMS)")
        col1, col2, col3 = st.columns(3)
        g_phi = col1.text_input("Grados φ:")
        m_phi = col2.text_input("Minutos φ:")
        s_phi = col3.text_input("Segundos φ:")

        st.markdown("### Longitud λ (GMS)")
        col4, col5, col6 = st.columns(3)
        g_lon = col4.text_input("Grados λ:")
        m_lon = col5.text_input("Minutos λ:")
        s_lon = col6.text_input("Segundos λ:")

        try:
            phi = signo_phi * gms_a_decimales(int(g_phi), int(m_phi), float(s_phi))
            lon = signo_lon * gms_a_decimales(int(g_lon), int(m_lon), float(s_lon))
        except:
            st.error("Valores GMS inválidos.")
            return

    # ALTURA
    h_input = st.text_input("Altura elipsoidal h (m):")
    try:
        h = float(h_input)
    except:
        st.error("Ingrese una altura válida.")
        return

    # BOTÓN CALCULAR
    if st.button("Calcular"):
        phi_rad = math.radians(phi)
        lon_rad = math.radians(lon)
        N = a / math.sqrt(1 - e2 * math.sin(phi_rad)**2)

        X = (N + h) * math.cos(phi_rad) * math.cos(lon_rad)
        Y = (N + h) * math.cos(phi_rad) * math.sin(lon_rad)
        Z = (N * (1 - e2) + h) * math.sin(phi_rad)

        theta = math.atan((b / a) * math.tan(phi_rad))
        omega = math.atan(math.tan(phi_rad) * (1 - e2))

        phi_deg = math.degrees(phi_rad)
        theta_deg = math.degrees(theta)
        omega_deg = math.degrees(omega)

        phi_gms = decimales_a_gms(phi_deg)
        theta_gms = decimales_a_gms(theta_deg)
        omega_gms = decimales_a_gms(omega_deg)

        st.success("Cálculo completado:")
        st.code(
            f"φ = {phi_deg:.8f}°  ({int(phi_gms[0])}° {int(phi_gms[1])}' {phi_gms[2]:.4f}\")\n"
            f"θ = {theta_deg:.8f}°  ({int(theta_gms[0])}° {int(theta_gms[1])}' {theta_gms[2]:.4f}\")\n"
            f"ω = {omega_deg:.8f}°  ({int(omega_gms[0])}° {int(omega_gms[1])}' {omega_gms[2]:.4f}\")\n\n"
            f"X = {X:.8f} m\nY = {Y:.8f} m\nZ = {Z:.8f} m\nN = {N:.8f} m"
        )

def obtener_parametros_datum(nombre):
    if nombre == 'Internacional':
        return 6378388, 1 / 297
    elif nombre == 'GRS 80':
        return 6378137, 1 / 298.257222101
    elif nombre == 'WGS84':
        return 6378137, 1 / 298.257223563
    else:
        return 6378137, 1 / 298.257223563
