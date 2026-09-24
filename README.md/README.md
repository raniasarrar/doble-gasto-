# Laboratorio S5 · El doble gasto

**Laboratorio de clase, sin calificación.** La actividad evaluable del momento es la Entrega 1 (Tema 1).

**Blockchain: Fundamentos Técnicos y Problemática Jurídica** · Grado en Derecho · UNIE · 2026-27
Tema 2 · Sesión 5 · jueves 24 de septiembre de 2026 · Prof. Dr. D. José Fernández Tamames

Práctica en el navegador que acompaña a la presentación `Sesion5_El_doble_gasto.pptx`. Cada paso se abre
cuando su diapositiva **LABORATORIO · PASO n** aparece en el proyector. Sin cuenta y sin instalación para
el alumnado.

## Correspondencia con la presentación

| Paso | Página | Minutos | Bloque de la sesión | Qué hace el alumno |
|---|---|---|---|---|
| 1 | La moneda que se copia | 21–27 | El doble gasto es un problema viejo | Envía una «moneda» y comprueba que el resumen de lo enviado y lo conservado es idéntico |
| 2 | La cadena de firmas | 40–47 | Cómo lo plantea Nakamoto | Firma con Ed25519 dos transmisiones de la misma moneda y verifica que las dos son válidas |
| 3 | Dos nodos, dos historias | 57–63 | **Integridad no es orden** | Mueve la separación entre envíos y comprueba que dos cadenas incompatibles son ambas íntegras |
| 4 | La doble venta del lote | 66–73 | Llamar a un árbitro | Ve qué venta recibe primero cada miembro de TrazaOliva, designa árbitro, prueba con Oleum Bética |
| 5 | Votar sin árbitro | 80–84 | Tres cosas a la vez | Fabrica identidades gratuitas hasta cambiar el resultado de la votación |
| 6 | Las tres condiciones | en casa | Cierre | Matriz, pregunta final, línea «garantiza / a costa de / deja fuera» y descarga de sus respuestas para estudiar |

## Reglas de diseño

- **Ningún resumen SHA-256 ni ninguna firma está escrito en el código**: todo se calcula en ejecución.
- **Ninguna página da la solución**: dan el instrumento y una pregunta breve.
- Los datos dependen del **nombre del alumno** (latencias, claves): distintos para cada uno y reproducibles.
- El .txt del paso 6 lleva un bloque de datos verificables y un código. No se usa ahora; queda preparado por si el laboratorio se integra más adelante en la Entrega 2 (el módulo `nucleo/verificacion.py` rehace cada ejercicio a partir del nombre).
- **Progreso:** la barra lateral de cada página descarga un .json con todo lo hecho; la portada lo recupera.
- Punto único de sincronización con el caso: `nucleo/comun.py` (`CONSORCIO`, `LOTE`, `VENTAS`, `PASOS`).
  Si los nombres de los miembros del consorcio del laboratorio anterior (`blockchain-laboratorio`) son
  otros, basta con cambiar la lista `CONSORCIO`.
- La doble venta del lote AOVE-2026-0148 es un **supuesto de clase**, no un hecho del expediente.

## Publicar (una vez, unos cinco minutos)

1. Crear en GitHub un repositorio **público** vacío, por ejemplo `jftmames/laboratorio-doble-gasto`.
2. Subir el contenido de esta carpeta:
   ```bash
   cd laboratorio-doble-gasto
   git init && git add . && git commit -m "Laboratorio S5 · El doble gasto"
   git branch -M main
   git remote add origin https://github.com/jftmames/laboratorio-doble-gasto.git
   git push -u origin main
   ```
   (Sin terminal: en la página del repositorio, *Add file → Upload files* y arrastrar la carpeta.)
3. En <https://share.streamlit.io>: *Create app* → el repositorio → rama `main` → archivo `Inicio.py` → *Deploy*.
4. Pegar la dirección resultante en el aula virtual con el rótulo **«Laboratorio S5 · Doble gasto»**
   (es el que cita la diapositiva 3).

**Aviso operativo:** las aplicaciones gratuitas se duermen sin uso y tardan unos treinta segundos en
despertar. Abrirla dos minutos antes de clase.

## Probar en local

```bash
pip install -r requirements.txt
streamlit run Inicio.py
python test_app.py      # recorre el laboratorio completo como un alumno y verifica sus datos
```
