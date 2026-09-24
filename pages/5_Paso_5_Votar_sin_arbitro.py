import time

import streamlit as st
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from nucleo.comun import NOMBRE_VENTA, configurar, evidencia, exigir_nombre, pie, respuesta, votos

configurar(5)
nombre = exigir_nombre()
ronda, sep = st.session_state.ronda, st.session_state.sep_guardada

st.markdown("**Qué vas a hacer.** Sin árbitro, votan los miembros: gana la venta que la mayoría vio "
            "primero. Después vas a fabricar identidades nuevas y ver cuánto cuesta cambiar el resultado.")

v = votos(nombre, ronda, sep)
st.markdown("#### 1 · La votación honesta")
st.caption(f"Mismos datos que en el paso 4 (ronda {ronda}, separación {sep} ms).")
ganadora = "H" if v["H"] >= v["O"] else "O"
st.markdown(f"Hamburgo **{v['H']}** · Osaka **{v['O']}** → gana **{NOMBRE_VENTA[ganadora]}**")

st.markdown("#### 2 · Fabrica identidades")
favor = st.radio("¿Qué venta quieres que gane?", ["Hamburgo", "Osaka"],
                 index=1 if ganadora == "H" else 0, horizontal=True)
k = "H" if favor == "Hamburgo" else "O"
otro = "O" if k == "H" else "H"
n = st.slider("Identidades nuevas que votan lo que tú digas", 0, 40, 0)

t0 = time.perf_counter()
for _ in range(n):
    Ed25519PrivateKey.generate()
coste_ms = (time.perf_counter() - t0) * 1000

final = dict(v)
final[k] += n
st.bar_chart({"Votos": {"Hamburgo": final["H"], "Osaka": final["O"]}})
necesarias = max(0, v[otro] - v[k] + 1)
st.markdown(f"Para que gane **{favor}** hacen falta **{necesarias}** identidades nuevas.")
if n:
    st.markdown(f"Fabricar {n} identidades (un par de claves cada una) ha costado **{coste_ms:.2f} ms** de cálculo. "
                "Ningún papel, ninguna autorización, ningún euro.")
    evidencia(5, {"ronda": ronda, "sep": sep, "favor": k, "n": n, "necesarias": necesarias,
                  "ms": round(coste_ms, 2)})
if final[k] > final[otro]:
    st.error(f"Gana {favor}. Lo has decidido tú, no la red.")

with st.expander("Qué acabas de ver", expanded=bool(n)):
    st.markdown("En una red abierta, un nodo es un programa que cualquiera arranca: **una identidad que no "
                "cuesta nada no puede votar**. En TrazaOliva esto no pasa porque el consorcio controla quién "
                "entra, pero entonces vuelve a haber alguien que admite: otro tercero. "
                "El lunes, la salida de Nakamoto: hacer que votar **cueste**.")
respuesta(5, "¿Cuánto te ha costado cada identidad falsa? ¿Qué haría falta para que votar tuviera un precio?")
pie()
