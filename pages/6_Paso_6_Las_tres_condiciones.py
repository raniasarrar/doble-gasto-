import streamlit as st

from nucleo.comun import PASOS, configurar, exigir_nombre, pie, progreso, texto_entrega

configurar(6)
nombre = exigir_nombre()
p6 = st.session_state.p6

st.markdown("**Qué vas a hacer.** Aplicar las tres condiciones a cuatro sistemas y cerrar con el formato de "
            "siempre. Esta página no corrige: lo comentamos el lunes en clase.")

SISTEMAS = ["Registro de la Propiedad", "Un banco", "TrazaOliva con árbitro designado", "Red abierta que vota por nodos"]
CONDS = ["Publicidad", "Acuerdo", "Sin árbitro"]
AYUDA = ["Todos ven todas las transacciones", "Una única historia del orden",
         "Nadie decide por los demás, aunque algunos mientan"]


def campo(clave, etiqueta, area=False):
    f = st.text_area if area else st.text_input
    val = f(etiqueta, value=p6.get(clave, ""), key=f"p6_{clave}", **({"height": 110} if area else {}))
    p6[clave] = val
    return val


st.markdown("#### 1 · ¿Qué condiciones cumple cada sistema?")
p6.setdefault("matriz", {})
for s in SISTEMAS:
    st.markdown(f"**{s}**")
    cols = st.columns(3)
    marcadas = []
    for i, c in enumerate(CONDS):
        if cols[i].checkbox(c, value=c in p6["matriz"].get(s, []), key=f"m_{s}_{i}", help=AYUDA[i]):
            marcadas.append(c)
    p6["matriz"][s] = marcadas
campo("final", "¿Algún sistema cumple las tres condiciones a la vez? Justifícalo en dos a cuatro líneas.", area=True)

st.markdown("#### 2 · Qué garantiza / a costa de qué / qué deja fuera")
opciones = ["La firma digital", "El encadenamiento por resúmenes", "El árbitro designado", "La votación por nodos"]
p6["mecanismo"] = st.selectbox("Elige un mecanismo de la sesión", opciones,
                               index=opciones.index(p6.get("mecanismo", opciones[0])))
campo("g", "Qué garantiza")
campo("c", "A costa de qué")
campo("f", "Qué deja fuera")

st.markdown("#### 3 · Tus respuestas de la sesión")
d = progreso()
faltan = []
for p in range(1, 6):
    txt = d["respuestas"].get(str(p), "").strip()
    ev = str(p) in d["evidencias"]
    if not txt or not ev:
        faltan.append(p)
    estado = ("✅" if txt and ev else "⚠️") + (" " if txt else " sin respuesta ·") + ("" if ev else " sin completar el ejercicio")
    st.markdown(f"- **Paso {p} · {PASOS[p][0]}** {estado}  \n  {txt if txt else ''}")
if faltan:
    st.info("Pasos sin completar: " + ", ".join(map(str, faltan)) + ". Si cerraste la pestaña, recupera tu progreso en la portada.")

st.markdown("#### 4 · Guarda tus respuestas")
if not all(str(p6.get(k, "")).strip() for k in ["final", "g", "c", "f"]):
    st.info("Completa la pregunta del apartado 1 y las tres líneas del apartado 2.")
else:
    st.download_button("Descargar mis respuestas (.txt)", texto_entrega(d), type="primary",
                       file_name=f"S5_doble_gasto_{nombre.replace(' ', '_')}.txt", mime="text/plain")
    st.caption("Para tu cuaderno. No se entrega ni se califica. Tráelo pensado el lunes: la sesión 6 empieza donde acaba este paso.")
pie()
