from pathlib import Path
import os

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

if "markdown_clase" not in st.session_state:
    st.session_state.markdown_clase = EJEMPLO


def limpiar_contenido() -> None:
    st.session_state.markdown_clase = ""

with st.sidebar:
    st.header("Configuracion")
    nombre_archivo = st.text_input("Nombre del archivo", value="presentacion_clase")
    estilo = st.selectbox(
        "Estilo visual",
        [
            "academico_formal",
            "tecnologico_oscuro",
            "alto_impacto",
            "ingenieria_codigo",
            "pizarra_matematica",
            "laboratorio_redes",
            "ciberseguridad",
            "minimalista_claro",
        ],
        index=1,
    )
    modo_imagen = st.selectbox(
        "Modo de imagen",
        [
            "biblioteca_pexels_pixabay",
            "biblioteca_pexels",
            "pexels_pixabay",
            "pexels_o_diseno",
            "pexels",
            "pixabay",
            "solo_biblioteca",
            "solo_diseno",
            "sin_imagen",
        ],
        index=0,
    )
    distribucion = st.selectbox("Distribucion", ["alternada", "fija", "aleatoria_controlada"], index=0)
    pexels_key = st.text_input("PEXELS_API_KEY", value=os.getenv("PEXELS_API_KEY", ""), type="password")
    pixabay_key = st.text_input("PIXABAY_API_KEY", value=os.getenv("PIXABAY_API_KEY", ""), type="password")
    if pexels_key.strip():
        os.environ["PEXELS_API_KEY"] = pexels_key.strip()
    if pixabay_key.strip():
        os.environ["PIXABAY_API_KEY"] = pixabay_key.strip()
    st.info("Puedes pegar las claves aqui o configurarlas como variables de entorno del Codespace.")

markdown = st.text_area("Contenido de la clase en Markdown", key="markdown_clase", height=560)

col1, col2 = st.columns([1, 1])
generar = col1.button("Generar presentacion", type="primary")
col2.button("Limpiar contenido", on_click=limpiar_contenido)

if generar:
    if not markdown.strip():
        st.error("Pega el contenido de la clase antes de generar.")
    else:
        try:
            clase = parsear_markdown(markdown)
            salida = Path("salidas") / f"{nombre_archivo.strip() or 'presentacion_clase'}.pptx"
            ruta = generar_presentacion(
                clase,
                salida,
                estilo_nombre=estilo,
                modo_imagen=modo_imagen,
                distribucion=distribucion,
            )
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
