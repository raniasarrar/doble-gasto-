import streamlit as st
from cryptography.exceptions import InvalidSignature

from nucleo.comun import configurar, corto, evidencia, exigir_nombre, pie, respuesta, sha
from nucleo.verificacion import clave, publica_hex

configurar(2)
nombre = exigir_nombre()

ana = clave("Ana", nombre)
pub_ana = publica_hex(ana)
pub_bruno, pub_carla = publica_hex(clave("Bruno", nombre)), publica_hex(clave("Carla", nombre))
emision = sha(f"emision|moneda|{nombre}")

st.markdown("**Qué vas a hacer.** Eres Ana. Vas a transmitir la misma moneda dos veces con una firma "
            "digital real (Ed25519) y a comprobar qué dice la verificación.")

st.markdown("#### Los datos")
st.markdown(f"- Moneda: resultado de la transacción de emisión `{corto(emision)}`\n"
            f"- Clave pública de Ana: `{corto(pub_ana, 24)}`\n"
            f"- Clave pública de Bruno: `{corto(pub_bruno, 24)}` · de Carla: `{corto(pub_carla, 24)}`")
st.caption("Es la moneda de Nakamoto: cada transmisión firma el resumen de la transacción anterior "
           "y la clave pública del siguiente propietario.")

m_bruno = f"Transfiero la moneda (tx previa {emision[:16]}) a la clave {pub_bruno[:16]} · Bruno"
m_carla = f"Transfiero la moneda (tx previa {emision[:16]}) a la clave {pub_carla[:16]} · Carla"

st.markdown("#### 1 · Firma la transmisión a Bruno")
st.code(m_bruno)
if st.button("Firmar como Ana → Bruno", type="primary"):
    st.session_state.p2_fb = ana.sign(m_bruno.encode())
if "p2_fb" in st.session_state:
    st.caption("Firma (primeros caracteres)")
    st.code(corto(st.session_state.p2_fb.hex(), 40))

st.markdown("#### 2 · Firma ahora la transmisión de la misma moneda a Carla")
st.code(m_carla)
if st.button("Firmar como Ana → Carla", type="primary"):
    st.session_state.p2_fc = ana.sign(m_carla.encode())
if "p2_fc" in st.session_state:
    st.caption("Firma (primeros caracteres)")
    st.code(corto(st.session_state.p2_fc.hex(), 40))

if "p2_fb" in st.session_state and "p2_fc" in st.session_state:
    st.markdown("#### 3 · Verifica las dos con la clave pública de Ana")
    alterar = st.checkbox("Antes de verificar, cambia una letra del mensaje a Carla (para comparar)")
    if st.button("Verificar"):
        st.session_state.p2_ver = True
    if st.session_state.get("p2_ver"):
        pub = ana.public_key()
        validas = 0
        for quien, msg, firma in [("Bruno", m_bruno, st.session_state.p2_fb),
                                  ("Carla", m_carla.replace("Carla", "Carlo") if alterar else m_carla,
                                   st.session_state.p2_fc)]:
            try:
                pub.verify(firma, msg.encode())
                validas += 1
                st.success(f"Transmisión a {quien}: firma **válida**. La hizo Ana y el mensaje no ha cambiado.")
            except InvalidSignature:
                st.error(f"Transmisión a {quien}: firma **no válida**. El mensaje no es el que Ana firmó.")
        evidencia(2, {"pub": pub_ana, "m_bruno": m_bruno, "m_carla": m_carla,
                      "firma_b": st.session_state.p2_fb.hex(), "firma_c": st.session_state.p2_fc.hex()})

        with st.expander("Qué acabas de ver", expanded=True):
            st.markdown("Sin alterar nada, las **dos** transmisiones son válidas. La firma prueba **quién** quiso "
                        "transmitir y que el mensaje **no ha cambiado**. No prueba que Ana no hubiera transmitido "
                        "antes la misma moneda. Es el fragmento 2 de Nakamoto: *el beneficiario no puede "
                        "verificar que uno de los propietarios no haya gastado dos veces la moneda*.")
        respuesta(2, "¿Qué prueba cada firma? ¿Qué no prueba ninguna de las dos?")
pie()
