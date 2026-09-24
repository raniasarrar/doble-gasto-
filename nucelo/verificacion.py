"""Comprobaciones de una entrega: se recalcula todo a partir del nombre y de los parámetros guardados."""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .comun import GENESIS, VENTAS, codigo, encadenar, nodos3, sha, votos


def clave(persona: str, nombre: str) -> Ed25519PrivateKey:
    # Clave reproducible: la misma para el mismo alumno. Solo para el aula.
    return Ed25519PrivateKey.from_private_bytes(bytes.fromhex(sha(f"clave|{persona}|{nombre}")))


def publica_hex(priv: Ed25519PrivateKey) -> str:
    return priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()


def cadena3(sep: int) -> dict:
    return {n: encadenar([GENESIS, "E1 · " + VENTAS[v["orden"][0]]])[-1]["resumen"] for n, v in nodos3(sep).items()}


def comprobar_entrega(d: dict, declarado: str | None) -> dict:
    """Devuelve {clave: (ok, detalle)} para cada comprobación."""
    nombre = d.get("nombre", "")
    ev = d.get("evidencias", {})
    r = {}
    rec = codigo(d)
    r["Código"] = (declarado == rec, f"declarado {declarado} · recalculado {rec}")

    e = ev.get("1")
    r["Paso 1"] = (bool(e) and sha(e["moneda"]) == e["resumen"], "moneda y resumen coherentes" if e else "sin evidencia")

    e = ev.get("2")
    if e:
        ok = publica_hex(clave("Ana", nombre)) == e["pub"]
        try:
            pub = clave("Ana", nombre).public_key()
            pub.verify(bytes.fromhex(e["firma_b"]), e["m_bruno"].encode())
            pub.verify(bytes.fromhex(e["firma_c"]), e["m_carla"].encode())
        except (InvalidSignature, ValueError, KeyError):
            ok = False
        r["Paso 2"] = (ok, "dos firmas de Ana verificadas con su clave" if ok else "firmas o clave no coinciden con el nombre")
    else:
        r["Paso 2"] = (False, "sin evidencia")

    e = ev.get("3")
    if e:
        ok = cadena3(int(e["sep"])) == e["resumenes"]
        dist = len(set(e["resumenes"].values())) == 2
        r["Paso 3"] = (ok, f"separación {e['sep']} ms · " + ("dos historias distintas" if dist else "misma historia en ambos nodos"))
    else:
        r["Paso 3"] = (False, "sin evidencia")

    e = ev.get("4")
    if e:
        ok = encadenar([GENESIS, "E1 · " + VENTAS[e["elegida"]]])[-1]["resumen"] == e["resumen"]
        v = votos(nombre, int(e["ronda"]), int(e["sep"]))
        ok = ok and v == e["votos"]
        r["Paso 4"] = (ok, f"ronda {e['ronda']} · árbitro {e['arbitro']} · votos H {v['H']} / O {v['O']}")
    else:
        r["Paso 4"] = (False, "sin evidencia")

    e = ev.get("5")
    if e:
        v = votos(nombre, int(e["ronda"]), int(e["sep"]))
        otro = "O" if e["favor"] == "H" else "H"
        nec = max(0, v[otro] - v[e["favor"]] + 1)
        ok = nec == e["necesarias"] and int(e["n"]) > 0
        r["Paso 5"] = (ok, f"hacían falta {nec} · fabricó {e['n']}")
    else:
        r["Paso 5"] = (False, "sin evidencia")

    p6 = d.get("p6", {})
    campos = ["final", "g", "c", "f"]
    r["Paso 6"] = (all(str(p6.get(k, "")).strip() for k in campos), "matriz, pregunta final y línea g/c/f")
    n_resp = sum(bool(str(d.get("respuestas", {}).get(str(p), "")).strip()) for p in range(1, 6))
    r["Respuestas 1-5"] = (n_resp == 5, f"{n_resp} de 5")
    return r
