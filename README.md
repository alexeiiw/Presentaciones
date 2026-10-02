# Presentaciones

Generador de presentaciones academicas de alto impacto usando Python, Streamlit, python-pptx, biblioteca local de imagenes, Pexels y Pixabay.

Version actual: `v0.12`

## Estructura del proyecto

```text
Presentaciones/
├── maestro.py                 # Entrada recomendada para abrir la interfaz web
├── app.py                     # Interfaz Streamlit
├── generar_desde_md.py        # Entrada para generar desde terminal
├── motor/                     # Modulos internos del generador
├── ejemplos/                  # Markdown de referencia
├── tests/                     # Pruebas del parser, motor e interfaz
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
- Revisa la validación previa, el resumen de diapositivas e imágenes y la vista de estructura antes de generar.
- Corrige los errores bloqueantes. Las recomendaciones de contenido, agenda e imágenes no bloquean la generación.
- Define `Agenda:`, `Contenido Presentacion:`, `Aprendizajes:` y `Frase Final:` para usar la estructura academica completa.
- `Fechas Parciales:` y `Qué queda pendiente:` crean diapositivas dedicadas cuando incluyen elementos. Si faltan, la validación lo informa como recomendación.
- Selecciona estilo visual.
- Selecciona modo de imagen.
- Selecciona distribucion de diapositivas.
- Genera y descarga primero el archivo `.pptx`.
- Para convertir el PPTX de la generación actual, usa `Generar PDF desde este PPTX`.
- Para convertir o volver a generar el PDF de cualquier PPTX guardado anteriormente, abre la pestaña `Convertir PPTX a PDF`, selecciona el archivo y pulsa `Convertir a PDF` o `Regenerar PDF`.
- Los archivos quedan guardados dentro de `salidas/`.
- Los `.pptx` y `.pdf` generados en `salidas/` estan excluidos de Git por defecto.
- Cambiar el Markdown, nombre de archivo o configuración invalida la descarga anterior hasta regenerar, evitando descargar por error una versión desactualizada.

## Pruebas

Con las dependencias instaladas desde `requirements.txt`, ejecuta:

```bash
python -m unittest discover -s tests -v
```

La suite revisa la validación del ejemplo, parser, layouts y estilos, reemplazo de PPTX, biblioteca/proveedores de imágenes, rutas locales, integración de generación con Streamlit y conversión de archivos PPTX guardados.

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

Desde la pestaña `Curador de imagenes` puedes revisar todas las imágenes en una galería, filtrar por estado y seleccionarlas individualmente o en lote. Usa las acciones masivas para aprobar, marcar como favoritas o rechazar la selección. Al pasar el cursor por una miniatura se muestra la keyword/descripción, proveedor, archivo, usos, estado y URL disponibles. El generador prioriza favoritas y aprobadas, y excluye rechazadas.

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

La interfaz muestra ahora esta revisión automáticamente y permite generar con recomendaciones, bloqueando solo errores que impedirían una salida útil. El PPTX se reemplaza al generar con el mismo nombre para facilitar iteraciones. La pestaña `Convertir PPTX a PDF` permite seleccionar presentaciones persistidas en `salidas/` en una sesión posterior.

## Historial de Cambios

### v0.12

- Se renovó el curador como galería visual con filtros y selección individual o de todas las imágenes visibles.
- Se añadieron acciones masivas para aprobar, marcar favoritas o rechazar imágenes.
- Las miniaturas muestran al pasar el cursor la keyword/descripción y metadatos disponibles de proveedor, archivo, usos, estado y URL.
- Se añadieron pruebas para cambios de estado masivos y visualización de la galería.

### v0.11

- Se agregó una pestaña independiente para listar, seleccionar y convertir a PDF cualquier PPTX guardado en `salidas/`, incluso si se generó en otra sesión.
- Si el PDF ya existe, la interfaz permite regenerarlo y descargarlo desde esa misma pestaña.
- Se actualizó la guía operativa y se añadieron pruebas automatizadas del flujo de conversión posterior.

### v0.10

- Se añadió revisión automática de la clase antes de generar, con errores bloqueantes, recomendaciones, conteo y vista previa estructural.
- Se alinearon el formato, el parser y el generador para admitir `Fechas Parciales:` y `Qué queda pendiente:` como diapositivas dedicadas cuando tienen elementos.
- Se aclaró el cierre de aprendizajes y se amplió el formato de clase para que los campos opcionales no frenen la preparación.
- La interfaz advierte cuando el Markdown o la configuración cambian después de generar y evita ofrecer una descarga desactualizada.
- Se mejoró la presentación de controles, opciones e información de revisión en la interfaz.
- Se corrigió la selección de imágenes para no repetir resultados agotados de Pexels/Pixabay y se estabilizaron rutas de biblioteca, imágenes locales y temporales.
- Se añadieron pruebas automatizadas de operación para parser, layouts, estilos, imágenes, rutas, generación e interfaz.

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
