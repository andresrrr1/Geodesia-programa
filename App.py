import streamlit as st
from Latitudes import latitudes_interface
from Directo import directas_interface
from Inverso import inversas_interface
from nivelacion import nivelacion_interface


# Título general del proyecto
st.set_page_config(page_title="Transformaciones Geodésicas", layout="centered")
st.title("Transformaciones Geodésicas")
st.markdown("---")

# Menú principal
opcion = st.sidebar.selectbox("Selecciona un módulo:", [
    "Inicio",
    "Latitudes Meridianas",
    "Coordenadas Geocéntricas Directas",
    "Coordenadas Geocéntricas Inversas",
    "Nivelación Geodésica"
])

# Navegación entre módulos
if opcion == "Inicio":
    st.subheader("Bienvenido al programa de transformaciones geodésicas")
    st.markdown("Selecciona un módulo en el menú lateral para comenzar.")

elif opcion == "Latitudes Meridianas":
    latitudes_interface()

elif opcion == "Coordenadas Geocéntricas Directas":
    directas_interface()

elif opcion == "Coordenadas Geocéntricas Inversas":
    inversas_interface()

elif opcion == "Nivelación Geodésica":
    nivelacion_interface()
