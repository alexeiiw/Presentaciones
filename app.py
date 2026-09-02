from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from generador_clases import generar_presentacion
from parser_markdown import parsear_markdown


load_dotenv()

EJEMPLO = """# Clase: Introduccion a Redes de Computadoras

Profesor: Prof. Nombre
Asignatura: Redes de Computadoras
Universidad: Universidad Ejemplo
Estilo: tecnologico_oscuro

## Diapositiva: Objetivo de la clase

Objetivo: Comprender los conceptos fundamentales de las redes de computadoras y su importancia en sistemas modernos.

Contenido:
- Identificar que es una red de computadoras.
- Reconocer los componentes basicos de una red.
- Diferenciar tipos de redes segun su alcance.
- Comprender la funcion de los protocolos de comunicacion.

Imagen: computer network infrastructure

## Diapositiva: Ejemplo en Python

Tipo: codigo

Objetivo: Mostrar una funcion simple para calcular latencia promedio.

```python
def latencia_promedio(mediciones_ms):
    return sum(mediciones_ms) / len(mediciones_ms)
```

Imagen: programming code network
"""


st.set_page_config(page_title="Generador de Presentaciones", page_icon="PPTX", layout="wide")

st.title("Generador de presentaciones academicas")
st.caption("Pega una clase en Markdown, selecciona estilo y genera un archivo .pptx.")

with st.sidebar:
    st.header("Configuracion")
    nombre_archivo = st.text_input("Nombre del archivo", value="presentacion_clase")
    estilo = st.selectbox("Estilo visual", ["academico_formal", "tecnologico_oscuro", "alto_impacto"], index=1)
    modo_imagen = st.selectbox("Modo de imagen", ["pexels_o_diseno", "pexels", "solo_diseno", "sin_imagen"], index=0)
    st.info("La clave PEXELS_API_KEY se lee desde .env o variables de entorno del Codespace.")

markdown = st.text_area("Contenido de la clase en Markdown", value=EJEMPLO, height=560)

if st.button("Generar presentacion", type="primary"):
    if not markdown.strip():
        st.error("Pega el contenido de la clase antes de generar.")
    else:
        try:
            clase = parsear_markdown(markdown)
            salida = Path("salidas") / f"{nombre_archivo.strip() or 'presentacion_clase'}.pptx"
            ruta = generar_presentacion(clase, salida, estilo_nombre=estilo, modo_imagen=modo_imagen)
            st.success(f"Presentacion generada: {ruta}")
            with open(ruta, "rb") as archivo:
                st.download_button(
                    "Descargar PPTX",
                    data=archivo,
                    file_name=ruta.name,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
        except Exception as exc:
            st.error(f"No se pudo generar la presentacion: {exc}")
