"""Piezas comunes del laboratorio de clase de la sesión 5 (sin calificación).

Punto único de sincronización con la presentación y con el caso:
- PASOS: título, página y minutos de cada paso (coinciden con las diapositivas LABORATORIO · PASO n).
- CONSORCIO: los diez miembros de TrazaOliva (nueve escriben; el Consejo Regulador conserva copia).
- LOTE y VENTAS: el supuesto de clase de la doble venta.

Ningún resumen SHA-256 ni ninguna firma está escrito en el código: todo se calcula al ejecutar.
"""
import datetime
import hashlib
import json
import random

import streamlit as st

VERSION = "S5-AO1-v2"

PASOS = {
    1: ("La moneda que se copia", "21–27", "El doble gasto es un problema viejo"),
    2: ("La cadena de firmas", "40–47", "Cómo lo plantea Nakamoto"),
    3: ("Dos nodos, dos historias", "57–63", "Integridad no es orden"),
    4: ("La doble venta del lote", "66–73", "Llamar a un árbitro"),
    5: ("Votar sin árbitro", "80–84", "Tres cosas a la vez"),
    6: ("Las tres condiciones", "en casa", "Cierre"),
}

CONSORCIO = [
    "Oleum Bética", "Almazara A", "Almazara B", "Almazara C", "Almazara D", "Almazara E",
    "Laboratorio", "Transportista 1", "Transportista 2", "Consejo Regulador DOP",
]

LOTE = "AOVE-2026-0148"
GENESIS = f"E0 · Lote {LOTE} · 3.000 botellas envasadas el 18-10-2026 · anota Oleum Bética"
VENTAS = {
    "H": f"Lote {LOTE} vendido al distribuidor de Hamburgo · firma Oleum Bética",
    "O": f"Lote {LOTE} vendido al distribuidor de Osaka · firma Oleum Bética",
}
NOMBRE_VENTA = {"H": "Hamburgo", "O": "Osaka"}

INICIO_BLOQUE = "----- DATOS VERIFICABLES (no editar) -----"
FIN_BLOQUE = "----- FIN DE LOS DATOS -----"


def sha(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def corto(h: str, n: int = 16) -> str:
    return h[:n] + "…"


# ---------------------------------------------------------------- estado
def _estado():
    ss = st.session_state
    ss.setdefault("nombre", "")
    ss.setdefault("respuestas", {})
    ss.setdefault("evidencias", {})
    ss.setdefault("p6", {})
    ss.setdefault("ronda", 1)
    ss.setdefault("sep_guardada", 30)


def configurar(paso: int | None = None):
    """Cabecera común: título, nombre del alumno y enlace con la diapositiva."""
    titulo = "Laboratorio S5 · El doble gasto" if paso is None else f"Paso {paso} · {PASOS[paso][0]}"
    st.set_page_config(page_title=titulo, page_icon="🔗", layout="centered")
    _estado()
    with st.sidebar:
        st.markdown("**Tu nombre**")
        nuevo = st.text_input("Nombre y apellido", value=st.session_state.nombre,
                              label_visibility="collapsed", placeholder="Escribe tu nombre")
        if nuevo.strip() != st.session_state.nombre:
            st.session_state.nombre = nuevo.strip()
        st.caption("Nombre y apellido, escritos siempre igual. De él dependen tus datos.")
    if paso is not None:
        t, mins, bloque = PASOS[paso]
        st.caption(f"Laboratorio de clase · Diapositiva **LABORATORIO · PASO {paso}** · min {mins} · {bloque}")
        st.title(f"Paso {paso} · {t}")
    return st.session_state.nombre


def exigir_nombre():
    if not st.session_state.get("nombre"):
        st.warning("Escribe tu nombre y apellido en la barra lateral para empezar "
                   "(en el móvil: botón › arriba a la izquierda).")
        st.stop()
    return st.session_state.nombre


def progreso() -> dict:
    ss = st.session_state
    return {"version": VERSION, "nombre": ss.nombre, "respuestas": ss.respuestas,
            "evidencias": ss.evidencias, "p6": ss.p6, "ronda": ss.ronda, "sep": ss.sep_guardada}


def cargar_progreso(d: dict):
    ss = st.session_state
    ss.nombre = d.get("nombre", "")
    ss.respuestas = {str(k): v for k, v in d.get("respuestas", {}).items()}
    ss.evidencias = {str(k): v for k, v in d.get("evidencias", {}).items()}
    ss.p6 = d.get("p6", {})
    ss.ronda = int(d.get("ronda", 1))
    ss.sep_guardada = int(d.get("sep", 30))


def pie():
    """Al final de cada página: botón para guardar el progreso (incluye lo hecho en esta página)."""
    if not st.session_state.get("nombre"):
        return
    with st.sidebar:
        st.divider()
        st.markdown("**Guardar mi progreso**")
        st.download_button("Descargar progreso (.json)", json.dumps(progreso(), ensure_ascii=False, indent=1),
                           file_name=f"progreso_S5_{st.session_state.nombre.replace(' ', '_')}.json",
                           mime="application/json", use_container_width=True)
        st.caption("Si cierras la pestaña, lo recuperas en la portada subiendo este archivo.")


def evidencia(paso: int, datos: dict):
    st.session_state.evidencias[str(paso)] = datos


def respuesta(paso: int, pregunta: str):
    """Caja de respuesta breve que se guarda para la entrega."""
    st.markdown(f"#### ✍️ Para contestar\n{pregunta}")
    previa = st.session_state.respuestas.get(str(paso), "")
    txt = st.text_area("Tu respuesta, en dos a cuatro líneas", value=previa, key=f"resp_{paso}", height=110)
    if txt != previa:
        st.session_state.respuestas[str(paso)] = txt
    if txt.strip():
        st.caption("Guardada en esta pestaña. La recoges en el paso 6.")


# ---------------------------------------------------------------- mecánica
def rng(*partes) -> random.Random:
    semilla = sha("|".join(str(p) for p in partes))
    return random.Random(int(semilla[:16], 16))


def encadenar(asientos: list[str]) -> list[dict]:
    """Cadena mínima del Tema 1: cada asiento lleva el resumen del anterior."""
    cadena, previo = [], "0" * 64
    for texto in asientos:
        h = sha(previo + texto)
        cadena.append({"texto": texto, "previo": previo, "resumen": h})
        previo = h
    return cadena


def comprobar(cadena: list[dict]) -> tuple[bool, int | None]:
    """Recalcula todos los resúmenes. Devuelve (íntegra, primer eslabón roto)."""
    previo = "0" * 64
    for i, a in enumerate(cadena):
        if a["previo"] != previo or sha(previo + a["texto"]) != a["resumen"]:
            return False, i
        previo = a["resumen"]
    return True, None


def nodos3(sep: int) -> dict:
    """Paso 3: tiempos de llegada a los dos nodos y venta que anota cada uno."""
    t = {"Nodo de Hamburgo": {"H": 20, "O": sep + 250}, "Nodo de Osaka": {"H": 250, "O": sep + 20}}
    return {n: {"t": v, "orden": sorted(["H", "O"], key=lambda k: (v[k], k))} for n, v in t.items()}


def llegadas(nombre: str, ronda: int, separacion_ms: int) -> list[dict]:
    """Cuándo recibe cada miembro las dos ventas (reproducible por nombre y ronda)."""
    r = rng("red", nombre, ronda)
    filas = []
    for m in CONSORCIO:
        lat_h = r.randint(15, 260)
        lat_o = r.randint(15, 260)
        th, to = lat_h, separacion_ms + lat_o
        if m == "Oleum Bética":  # quien emite conoce las dos al instante
            th, to = 0, separacion_ms
        primero = "H" if (th, "H") < (to, "O") else "O"
        filas.append({"miembro": m, "t_H": th, "t_O": to, "primero": primero})
    return filas


def votos(nombre: str, ronda: int, sep: int) -> dict:
    f = llegadas(nombre, ronda, sep)
    return {"H": sum(x["primero"] == "H" for x in f), "O": sum(x["primero"] == "O" for x in f)}


# ---------------------------------------------------------------- entrega
def canon(d: dict) -> str:
    return json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def codigo(datos: dict) -> str:
    return sha(canon(datos))[:16].upper()


def texto_entrega(datos: dict) -> str:
    cod = codigo(datos)
    p6 = datos["p6"]
    lin = [
        "LABORATORIO DE CLASE · SESIÓN 5 · «EL DOBLE GASTO»",
        "Blockchain: Fundamentos Técnicos y Problemática Jurídica · UNIE · 2026-27",
        f"Alumno/a: {datos['nombre']}",
        f"Código: {cod}",
        f"Generado: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}",
        "",
    ]
    for p in range(1, 6):
        lin += [f"PASO {p} · {PASOS[p][0]}", datos["respuestas"].get(str(p), "(sin respuesta)").strip(), ""]
    lin += ["PASO 6 · Condiciones marcadas"]
    for s, v in p6.get("matriz", {}).items():
        lin.append(f"- {s}: " + (", ".join(v) if v else "ninguna"))
    lin += ["", f"¿Algún sistema cumple las tres? {p6.get('final', '')}", "",
            f"Mecanismo: {p6.get('mecanismo', '')}", f"Qué garantiza: {p6.get('g', '')}",
            f"A costa de qué: {p6.get('c', '')}", f"Qué deja fuera: {p6.get('f', '')}", "",
            f"Nota sobre uso de IA: {p6.get('ia', '') or '(no declarada)'}", "",
            INICIO_BLOQUE, canon(datos), FIN_BLOQUE, ""]
    return "\n".join(lin)


def leer_entrega(texto: str) -> tuple[dict | None, str | None, str]:
    """Devuelve (datos, código declarado, error)."""
    try:
        bloque = texto.split(INICIO_BLOQUE, 1)[1].split(FIN_BLOQUE, 1)[0].strip()
        datos = json.loads(bloque)
    except Exception:
        return None, None, "No se encuentra el bloque de datos verificables."
    declarado = None
    for l in texto.splitlines():
        if l.startswith("Código:"):
            declarado = l.split(":", 1)[1].strip()
            break
    return datos, declarado, ""
