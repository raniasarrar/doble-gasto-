import streamlit as st

from nucleo.comun import (GENESIS, NOMBRE_VENTA, VENTAS, comprobar, configurar, corto, encadenar, evidencia,
                          exigir_nombre, nodos3, pie, respuesta)

configurar(3)
exigir_nombre()

st.markdown("**Qué vas a hacer.** Oleum Bética envía a la vez dos ventas del mismo lote: una por la "
            "pasarela de Europa y otra por la de Asia. Vas a ver qué anota cada nodo y si su cadena "
            "pasa la prueba de integridad del Tema 1.")
st.caption("Supuesto de clase: no forma parte del expediente del caso.")

st.markdown("#### 1 · Las dos ventas")
st.code(f"H · {VENTAS['H']}\nO · {VENTAS['O']}")

st.markdown("#### 2 · La red")
sep = st.slider("Milisegundos entre el envío de la venta H y el de la venta O", 0, 400,
                st.session_state.get("p3_sep", 30), step=10)
st.session_state.p3_sep = sep
st.caption("Cada venta tarda 20 ms en llegar al nodo cercano y 250 ms al nodo lejano. "
           "Quien envía decide la separación.")

cadenas = {}
cols = st.columns(2)
for col, (nodo, v) in zip(cols, nodos3(sep).items()):
    t, (primero, segundo) = v["t"], v["orden"]
    with col:
        st.markdown(f"**{nodo}**")
        st.markdown(f"Recibe H a los {t['H']} ms · O a los {t['O']} ms")
        st.markdown(f"1.º venta a **{NOMBRE_VENTA[primero]}** ✅ anotada  \n"
                    f"2.º venta a **{NOMBRE_VENTA[segundo]}** ❌ rechazada: doble venta")
        if t["H"] == t["O"]:
            st.caption("Empate: el programa desempata por la letra. También eso es una regla que alguien decidió.")
    cadenas[nodo] = encadenar([GENESIS, "E1 · " + VENTAS[primero]])

if len({c[-1]["texto"] for c in cadenas.values()}) == 1:
    st.info("Con esta separación los dos nodos ven lo mismo. Baja el deslizador: quien envía puede elegir.")
else:
    st.warning("Los dos nodos aplican bien la misma regla («la que cuenta es la primera») y anotan cosas distintas.")

st.markdown("#### 3 · La prueba del Tema 1")
alterar = st.checkbox("Para comparar: altera a mano el asiento E0 en la copia del nodo de Hamburgo")
revisar = {n: [dict(a) for a in c] for n, c in cadenas.items()}
if alterar:
    revisar["Nodo de Hamburgo"][0]["texto"] = GENESIS.replace("3.000", "2.500")
if st.button("Comprobar integridad de las dos cadenas", type="primary"):
    st.session_state.p3_ver = True
if st.session_state.get("p3_ver"):
    for nodo, cad in revisar.items():
        ok, roto = comprobar(cad)
        if ok:
            st.success(f"{nodo}: cadena **íntegra** ✓ · último resumen `{corto(cad[-1]['resumen'])}`")
        else:
            st.error(f"{nodo}: cadena **rota** en el asiento E{roto}. El resumen delata la alteración.")
    evidencia(3, {"sep": sep, "resumenes": {n: c[-1]["resumen"] for n, c in cadenas.items()}})
    with st.expander("Qué acabas de ver", expanded=True):
        st.markdown("Sin alterar nada, **las dos cadenas son íntegras** y terminan en resúmenes distintos. "
                    "El resumen delata que alguien cambió algo; aquí nadie cambió nada. "
                    "El doble gasto es un problema de **orden**, no de **integridad**.")
    st.caption("Para la entrega cuenta la última comprobación: déjala hecha con una separación en la que los nodos discrepen.")
    respuesta(3, "Las dos cadenas son íntegras. ¿Cuál es la verdadera? ¿Con qué criterio?")
pie()
