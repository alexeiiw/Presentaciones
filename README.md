# Presentaciones

Generador de presentaciones academicas de alto impacto usando Python, Streamlit, python-pptx, biblioteca local de imagenes, Pexels y Pixabay.

Version actual: `v0.9`

## Estructura del proyecto

```text
Presentaciones/
├── maestro.py                 # Entrada recomendada para abrir la interfaz web
├── app.py                     # Interfaz Streamlit
├── generar_desde_md.py        # Entrada para generar desde terminal
├── motor/                     # Modulos internos del generador
├── ejemplos/                  # Markdown de referencia
├── assets/                    # Assets locales
├── biblioteca_imagenes/       # Biblioteca e indice local ignorado
├── salidas/                   # PPTX y PDF generados, ignorados por Git
└── temp/                      # Archivos temporales, ignorados por Git
```

La raiz conserva solo los puntos de entrada y la documentacion principal. La logica interna vive en `motor/`.

## Instalacion en GitHub Codespaces

```bash
pip install -r requirements.txt
```

Para exportar tambien a PDF sin PowerPoint, instala LibreOffice en el Codespace:

```bash
sudo apt-get update
sudo apt-get install -y libreoffice
libreoffice --version
```

La generacion de PPTX no requiere LibreOffice. LibreOffice solo se usa cuando se pide crear PDF.

## Configuracion de Pexels

La aplicacion lee las claves desde variables de entorno.

Crea un archivo `.env` en la raiz del proyecto, basado en `.env.example`:

```bash
PEXELS_API_KEY=tu_clave
PIXABAY_API_KEY=tu_clave
```

En Codespaces tambien puedes exportarla antes de ejecutar la app:

```bash
export PEXELS_API_KEY="tu_clave"
export PIXABAY_API_KEY="tu_clave"
```

Tambien puedes pegar las claves directamente en la barra lateral de la interfaz web.

Mas detalle en `CONFIGURACION.md`.

## Ejecutar interfaz web

```bash
streamlit run app.py
```

Tambien puedes iniciar la interfaz desde el script maestro:

```bash
python maestro.py
```

`maestro.py` es el punto de entrada recomendado para abrir la pagina web. Los modulos internos del generador se encuentran en `motor/`; `app.py` y `generar_desde_md.py` se conservan como puntos de entrada visibles.

## Generar desde terminal

```bash
python generar_desde_md.py ejemplos/redes_computadoras.md --salida salidas/redes_computadoras.pptx --estilo tecnologico_oscuro
```

Para generar PPTX y luego PDF desde terminal:

```bash
python generar_desde_md.py ejemplos/redes_computadoras.md --salida salidas/redes_computadoras.pptx --estilo tecnologico_oscuro --pdf
```

## Uso

- Pega el Markdown de la clase.
- Define `Agenda:`, `Contenido Presentacion:`, `Aprendizajes:` y `Frase Final:` si quieres usar la estructura academica completa.
- Selecciona estilo visual.
- Selecciona modo de imagen.
- Selecciona distribucion de diapositivas.
- Genera y descarga primero el archivo `.pptx`.
- Si necesitas PDF, usa la opcion `Generar PDF desde este PPTX` despues de crear la presentacion.
- Los archivos quedan guardados dentro de `salidas/`.
- Los `.pptx` y `.pdf` generados en `salidas/` estan excluidos de Git por defecto.

## Imagenes Locales

Puedes subir imagenes al Codespace dentro de `assets/` y usarlas directamente desde el Markdown.

Para presentaciones UMG, la recomendacion operativa es usar `images.jpg` como imagen institucional a color y `Umg.png` como logo institucional en blanco y negro o version alternativa segun convenga al estilo visual. La seleccion y curacion final de imagenes queda a criterio del docente.

Ejemplo para la portada:

```markdown
Imagen Portada: assets/images.jpg
Logo Portada: assets/Umg.png
```

Tambien puedes indicar solo el nombre si la imagen esta dentro de `assets/`:

```markdown
Imagen Portada: images.jpg
Logo Portada: Umg.png
```

La imagen local de portada tiene prioridad aunque el modo de imagen seleccionado sea `sin_imagen` o `solo_diseno`.

Ejemplo para una diapositiva:

```markdown
Imagen: assets/diagrama_usb.png
```

Formatos soportados: `.jpg`, `.jpeg`, `.png`, `.webp` y `.bmp`. Los archivos dentro de `assets/` son locales y no se suben al repo por defecto.

## Modos de imagen

- `biblioteca_pexels_pixabay`: busca primero en biblioteca local, luego Pexels y luego Pixabay.
- `biblioteca_pexels`: busca primero en biblioteca local y luego Pexels.
- `pexels_pixabay`: busca en Pexels y luego Pixabay sin consultar biblioteca local.
- `pexels_o_diseno`: intenta Pexels y si falla crea diseno visual.
- `pexels`: intenta Pexels y si falla deja el area sin imagen.
- `pixabay`: intenta Pixabay y si falla crea diseno visual.
- `solo_biblioteca`: usa solo imagenes locales guardadas.
- `solo_diseno`: no usa API, crea diseno visual.
- `sin_imagen`: genera solo contenido textual.

## Biblioteca de imagenes

Las imagenes descargadas se guardan localmente en `biblioteca_imagenes/imagenes/` y se registran en `biblioteca_imagenes/index.json` para reutilizarlas en futuras presentaciones.

Por defecto, las imagenes descargadas y `biblioteca_imagenes/index.json` no se suben a GitHub para evitar que el repositorio crezca demasiado y para que el indice local no genere cambios pendientes constantes.

El archivo `biblioteca_imagenes/index.example.json` muestra la estructura esperada del indice.

Desde la pestaña `Curador de imagenes` puedes marcar cada imagen como `favorita`, `aprobada`, `pendiente` o `rechazada`. El curador muestra primero las pendientes y permite filtrar por estado. El generador prioriza favoritas y aprobadas, y excluye rechazadas.

## Distribuciones

- `alternada`: cambia imagen derecha/izquierda de forma ordenada.
- `fija`: mantiene el mismo layout en todas las diapositivas.
- `aleatoria_controlada`: varia el layout con una secuencia controlada.

## Estilos

- `academico_formal`
- `tecnologico_oscuro`
- `alto_impacto`
- `ingenieria_codigo`
- `pizarra_matematica`
- `laboratorio_redes`
- `ciberseguridad`
- `minimalista_claro`
- `universitario_elegante`
- `seminario_ejecutivo`
- `taller_practico`
- `modo_examen`
- `clase_visual`

## Tipos de diapositiva

- `contenido`: layout general con bullets e imagen/diseno.
- `codigo`: bloque de codigo con soporte para triple backtick.
- `columnas`: divide bullets en dos paneles.
- `ruta`: muestra una secuencia de pasos.
- `frase`: resalta una idea central a gran escala.
- `seccion`: crea un separador visual para bloques grandes de la clase.
- `diagrama`: organiza bullets como mapa conceptual o como diagrama especializado usando `Diagrama:`.
- `diagrama` con `Diagrama: cdn`: dibuja una arquitectura de CDN con usuario, DNS/enrutamiento, borde, cache, origen e ISP/backbone.
- `diagrama` con `Diagrama: flujo`: dibuja un proceso paso a paso.
- `diagrama` con `Diagrama: bloques`: dibuja bloques funcionales.
- `diagrama` con `Diagrama: casos de uso`: dibuja actores alrededor del sistema.
- `diagrama` con `Diagrama: arquitectura`, `topologia` o `protocolo`: dibuja capas o componentes relacionados.
- `actividad`: soporte heredado; no se recomienda para contenido generado por LLM porque el formato actual prohibe actividades, tareas y entregables dentro de la presentacion.
- `repositorio`: presenta recursos o enlaces como tarjetas.

## Formato de entrada

Revisa `FORMATO_CLASE.md` y `ejemplos/redes_computadoras.md`.

`FORMATO_CLASE.md` incluye reglas para que un LLM genere contenido completo: todo bloque anunciado en `Agenda:` o `Contenido Presentacion:` debe desarrollarse en diapositivas posteriores, y cada `Tipo: seccion` debe ir seguido por contenido real.

Antes de generar, valida el checklist de calidad del formato para evitar diapositivas vacias, temas inconclusos o layouts repetitivos.

## Historial de Cambios

### v0.9

- Se agrego soporte para el campo `Diagrama:` en diapositivas `Tipo: diagrama`.
- Se agregaron layouts especificos para diagramas `cdn`, `flujo`, `bloques`, `casos de uso`, `secuencia`, `arquitectura`, `topologia`, `mapa conceptual` y `protocolo`.
- El parser Markdown ahora conserva el tipo de diagrama solicitado.
- `FORMATO_CLASE.md` documenta ejemplos de CDN, flujo y casos de uso.
- La estructura del proyecto se mantiene: puntos de entrada y documentacion en raiz; logica interna en `motor/`.

### v0.8

- Se agrego `maestro.py` como lanzador unico de la interfaz web.
- Se organizaron los modulos internos del generador dentro de `motor/`.
- Se actualizaron los imports de Streamlit y del generador de terminal para usar el paquete `motor`.
- El formato de presentaciones ya no exige ni genera actividades, tareas, laboratorios, preguntas guiadas o entregables.
- Toda presentacion debe incluir fechas de parciales, `Que aprendiste` y `Que queda pendiente`, sin una seccion `Como continua el modulo`.
- Se conservaron `ñ`, acentos y caracteres propios del español en los Markdown de presentacion.

### v0.7

- Se agrego exportacion opcional a PDF mediante LibreOffice headless.
- La interfaz mantiene el PPTX como descarga principal y permite generar PDF despues.
- La terminal acepta `--pdf` para convertir el PPTX generado.
- Se agrego `exportadores.py` para aislar deteccion y conversion con LibreOffice.
- Los PDF generados en `salidas/` y `temp/` quedan excluidos de Git.
- Se mejoro el ajuste de texto en diapositivas densas, actividades y cierre.
- Se documento la instalacion de LibreOffice en Codespaces.

### v0.6

- Se agregaron cinco estilos visuales nuevos.
- Se agregaron tipos avanzados de diapositiva con `Tipo:`.
- Se agrego `Tipo: seccion` y formato automatico para diapositivas con solo titulo.
- Se mejoraron los layouts `ruta` y `diagrama` para reducir texto recortado y aprovechar mejor el espacio.
- Se agrego curador basico de imagenes en Streamlit.
- La biblioteca ahora prioriza imagenes favoritas/aprobadas y evita rechazadas.
- El curador ahora filtra por estado y muestra pendientes por defecto.
- `FORMATO_CLASE.md` ahora incluye instrucciones especificas para generacion con LLM.
- `FORMATO_CLASE.md` ahora incluye checklist de completitud para evitar bloques anunciados sin desarrollo.

### v0.5

- Se agrego soporte para imagenes locales en `assets/`.
- `Imagen Universidad:` ahora puede apuntar a un archivo local.
- Se agrego `Imagen Portada:` como alias mas claro para portada.
- Se agrego `Logo Portada:` para colocar el logo institucional sin recortarlo.
- Agenda y contenido ahora paginan listas largas y ajustan mejor tarjetas extensas.
- La portada respeta imagen local aunque el modo de imagen desactive APIs.
- `Imagen:` ahora puede apuntar a un archivo local por diapositiva.

### v0.4

- Se agrego portada institucional con imagen definida por `Imagen Universidad:`.
- Se agrego diapositiva automatica de agenda.
- Se agrego diapositiva automatica de contenido de la presentacion.
- Se agrego diapositiva final automatica con aprendizajes y frase motivacional.
- Se mejoro la interfaz Streamlit con una cabecera visual y mejor organizacion.

### v0.3

- Se agrego Pixabay como proveedor secundario de imagenes.
- Se agrego biblioteca local para reutilizar imagenes descargadas.
- Se agrego selector de distribucion: fija, alternada y aleatoria controlada.
- Se agrego boton para limpiar contenido en la interfaz.
- Se agregaron nuevos estilos visuales.
- Se documento `CONFIGURACION.md` para claves locales.

### v0.2

- Se mejoro el layout para titulos largos.
- Se agrego ingreso de API key desde la interfaz.
- Se agrego limpieza basica de Markdown y LaTeX.

### v0.1

- Primera version del generador.
- Interfaz Streamlit.
- Integracion inicial con Pexels.
- Soporte Markdown.
- Soporte para diapositivas con codigo.
