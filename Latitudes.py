import math
import streamlit as st
def gms_a_decimales(grados, minutos, segundos):
    signo = -1 if grados < 0 else 1
    return signo * (abs(grados) + minutos / 60 + segundos / 3600)

def decimales_a_gms(decimal):
    signo = -1 if decimal < 0 else 1
    decimal = abs(decimal)
    g = int(decimal)
    m = int((decimal - g) * 60)
    s = (decimal - g - m / 60) * 3600
    return signo * g, m, s

def calcular_latitudes(valor, tipo, a, b, e2):
    def decimales_a_gms_local(decimal):
        signo = -1 if decimal < 0 else 1
        decimal = abs(decimal)
        g = int(decimal)
        m = int((decimal - g) * 60)
        s = (decimal - g - m / 60) * 3600
        return signo * g, m, s

    if tipo == 'phi':
        phi = math.radians(valor)
        N = a / math.sqrt(1 - e2 * math.sin(phi)**2)
        X = N * math.cos(phi)
        Z = N * (1 - e2) * math.sin(phi)
        omega = math.atan2(Z, X)
        theta = math.atan((b / a) * math.tan(phi))
    elif tipo == 'theta':
        theta = math.radians(valor)
        phi = math.atan((a / b) * math.tan(theta))
        omega = math.atan(math.tan(phi) * (1 - e2))
        X = a * math.cos(theta)
        Z = b * math.sin(theta)
        N = a / math.sqrt(1 - e2 * math.sin(phi)**2)
    elif tipo == 'omega':
        omega = math.radians(valor)
        phi = math.atan(math.tan(omega) / (1 - e2))
        theta = math.atan((b / a) * math.tan(phi))
        N = a / math.sqrt(1 - e2 * math.sin(phi)**2)
        X1 = N * math.cos(phi)
        Z1 = N * (1 - e2) * math.sin(phi)
        Rg = (a * math.sqrt(1 - e2)) / math.sqrt(1 - e2 * math.cos(omega)**2)
        X2 = Rg * math.cos(omega)
        Z2 = Rg * math.sin(omega)
        diff_X = abs(X1 - X2)
        diff_Z = abs(Z1 - Z2)
        alerta = "\n⚠️ ¡Atención! Los métodos difieren significativamente." if diff_X > 1 or diff_Z > 1 else "\n✅ Métodos consistentes."

        phi_deg = math.degrees(phi)
        theta_deg = math.degrees(theta)
        omega_deg = math.degrees(omega)

        phi_gms = decimales_a_gms_local(phi_deg)
        theta_gms = decimales_a_gms_local(theta_deg)
        omega_gms = decimales_a_gms_local(omega_deg)

        return (
            f"φ: {phi_deg:.7f}°  ({int(phi_gms[0])}° {int(phi_gms[1])}' {phi_gms[2]:.4f}\")\n"
            f"θ: {theta_deg:.7f}°  ({int(theta_gms[0])}° {int(theta_gms[1])}' {theta_gms[2]:.4f}\")\n"
            f"ω: {omega_deg:.7f}°  ({int(omega_gms[0])}° {int(omega_gms[1])}' {omega_gms[2]:.4f}\")\n\n"
            f"Método 1 (desde φ):\nX1 = {X1:.4f} m\nZ1 = {Z1:.4f} m\n"
            f"Método 2 (usando Rg):\nX2 = {X2:.4f} m\nZ2 = {Z2:.4f} m\nRg = {Rg:.4f} m\nN = {N:.4f} m{alerta}"
        )
    else:
        return "Tipo no válido."

    phi_deg = math.degrees(phi)
    theta_deg = math.degrees(theta)
    omega_deg = math.degrees(omega)

    phi_gms = decimales_a_gms_local(phi_deg)
    theta_gms = decimales_a_gms_local(theta_deg)
    omega_gms = decimales_a_gms_local(omega_deg)

    return (
        f"φ = {phi_deg:.8f}°  ({int(phi_gms[0])}° {int(phi_gms[1])}' {phi_gms[2]:.8f}\")\n"
        f"θ = {theta_deg:.8f}°  ({int(theta_gms[0])}° {int(theta_gms[1])}' {theta_gms[2]:.8f}\")\n"
        f"ω = {omega_deg:.8f}°  ({int(omega_gms[0])}° {int(omega_gms[1])}' {omega_gms[2]:.8f}\")\n"
        f"X = {X:.10f} m\nZ = {Z:.10f} m\nN = {N:.4f} m"
    )

def latitudes_interface():
    st.header("Latitudes Meridianas (φ, θ, ω)")
    st.markdown("---")

    datum = st.selectbox("Sistema de referencia (Datum):", ['Internacional', 'GRS 80', 'WGS84', 'Manual'])

    if datum == 'Manual':
        col1, col2 = st.columns(2)
        a_input = col1.text_input("Semieje mayor a (m):", value="")
        f_input = col2.text_input("Achatamiento (1/f):", value="")

        if not a_input.strip() or not f_input.strip():
            st.warning("Por favor ingrese el valor de a y 1/f.")
            return

        try:
            a = float(a_input)
            f_inv = float(f_input)
            if f_inv == 0:
                st.error("El valor de 1/f no puede ser cero.")
                return
            f = 1 / f_inv
        except ValueError:
            st.error("Debe ingresar valores numéricos válidos para a y 1/f.")
            return
    else:
        valores = {
            'Internacional': (6378388, 1 / 297),
            'GRS 80': (6378137, 1 / 298.257222101),
            'WGS84': (6378137, 1 / 298.257223563)
        }
        a, f = valores[datum]

    b = a * (1 - f)
    e2 = 2 * f - f ** 2

    tipo = st.selectbox("Tipo de latitud:", ['Geodésica (φ)', 'Paramétrica (θ)', 'Geocéntrica (ω)'])
    formato = st.radio("Formato de entrada:", ['GMS', 'Decimal'])
    direccion = st.radio("Dirección:", ['Norte (N)', 'Sur (S)'])
    signo = 1 if direccion == 'Norte (N)' else -1

    if formato == 'GMS':
        col1, col2, col3 = st.columns(3)
        grados_input = col1.text_input("Grados:")
        minutos_input = col2.text_input("Minutos:")
        segundos_input = col3.text_input("Segundos:")

        try:
            grados = float(grados_input) if grados_input.strip() else 0.0
            minutos = float(minutos_input) if minutos_input.strip() else 0.0
            segundos = float(segundos_input) if segundos_input.strip() else 0.0
            valor = signo * gms_a_decimales(grados, minutos, segundos)
        except ValueError:
            st.error("Debe ingresar valores numéricos válidos.")
            return
    else:
        decimal_input = st.text_input("Latitud decimal:")
        try:
            valor = signo * float(decimal_input) if decimal_input.strip() else 0.0
        except ValueError:
            st.error("Debe ingresar un valor decimal válido.")
            return

    if st.button("Calcular") and valor is not None:
        tipo_map = {'Geodésica (φ)': 'phi', 'Paramétrica (θ)': 'theta', 'Geocéntrica (ω)': 'omega'}
        resultado = calcular_latitudes(valor, tipo_map[tipo], a, b, e2)
        st.success("Resultado:")
        st.code(resultado)
