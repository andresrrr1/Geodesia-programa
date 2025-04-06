import streamlit as st
import pandas as pd

def nivelacion_interface():
    st.header("🟦 Nivelación Geodésica - Subes y Bajas")
    st.markdown("Este módulo permite calcular cotas a partir de V+ y V− para cada estación.")

    # Paso 1: Número de estaciones
    num_estaciones = st.number_input("🔢 Número de estaciones:", min_value=1, max_value=50, step=1)

    if "datos_nivelacion" not in st.session_state:
        st.session_state.datos_nivelacion = []

    # Generar espacio para ingresar datos (lo haremos en la siguiente parte)
    if num_estaciones > 0:
        st.markdown("### 📝 Ingreso de datos por estación")

        columnas = ["Estación", "Punto Visado", "V+", "V−"]
        st.columns(len(columnas))  # for layout spacing

        # Mostrar encabezado
        col_encabezado = st.columns(len(columnas))
        for j, col_name in enumerate(columnas):
            col_encabezado[j].markdown(f"**{col_name}**")

        datos = []

        for i in range(num_estaciones):
            cols = st.columns(len(columnas))
            fila = []
            for j in range(len(columnas)):
                valor = cols[j].text_input(label="", key=f"{columnas[j]}_{i}")
                fila.append(valor)
            datos.append(fila)

        st.session_state.datos_nivelacion = datos

        st.markdown("---")
        cota_inicial = st.number_input("📏 Cota inicial conocida (m):", step=0.001, format="%.3f")

        if st.button("🔍 Calcular cotas"):
            datos = st.session_state.datos_nivelacion
            resultados = []

            cotas = []
            hi_actual = None
            cota_actual = cota_inicial
            cotas.append(cota_actual)

            for i, fila in enumerate(datos):
                est, pv, vp_raw, vm_raw = fila

                try:
                    vp = float(vp_raw) if vp_raw.strip() else 0.0
                except:
                    vp = 0.0

                try:
                    vm = float(vm_raw) if vm_raw.strip() else 0.0
                except:
                    vm = 0.0

                # Calcular HI como antes
                hi = ""
                if vp_raw.strip() and vm_raw.strip():
                    hi_actual = hi_actual + vp - vm if hi_actual is not None else cota_actual + vp - vm
                    hi = hi_actual
                elif vp_raw.strip():
                    hi_actual = cota_actual + vp
                    hi = hi_actual

                # Calcular COTA con la lógica de tu imagen
                if i == 0:
                    cota = cota_actual  # primera cota es la que se ingresó
                else:
                    try:
                        vp_prev = float(datos[i - 1][2]) if datos[i - 1][2].strip() else 0.0
                    except:
                        vp_prev = 0.0
                    cota = cotas[-1] + vp_prev - vm

                sube = max(0, cota - cotas[-1])
                baja = max(0, cotas[-1] - cota)
                cotas.append(cota)

                resultados.append([est, pv, vp, vm, hi, cota, sube, baja])

            df_resultado = pd.DataFrame(resultados, columns=["Estación", "Punto Visado", "V+", "V−", "HI", "Cota", "Sube", "Baja"])
            st.markdown("### 📋 Resultados:")
            st.dataframe(df_resultado, use_container_width=True)

            st.session_state.df_resultado = df_resultado



