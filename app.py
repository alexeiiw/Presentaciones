from pathlib import Path
import os

import streamlit as st
from dotenv import load_dotenv

from biblioteca_imagenes import actualizar_estado, leer_index
from estilos import nombres_estilos
from generador_clases import generar_presentacion
from parser_markdown import parsear_markdown


load_dotenv()

EJEMPLO = """# Clase: Introduccion a Redes de Computadoras

Profesor: Prof. Nombre
Asignatura: Redes de Computadoras
Universidad: Universidad Ejemplo
Estilo: tecnologico_oscuro
Imagen Portada: images.jpg
Logo Portada: Umg.png

Agenda:
- Bienvenida y contexto de la semana
- Revisión de conceptos previos
- Desarrollo del tema central
- Demostración técnica guiada
- Actividad practica de cierre

Contenido Presentacion:
- Objetivo de la clase
- Fundamentos de redes de computadoras
- Componentes principales
- Ejemplo técnico aplicado
- Cierre y aprendizajes

Aprendizajes:
- Diferenciar componentes físicos y lógicos de una red.
- Explicar la función básica de los protocolos de comunicación.
- Relacionar redes con servicios modernos de internet.

Frase Final: La ingeniería se aprende mejor cuando conectas teoría, práctica y criterio técnico.

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

## Diapositiva: Ruta de aprendizaje

Tipo: ruta

Contenido:
- Concepto base
- Demostracion guiada
- Practica individual
- Discusion tecnica
- Evidencia final
"""


st.set_page_config(page_title="Generador de Presentaciones", page_icon="PPTX", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        padding: 1.2rem 1.4rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #0f172a 0%, #164e63 55%, #0891b2 100%);
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
    }
    .main-title h1 { margin: 0; font-size: 2.1rem; }
    .main-title p { margin: .35rem 0 0 0; color: #cffafe; }
    .panel-note {
        padding: .85rem 1rem;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        color: #334155;
        margin-bottom: .8rem;
    }
    </style>
    <div class="main-title">
        <h1>Generador de presentaciones academicas</h1>
        <p>Markdown estructurado, imagenes reutilizables, estilos visuales y salida PowerPoint lista para clase.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="panel-note">
    Flujo recomendado: escribe la clase en Markdown, define agenda y aprendizajes, selecciona estilo, genera el PPTX y descargalo.
    </div>
    """,
    unsafe_allow_html=True,
)

if "markdown_clase" not in st.session_state:
    st.session_state.markdown_clase = EJEMPLO


def limpiar_contenido() -> None:
    st.session_state.markdown_clase = ""

with st.sidebar:
    st.header("Configuracion de salida")
    nombre_archivo = st.text_input("Nombre del archivo", value="presentacion_clase")
    estilo = st.selectbox(
        "Estilo visual",
        nombres_estilos(),
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
    st.info("Las claves se pueden pegar aqui, guardarlas en .env o exportarlas como variables de entorno.")

tab_editor, tab_curador = st.tabs(["Generador", "Curador de imagenes"])

with tab_editor:
    st.subheader("Contenido fuente")
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

with tab_curador:
    st.subheader("Biblioteca local")
    registros = leer_index()
    if not registros:
        st.info("Aun no hay imagenes descargadas en la biblioteca local.")
    else:
        st.caption("Marca como favorita o aprobada para priorizarla. Marca como rechazada para excluirla de futuras presentaciones.")
        estados = ["pendiente", "aprobada", "favorita", "rechazada"]
        conteos = {estado: sum(1 for r in registros if r.get("estado", "pendiente") == estado) for estado in estados}
        st.write(
            f"Pendientes: {conteos['pendiente']} | Aprobadas: {conteos['aprobada']} | "
            f"Favoritas: {conteos['favorita']} | Rechazadas: {conteos['rechazada']}"
        )
        filtro = st.radio(
            "Mostrar imagenes",
            ["pendiente", "aprobada", "favorita", "rechazada", "todas"],
            horizontal=True,
            index=0,
        )
        registros_filtrados = [
            (indice, registro)
            for indice, registro in enumerate(registros)
            if filtro == "todas" or registro.get("estado", "pendiente") == filtro
        ]
        if not registros_filtrados:
            st.info("No hay imagenes en este filtro.")
        for indice, registro in registros_filtrados:
            titulo_registro = f"{indice + 1:03d} | {registro.get('keyword', 'sin keyword')} | {registro.get('proveedor', 'local')}"
            with st.expander(titulo_registro):
                archivo_valor = registro.get("archivo", "")
                archivo = Path(archivo_valor) if archivo_valor else None
                col_img, col_meta = st.columns([1, 2])
                if archivo and archivo.exists() and archivo.is_file():
                    col_img.image(str(archivo), use_container_width=True)
                else:
                    col_img.warning("Archivo no encontrado")
                col_meta.write(f"**Archivo:** `{registro.get('archivo', '')}`")
                col_meta.write(f"**Usos:** {registro.get('usos', 0)}")
                if registro.get("url"):
                    col_meta.write(f"**URL:** {registro.get('url')}")
                estado_actual = registro.get("estado", "pendiente")
                estado = col_meta.selectbox(
                    "Estado",
                    estados,
                    index=estados.index(estado_actual) if estado_actual in estados else 0,
                    key=f"estado_imagen_{indice}",
                )
                if col_meta.button("Guardar estado", key=f"guardar_estado_{indice}"):
                    actualizar_estado(indice, estado)
                    st.success("Estado actualizado.")
