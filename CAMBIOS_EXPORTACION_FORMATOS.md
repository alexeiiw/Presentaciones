# Propuesta de cambios: exportacion a multiples formatos

## Contexto actual

El proyecto genera presentaciones academicas a partir de archivos Markdown estructurados.

Actualmente:

- La interfaz de Streamlit genera archivos `.pptx`.
- La interfaz permite indicar el nombre del archivo.
- Los archivos se guardan en `salidas/`.
- El comando de terminal permite elegir la ruta de salida con `--salida`.
- La fuente principal de contenido es el Markdown, que puede reutilizarse para crear varias presentaciones.
- No existe una exportacion integrada a PDF.
- El proyecto depende de `python-pptx` para construir las diapositivas.

Archivos relacionados:

- `app.py`: interfaz web y descarga del PPTX.
- `generador_clases.py`: construccion y guardado de la presentacion.
- `generar_desde_md.py`: generacion desde la terminal.
- `requirements.txt`: dependencias actuales.
- `salidas/`: carpeta donde se guardan las presentaciones generadas.

## Problema

A veces el usuario no tiene acceso a una computadora con Microsoft PowerPoint. En ese caso puede generar la presentacion, pero no puede abrirla para exportarla manualmente a PDF.

El PDF es importante porque el usuario normalmente presenta, comparte o transporta sus materiales en ese formato. La solucion no debe depender exclusivamente de tener PowerPoint instalado.

Tambien se necesita conservar la posibilidad de generar varias versiones desde una misma fuente Markdown, por ejemplo:

```text
salidas/redes_computadoras.pptx
salidas/redes_computadoras.pdf
salidas/redes_computadoras.txt
salidas/redes_computadoras.html
```

Los nombres pueden cambiar segun el tema o la clase:

```text
salidas/presentacion_1.pptx
salidas/presentacion_1.pdf
salidas/presentacion_2.pptx
salidas/presentacion_2.pdf
```

## Objetivo general

Permitir que una misma clase en Markdown genere uno o varios formatos de salida, incluyendo PDF, sin exigir Microsoft PowerPoint en el equipo del usuario.

## Objetivos especificos

1. Mantener la generacion actual de `.pptx`.
2. Agregar una opcion para generar `.pdf` automaticamente.
3. Permitir seleccionar uno o varios formatos desde Streamlit.
4. Permitir seleccionar formatos desde la terminal.
5. Guardar todos los archivos en `salidas/` con nombres consistentes.
6. Evitar que generar un formato destruya accidentalmente otro archivo.
7. Mostrar claramente en la interfaz cuales archivos fueron creados y permitir descargarlos.
8. Mantener el Markdown como fuente unica para evitar duplicar contenido.

## Alternativas de implementacion

### Alternativa 1: LibreOffice en modo headless

Generar primero el `.pptx` con `python-pptx` y convertirlo mediante LibreOffice sin abrir una interfaz grafica:

```bash
libreoffice --headless --convert-to pdf \
  --outdir salidas salidas/presentacion_1.pptx
```

**Ventajas:**

- Funciona en Linux, Codespaces y servidores.
- Puede automatizarse desde Python.
- No requiere Microsoft PowerPoint.
- Conserva el flujo actual basado en PPTX.

**Riesgos o requisitos:**

- LibreOffice debe estar instalado en el entorno.
- La fidelidad visual puede diferir ligeramente de PowerPoint.
- Deben comprobarse fuentes, imagenes, tamanos y saltos de pagina.

**Valoracion:** alternativa recomendada para una primera implementacion.

### Alternativa 2: Impresora virtual o funcion "Imprimir a PDF"

Agregar un flujo que use la impresion del sistema operativo para seleccionar una impresora PDF, por ejemplo:

- Microsoft Print to PDF en Windows.
- Guardar como PDF en macOS.
- Una impresora virtual PDF en Linux.

**Ventajas:**

- Es familiar para el usuario.
- Puede producir un PDF sin usar la opcion de exportacion de PowerPoint.
- Puede servir como respaldo cuando exista un programa capaz de abrir el PPTX.

**Limitaciones importantes:**

- La aplicacion no puede asumir que existe una impresora PDF instalada.
- Un servidor o Codespace normalmente no tiene una impresora grafica disponible.
- Automatizar una ventana de impresion depende del sistema operativo y es fragil.
- No es una buena solucion principal para un proceso web o sin interfaz grafica.

**Valoracion:** incluirlo como alternativa documentada o respaldo local, pero no como mecanismo principal del servidor.

### Alternativa 3: Convertir con Microsoft PowerPoint

Usar PowerPoint para abrir el PPTX y exportarlo a PDF.

**Ventajas:**

- Generalmente ofrece la mayor fidelidad visual.
- Es el flujo conocido por muchos usuarios.

**Limitaciones:**

- Requiere una computadora con PowerPoint.
- No resuelve el problema principal del usuario.
- No es apropiado para automatizacion en Linux o Codespaces.

**Valoracion:** mantenerlo como alternativa manual, no como dependencia del proyecto.

### Alternativa 4: Google Slides u otro servicio web

Subir el PPTX a Google Slides, OnlyOffice u otro servicio compatible y descargarlo como PDF.

**Ventajas:**

- No requiere PowerPoint instalado.
- Puede funcionar desde un navegador.

**Limitaciones:**

- Requiere subir el archivo a un servicio externo.
- Puede haber problemas de privacidad, conectividad o fidelidad.
- No es una conversion automatica integrada al proyecto.

**Valoracion:** alternativa manual para el usuario, no primera opcion tecnica.

### Alternativa 5: Generar PDF directamente desde Python

Crear el PDF desde la misma informacion que genera el PPTX, usando una biblioteca de PDF.

**Ventajas:**

- No depende de LibreOffice ni PowerPoint.
- Puede ser totalmente automatizado.

**Limitaciones:**

- Habria que implementar de nuevo todos los layouts visuales para PDF.
- El PDF y el PPTX podrian quedar visualmente diferentes.
- Aumenta bastante el mantenimiento del proyecto.

**Valoracion:** considerar en una fase posterior solo si se necesita control total del PDF.

## Propuesta recomendada

Implementar una capa de exportacion con varios formatos y usar LibreOffice como convertidor de PPTX a PDF cuando este disponible.

Flujo propuesto:

```text
Markdown
  -> parser_markdown.py
  -> modelo de clase
  -> generador de formatos
       -> PPTX
       -> PDF mediante LibreOffice
       -> otros formatos futuros
  -> carpeta salidas/
```

El PPTX debe seguir siendo el formato base para la presentacion visual. El PDF se obtiene a partir de ese PPTX para mantener la mayor consistencia posible entre ambos archivos.

## Requisitos funcionales propuestos

### Interfaz Streamlit

Agregar una seccion llamada `Formatos de salida` con opciones seleccionables:

- `PPTX`.
- `PDF`.
- Futuros formatos, sin tener que redisenar todo el flujo.

Comportamiento esperado:

- `PPTX` seleccionado: genera el archivo `.pptx`.
- `PDF` seleccionado: genera el `.pptx` base y luego el `.pdf`, o convierte una salida existente.
- Ambos seleccionados: genera los dos archivos.
- La interfaz muestra un boton de descarga independiente para cada formato.
- Si LibreOffice no esta disponible, la interfaz explica el problema y conserva la descarga del PPTX.
- El nombre indicado por el usuario se reutiliza cambiando solamente la extension.

Ejemplo:

```text
Nombre base: redes_computadoras
Formatos: PPTX y PDF

Resultado:
- salidas/redes_computadoras.pptx
- salidas/redes_computadoras.pdf
```

### Interfaz de terminal

Ampliar `generar_desde_md.py` con una opcion semejante a:

```bash
python generar_desde_md.py ejemplos/redes_computadoras.md \
  --salida salidas/redes_computadoras.pptx \
  --formatos pptx,pdf \
  --estilo tecnologico_oscuro
```

Tambien podria aceptarse una ruta base sin extension, siempre que la decision quede documentada:

```bash
python generar_desde_md.py ejemplos/redes_computadoras.md \
  --salida salidas/redes_computadoras \
  --formatos pptx,pdf
```

La opcion debe validar formatos desconocidos y devolver un mensaje claro.

### Organizacion de archivos

Todos los formatos derivados de una presentacion deben compartir el mismo nombre base:

```text
salidas/
  redes_computadoras.pptx
  redes_computadoras.pdf
```

No se deben mezclar archivos temporales con las salidas finales. Si LibreOffice necesita una carpeta temporal, debe utilizar `temp/` y limpiarla al terminar cuando sea posible.

## Requisitos no funcionales

- La conversion debe funcionar sin PowerPoint.
- El sistema debe detectar si LibreOffice esta instalado.
- Los errores de conversion deben mostrarse sin ocultar el PPTX ya generado.
- La solucion debe funcionar desde Streamlit y desde la terminal.
- Las rutas deben manejarse con `pathlib`.
- No se deben introducir claves API nuevas para exportar.
- La generacion de un solo PPTX debe continuar funcionando como antes.
- La documentacion debe explicar como instalar LibreOffice en el entorno utilizado.

## Plan sugerido de implementacion

1. Crear un modulo dedicado, por ejemplo `exportadores.py`, para separar la conversion de formatos del generador de diapositivas.
2. Implementar una funcion para detectar LibreOffice.
3. Implementar una funcion para convertir un PPTX a PDF usando un proceso no interactivo.
4. Integrar la seleccion de formatos en `app.py`.
5. Integrar `--formatos` en `generar_desde_md.py`.
6. Agregar mensajes de error y advertencias cuando PDF no pueda generarse.
7. Actualizar `README.md` y `CONFIGURACION.md`.
8. Probar varios nombres de archivo, espacios, formatos seleccionados y ausencia de LibreOffice.

## Casos de prueba minimos

- Generar solamente PPTX.
- Generar solamente PDF.
- Generar PPTX y PDF.
- Generar dos presentaciones con nombres diferentes.
- Regenerar una presentacion y confirmar el comportamiento ante archivos existentes.
- Usar un nombre con espacios y caracteres acentuados.
- Ejecutar la conversion cuando LibreOffice no esta instalado.
- Confirmar que un error de PDF no impide descargar el PPTX.
- Confirmar que el PDF resultante tiene el mismo numero de diapositivas que el PPTX.
- Confirmar que imagenes, titulos y texto no quedan recortados en el PDF.

## Decision pendiente para la siguiente IA

La siguiente IA debe analizar si conviene implementar primero:

1. Solo LibreOffice como conversion automatica.
2. LibreOffice mas una opcion manual de "imprimir a PDF" documentada.
3. Un sistema general de exportadores preparado para PPTX, PDF, HTML y otros formatos.

La recomendacion inicial de este documento es la opcion 1, con una arquitectura suficientemente separada para agregar otros formatos despues. La opcion de imprimir a PDF debe quedar documentada como respaldo del usuario, pero no debe ser un requisito del servidor ni de la aplicacion Streamlit.
