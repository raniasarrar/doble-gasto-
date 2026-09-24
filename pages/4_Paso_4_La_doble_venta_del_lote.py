import streamlit as st

from nucleo.comun import (CONSORCIO, GENESIS, NOMBRE_VENTA, VENTAS, comprobar, configurar, corto, encadenar,
                          evidencia, exigir_nombre, llegadas, pie, respuesta, votos)

configurar(4)
nombre = exigir_nombre()

st.markdown("**Qué vas a hacer.** Ahora son los diez miembros de TrazaOliva. Verás qué venta recibe "
            "primero cada uno, y después designarás un árbitro que ordene por todos.")

st.markdown("#### 1 · Qué ve primero cada miembro")
c1, c2 = st.columns([3, 1])
with c1:
    sep = st.slider("Milisegundos entre los dos envíos de Oleum Bética", 0, 300,
                    st.session_state.sep_guardada, step=10)
    st.session_state.sep_guardada = sep
with c2:
    st.write("")
    if st.button("Otra ronda"):
        st.session_state.ronda += 1
ronda = st.session_state.ronda
st.caption(f"Ronda {ronda}. Las latencias dependen de tu nombre y de la ronda.")

filas = llegadas(nombre, ronda, sep)
st.dataframe([{"Miembro": f["miembro"], "Recibe Hamburgo (ms)": f["t_H"], "Recibe Osaka (ms)": f["t_O"],
               "Ve primero": NOMBRE_VENTA[f["primero"]]} for f in filas], hide_index=True, width="stretch")
v = votos(nombre, ronda, sep)
m1, m2 = st.columns(2)
m1.metric("Anotan Hamburgo", v["H"])
m2.metric("Anotan Osaka", v["O"])
if v["H"] and v["O"]:
    st.warning("El consorcio no tiene una historia: tiene dos.")
else:
    st.info("Esta vez todos ven lo mismo. Prueba otra ronda o baja la separación.")

st.markdown("#### 2 · Designa un árbitro")
arbitro = st.selectbox("Quién ordena por todos", ["— nadie —"] + CONSORCIO)
if arbitro != "— nadie —":
    elegida = next(f for f in filas if f["miembro"] == arbitro)["primero"]
    if arbitro == "Oleum Bética":
        st.markdown("Oleum Bética es **parte interesada**: recibió las dos al instante y puede elegir.")
        pref = st.radio("Oleum Bética prefiere que conste la venta a…", ["Hamburgo", "Osaka"], horizontal=True)
        elegida = "H" if pref == "Hamburgo" else "O"
    st.success(f"Los diez adoptan el orden de **{arbitro}**: primera venta, **{NOMBRE_VENTA[elegida]}**. "
               "Una sola historia, al instante.")

    st.markdown("#### 3 · ¿Lo detecta la cadena?")
    cadena = encadenar([GENESIS, "E1 · " + VENTAS[elegida]])
    if st.button("Comprobar integridad de la cadena del consorcio", type="primary"):
        st.session_state.p4_ver = True
    if st.session_state.get("p4_ver"):
        ok, _ = comprobar(cadena)
        st.success(f"Cadena **íntegra** ✓ · último resumen `{corto(cadena[-1]['resumen'])}`" if ok else "Cadena rota.")
        evidencia(4, {"ronda": ronda, "sep": sep, "arbitro": arbitro, "elegida": elegida,
                      "resumen": cadena[-1]["resumen"], "votos": v})
        with st.expander("Qué acabas de ver", expanded=True):
            st.markdown("El árbitro resuelve el orden **por autoridad**, como el Registro o la casa de moneda. "
                        "Su precio: hay que pagarle y creerle. Si el árbitro ordena a su favor, la cadena "
                        "queda igual de íntegra: **el control técnico no ve el sesgo de quien ordena**.")
        st.caption("Para la entrega cuenta la última comprobación. Recomendado: déjala hecha con Oleum Bética como árbitro.")
        respuesta(4, "¿Qué cambia cuando el árbitro es parte interesada? ¿Lo detecta la cadena?")
pie()
