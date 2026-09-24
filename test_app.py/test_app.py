"""Recorre el laboratorio completo como lo haría un alumno y verifica la entrega. Uso: python test_app.py"""
from streamlit.testing.v1 import AppTest
from nucleo.comun import leer_entrega, texto_entrega
from nucleo.verificacion import comprobar_entrega

CLAVES = ["nombre", "respuestas", "evidencias", "p6", "ronda", "sep_guardada"]
estado = {"nombre": "Alumna Prueba", "respuestas": {}, "evidencias": {}, "p6": {}, "ronda": 1, "sep_guardada": 30}

def pagina(ruta):
    at = AppTest.from_file(ruta, default_timeout=30)
    for k, v in estado.items():
        at.session_state[k] = v
    return at.run()

def guardar(at):
    assert not at.exception, at.exception
    for k in CLAVES:
        estado[k] = at.session_state[k]

def contestar(at, texto):
    at.text_area(key=[t.key for t in at.text_area if t.key and t.key.startswith("resp_")][0]).input(texto).run()

at = AppTest.from_file("Inicio.py", default_timeout=30).run(); assert not at.exception, at.exception

at = pagina("pages/1_Paso_1_La_moneda_que_se_copia.py"); at.button[0].click().run(); at.button[1].click().run()
assert any("idénticos" in e.value for e in at.error); contestar(at, "No hay diferencia."); guardar(at)

at = pagina("pages/2_Paso_2_La_cadena_de_firmas.py"); at.button[0].click().run(); at.button[1].click().run(); at.button[2].click().run()
assert sum("válida**." in s.value for s in at.success) == 2; contestar(at, "Autoría, no orden."); guardar(at)

at = pagina("pages/3_Paso_3_Dos_nodos_dos_historias.py"); at.button[0].click().run()
assert sum("íntegra" in s.value for s in at.success) == 2; contestar(at, "Ninguna sin criterio."); guardar(at)

at = pagina("pages/4_Paso_4_La_doble_venta_del_lote.py"); at.selectbox[0].select("Oleum Bética").run(); at.button[1].click().run()
assert any("íntegra" in s.value for s in at.success); contestar(at, "El sesgo no se ve."); guardar(at)

at = pagina("pages/5_Paso_5_Votar_sin_arbitro.py"); at.slider[0].set_value(12).run(); contestar(at, "Nada."); guardar(at)

at = pagina("pages/6_Paso_6_Las_tres_condiciones.py")
at.checkbox(key="m_Registro de la Propiedad_0").check().run()
at.text_area(key="p6_final").input("Ninguno.").run()
for k, v in [("p6_g", "un orden"), ("p6_c", "un tercero"), ("p6_f", "la verdad")]:
    at.text_input(key=k).input(v).run()
assert not at.exception and len(at.get("download_button")) >= 1, "p6"
guardar(at)

d = {"version": "S5-AO1-v2", "nombre": estado["nombre"], "respuestas": estado["respuestas"],
     "evidencias": estado["evidencias"], "p6": estado["p6"], "ronda": estado["ronda"], "sep": estado["sep_guardada"]}
txt = texto_entrega(d)
datos, cod, err = leer_entrega(txt)
r = comprobar_entrega(datos, cod)
malos = [k for k, (ok, _) in r.items() if not ok]
assert not malos, r
# manipulación: cambiar una respuesta dentro del bloque
datos["respuestas"]["1"] = "Otra cosa"
assert not comprobar_entrega(datos, cod)["Código"][0]
# suplantación: mismo archivo con otro nombre
d2 = dict(d, nombre="Otra Persona"); from nucleo.comun import codigo
r2 = comprobar_entrega(d2, codigo(d2)); assert not r2["Paso 2"][0] and not r2["Paso 4"][0]
print("OK · entrega verificada · código", cod)
print(txt.split("-----")[0][-600:])
