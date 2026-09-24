import streamlit as st

from nucleo.comun import configurar, corto, evidencia, exigir_nombre, pie, respuesta, sha

configurar(1)
nombre = exigir_nombre()

st.markdown("**Qué vas a hacer.** Crear una moneda digital, enviarla y comprobar qué conservas tú "
            "y qué recibe quien la cobra.")

st.markdown("#### 1 · Escribe tu moneda")
moneda = st.text_input("Tu moneda es este texto:", value=f"Moneda n.º 1 de {nombre}")
st.caption("Una moneda digital no es más que esto: unos datos. Aquí, una frase.")

st.markdown("#### 2 · Envíala a Bruno")
if st.button("Enviar a Bruno", type="primary"):
    st.session_state.p1_enviada = moneda
    evidencia(1, {"moneda": moneda, "resumen": sha(moneda)})
enviada = st.session_state.get("p1_enviada")

if enviada:
    st.markdown("#### 3 · Compara lo que tiene cada uno")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Lo que conservas tú**")
        st.code(moneda)
        st.caption("Resumen SHA-256")
        st.code(corto(sha(moneda), 32))
    with c2:
        st.markdown("**Lo que ha recibido Bruno**")
        st.code(enviada)
        st.caption("Resumen SHA-256")
        st.code(corto(sha(enviada), 32))

    if moneda == enviada:
        st.error("Los dos resúmenes son idénticos. No hay original y copia: hay dos monedas iguales, "
                 "y tú sigues teniendo la tuya.")
    else:
        st.warning("Has cambiado tu texto después de enviarlo: pulsa otra vez «Enviar a Bruno» para ver el caso limpio.")

    st.markdown("#### 4 · ¿Y si ahora pagas a Carla?")
    if st.button("Enviar la misma moneda a Carla"):
        st.session_state.p1_carla = moneda
    if st.session_state.get("p1_carla"):
        iguales = len({sha(moneda), sha(enviada), sha(st.session_state.p1_carla)}) == 1
        st.error("Tres personas tienen ahora la misma moneda, bit a bit. " +
                 ("Los tres resúmenes coinciden." if iguales else ""))

    with st.expander("Qué acabas de ver", expanded=True):
        st.markdown("Con una botella, **entregar excluye**: si se la das a Bruno, tú ya no la tienes. "
                    "Con un fichero, **enviar no desposee**. Eso es el doble gasto: gastar dos veces la "
                    "misma unidad de valor digital porque entregarla no te la quita. "
                    "En la capa normativa tiene un nombre viejo: **doble venta** (art. 1473 CC).")

    respuesta(1, "¿Hay alguna diferencia entre la original y la copia? ¿Quién es el dueño de la moneda?")

pie()
