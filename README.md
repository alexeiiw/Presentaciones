# Presentaciones

Generador de presentaciones academicas de alto impacto usando Python, Streamlit, python-pptx, biblioteca local de imagenes, Pexels y Pixabay.

## Instalacion en GitHub Codespaces

```bash
pip install -r requirements.txt
```

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

## Generar desde terminal

```bash
python generar_desde_md.py ejemplos/redes_computadoras.md --salida salidas/redes_computadoras.pptx --estilo tecnologico_oscuro
```

## Uso

- Pega el Markdown de la clase.
- Define `Agenda:`, `Contenido Presentacion:`, `Aprendizajes:` y `Frase Final:` si quieres usar la estructura academica completa.
- Selecciona estilo visual.
- Selecciona modo de imagen.
- Selecciona distribucion de diapositivas.
- Genera y descarga el archivo `.pptx`.
- El archivo tambien queda guardado dentro de `salidas/`.

## Imagenes Locales

Puedes subir imagenes al Codespace dentro de `assets/` y usarlas directamente desde el Markdown.

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

## Formato de entrada

Revisa `FORMATO_CLASE.md` y `ejemplos/redes_computadoras.md`.

## Historial de Cambios

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
