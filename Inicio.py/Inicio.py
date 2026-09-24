import json

import streamlit as st

from nucleo.comun import PASOS, cargar_progreso, configurar, pie

nombre = configurar()

st.caption("Blockchain: Fundamentos Técnicos y Problemática Jurídica · Grado en Derecho · UNIE · 2026-27")
st.title("Laboratorio S5 · El doble gasto")
st.markdown("**Laboratorio de clase** · Tema 2 · Sesión 5 · jueves 24 de septiembre de 2026 · no se califica")

st.info("**Pregunta viva del Tema 2.** ¿Se puede fabricar acuerdo entre desconocidos que pueden "
        "mentir, sin que nadie arbitre?")

if not nombre:
    st.warning("👈 Escribe tu nombre y apellido en la barra lateral. En el móvil, ábrela con el botón › de arriba a la izquierda.")
else:
    st.success(f"Hola, {nombre}. Sigue los pasos cuando aparezcan en pantalla.")

st.markdown("### Cómo funciona")
st.markdown(
    "- Seis pasos, uno por bloque de la clase. Cada paso se abre cuando su diapositiva "
    "*LABORATORIO · PASO n* aparece en el proyector.\n"
    "- En cada paso: haz el ejercicio, **pulsa el botón de comprobación** y contesta la pregunta.\n"
    "- El paso 6 se termina en casa y te deja descargar tus respuestas para estudiar. No se entrega ni se califica.\n"
    "- Tus datos viven en esta pestaña. **Descarga tu progreso** (barra lateral) antes de cerrarla.")

st.markdown("### Los seis pasos")
st.table({"Paso": [f"{n}" for n in PASOS], "Página": [PASOS[n][0] for n in PASOS],
          "Minutos de clase": [PASOS[n][1] for n in PASOS]})

st.markdown("### ¿Cerraste la pestaña? Recupera tu progreso")
arch = st.file_uploader("Sube el archivo progreso_S5_….json que descargaste", type=["json"])
if arch is not None and not st.session_state.get("recuperado") == arch.name:
    try:
        cargar_progreso(json.load(arch))
        st.session_state.recuperado = arch.name
        st.success("Progreso recuperado. Sigue donde lo dejaste.")
        st.rerun()
    except Exception:
        st.error("Ese archivo no es un progreso del laboratorio. Sube el .json que descargaste de la barra lateral.")
pie()
