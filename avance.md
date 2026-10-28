# Avance — Identidad visual KIPP (v1.1)

**Estado:** COMPLETADO — listo para publicar
**Objetivo:** aplicar la personalidad visual de KIPP (Interstellar) a toda la interfaz web.
**Alcance:** solo interfaz. Sin cambios de voz/microcopy. Sin estilo `kipp_monolito` para PPTX.
**Acento:** azul reactor `#7FD4E8`.
**Base:** commit `bf75156` (v1.0).

## Checklist

- [x] Registro de avance creado
- [x] `.streamlit/config.toml` con tema oscuro
- [x] Favicon monolito en `assets/kipp_icon.png`
- [x] CSS y cabecera monolito en `app.py`
- [x] Pruebas (17) + compilación + dependencias
- [x] Documentación actualizada (README, CONFIGURACION)
- [x] Versión v1.1
- [ ] Commit y push a GitHub

## Cambios aplicados

- `set_page_config`: favicon PNG del monolito, sin emoji.
- Tema oscuro completo: fondo `#0A0B0D`, paneles `#121417`, línea `#262A2F`, texto `#E8EAED`, acento `#7FD4E8`.
- Cabecera degradada reemplazada por monolito de cuatro placas y hairline inferior.
- Tipografía: Inter para contenido, JetBrains Mono para etiquetas y estados, con fallback local.
- Pestañas, métricas, botones, alertas, expansores, inputs, sidebar y galería rediseñados.
- Alertas: fondo de panel y borde izquierdo semántico (acento, verde, ámbar, rojo).
- Botones: rectangulares, mono en mayúsculas; primario en acento con texto oscuro.
- Galería: overlay con nombre de archivo (no ruta completa) y borde de acento al pasar el cursor.
- Textos y microcopy intactos. Lógica y PPTX sin tocar.

## Verificación visual

Capturas revisadas en Chrome a 1440 px con las tres pestañas y la galería sembrada temporalmente:

- Interfaz principal con sidebar abierto: correcta.
- Convertir PPTX a PDF: correcta.
- Curador con dos imágenes y tooltip: correcto.
- Estilos calculados: alerta `#121417`, botón primario `#7FD4E8` con texto `#06090B`, títulos en peso 300.
- Datos temporales de la galería restaurados: `index.json` vuelve a `[]` y las imágenes de prueba se eliminaron.

## Pruebas

- `python -m unittest discover -s tests`: 17 pruebas OK (exit 0).
- `py_compile` de `app.py`, `maestro.py`, `generar_desde_md.py`, `motor/*.py` y `tests/*.py`: OK.
- `pip check`: sin dependencias rotas.

## Bitácora

- **Inicio:** repositorio limpio en `bf75156`.
- **Tema:** creados `.streamlit/config.toml` y `assets/kipp_icon.png` (651 bytes).
- **Interfaz:** CSS y cabecera monolito aplicados en `app.py`.
- **Correcciones tras revisión:** alertas, contraste de botones, peso de títulos, marcos sobrantes de Streamlit, salto de etiquetas y ruta en el tooltip.
- **Documentación:** README y CONFIGURACION actualizados; versión v1.1.
- **Publicación:** pendiente de commit y push.
