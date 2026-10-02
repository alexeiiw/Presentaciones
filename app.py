from pathlib import Path
import base64
from html import escape
import json
import os
import re
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from motor.biblioteca_imagenes import (
    _resolver_archivo as resolver_archivo_biblioteca,
    actualizar_estado,
    actualizar_estados_archivos,
    leer_index,
)
from motor.estilos import nombres_estilos
from motor.exportadores import convertir_pptx_a_pdf
from motor.generador_clases import contar_diapositivas_estimadas, generar_presentacion
from motor.parser_markdown import parsear_markdown
from motor.validaciones import validar_clase


ROOT = Path(__file__).resolve().parent
SALIDAS = ROOT / "salidas"


load_dotenv()

EJEMPLO = """# Clase: Introduccion a Redes de Computadoras

Profesor: Prof. Nombre
Asignatura: Redes de Computadoras
Universidad: Universidad Ejemplo
Estilo: tecnologico_oscuro
Imagen Portada: images.jpg
Logo Portada: Umg.png

Agenda:
- Fundamentos de redes de computadoras
- Componentes principales
- Arquitectura de red básica
- Ejemplo en Python
- Ruta de aprendizaje
- Fechas de parciales y síntesis final

Contenido Presentacion:
- Objetivo de la clase
- Fundamentos de redes de computadoras
- Componentes principales
- Arquitectura de red básica
- Ejemplo en Python
- Ruta de aprendizaje
- Fechas de parciales
- Aprendizajes y qué queda pendiente

Fechas Parciales:
- Parcial 1: agrega aquí la fecha confirmada

Qué queda pendiente:
- Profundizar en protocolos de enrutamiento en la próxima clase

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

## Diapositiva: Arquitectura de red básica

Tipo: diagrama

Diagrama: bloques

Contenido:
- Usuario: inicia solicitudes desde un dispositivo final.
- Switch: conecta dispositivos dentro de la red local.
- Router: dirige tráfico entre redes.
- Firewall: aplica reglas de seguridad.
- Servidor: entrega servicios y recursos.

## Diapositiva: Ruta de aprendizaje

Tipo: ruta

Contenido:
- Concepto base
- Demostracion guiada
- Practica individual
- Discusion tecnica
- Evidencia final
"""


st.set_page_config(page_title="Generador de Presentaciones", page_icon="🎓", layout="wide")

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
    .stButton > button { border-radius: 10px; font-weight: 600; min-height: 2.7rem; }
    div[data-testid="stMetric"] { background: #f8fafc; border: 1px solid #e2e8f0; padding: .8rem; border-radius: 12px; }
    div[data-testid="stTabs"] button { font-weight: 600; }
    div[data-testid="stExpander"] { border-radius: 12px; }
    .block-container { padding-top: 1.6rem; padding-bottom: 2.5rem; }
    .image-gallery-card { position: relative; overflow: hidden; border-radius: 10px; }
    .image-gallery-card img { display: block; width: 100%; height: 190px; object-fit: cover; }
    .image-metadata-tooltip {
        position: absolute; inset: auto 0 0; max-height: 100%; overflow-y: auto;
        padding: .8rem; color: #fff; background: rgba(15, 23, 42, .94);
        font-size: .82rem; line-height: 1.5; opacity: 0; visibility: hidden;
        transition: opacity .16s ease; overflow-wrap: anywhere;
    }
    .image-gallery-card:hover .image-metadata-tooltip,
    .image-gallery-card:focus-within .image-metadata-tooltip { opacity: 1; visibility: visible; }
    </style>
    <div class="main-title">
        <h1>Generador de presentaciones academicas</h1>
        <p>Markdown estructurado, imagenes reutilizables, estilos visuales, salida PowerPoint y PDF opcional.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="panel-note">
    Flujo recomendado: escribe la clase en Markdown, genera primero el PPTX y luego crea el PDF opcional si lo necesitas.
    </div>
    """,
    unsafe_allow_html=True,
)

if "markdown_clase" not in st.session_state:
    st.session_state.markdown_clase = EJEMPLO
if "pptx_generado" not in st.session_state:
    st.session_state.pptx_generado = None
if "pdf_generado" not in st.session_state:
    st.session_state.pdf_generado = None


def limpiar_contenido() -> None:
    st.session_state.markdown_clase = ""
    st.session_state.pptx_generado = None
    st.session_state.pdf_generado = None
    st.session_state.markdown_generado = None


def normalizar_nombre_archivo(nombre: str) -> str:
    seguro = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", nombre.strip()).strip(" ._")
    return seguro or "presentacion_clase"


def firma_generacion(markdown: str, nombre: str, estilo: str, modo_imagen: str, distribucion: str) -> str:
    return json.dumps(
        [markdown, normalizar_nombre_archivo(nombre), estilo, modo_imagen, distribucion],
        ensure_ascii=False,
    )


def imagen_galeria_data_uri(ruta: Path) -> str:
    with Image.open(ruta) as imagen:
        imagen.thumbnail((480, 360))
        if imagen.mode not in {"RGB", "L"}:
            imagen = imagen.convert("RGB")
        elif imagen.mode == "L":
            imagen = imagen.convert("RGB")
        buffer = BytesIO()
        imagen.save(buffer, format="JPEG", quality=72, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def actualizar_seleccion_imagen(indice: int) -> None:
    seleccionadas = st.session_state.setdefault("imagenes_seleccionadas", set())
    if st.session_state.get(f"seleccionar_imagen_{indice}", False):
        seleccionadas.add(indice)
    else:
        seleccionadas.discard(indice)


def listar_presentaciones(directorio: Path = SALIDAS) -> list[Path]:
    directorio = Path(directorio)
    if not directorio.exists():
        return []
    return sorted(
        (archivo for archivo in directorio.glob("*.pptx") if archivo.is_file()),
        key=lambda archivo: archivo.stat().st_mtime,
        reverse=True,
    )


def mostrar_convertidor_pptx() -> None:
    st.subheader("Convertir un PowerPoint guardado a PDF")
    st.caption("Selecciona una presentación de salidas/. También aparecen archivos creados en sesiones anteriores.")
    presentaciones = listar_presentaciones()
    if not presentaciones:
        st.info(
            "Todavía no hay archivos PPTX en salidas/. Genera una presentación y aparecerá aquí "
            "para convertirla cuando quieras."
        )
        return

    archivos_por_etiqueta = {
        f"{archivo.name} · {archivo.stat().st_size / (1024 * 1024):.1f} MB": archivo
        for archivo in presentaciones
    }
    seleccion_etiqueta = st.selectbox(
        "Presentación guardada",
        list(archivos_por_etiqueta),
        key="pptx_existente_seleccionado",
    )
    seleccion = archivos_por_etiqueta[seleccion_etiqueta]
    salida_pdf = seleccion.with_suffix(".pdf")
    pdf_existente = salida_pdf.is_file()
    if pdf_existente:
        st.caption(f"Ya existe un PDF para este archivo: {salida_pdf.name}. Puedes regenerarlo para reemplazarlo.")
        texto_boton = "Regenerar PDF"
    else:
        st.caption("Aún no hay PDF para esta presentación.")
        texto_boton = "Convertir a PDF"

    if st.button(texto_boton, key="convertir_pptx_guardado", type="primary"):
        with st.spinner("Convirtiendo la presentación con LibreOffice..."):
            resultado = convertir_pptx_a_pdf(seleccion, salida_pdf)
        if resultado.ok and resultado.ruta:
            st.session_state.pdf_convertido_en_sesion = str(seleccion)
            st.success(resultado.mensaje)
        else:
            st.warning(resultado.mensaje)

    if salida_pdf.is_file() and (
        pdf_existente or st.session_state.get("pdf_convertido_en_sesion") == str(seleccion)
    ):
        with salida_pdf.open("rb") as archivo_pdf:
            st.download_button(
                "Descargar PDF seleccionado",
                data=archivo_pdf,
                file_name=salida_pdf.name,
                mime="application/pdf",
                key="descargar_pdf_existente",
            )


with st.sidebar:
    st.header("Ajustes de presentación")
    nombre_archivo = st.text_input("Nombre del archivo", value="presentacion_clase")
    st.caption("Al repetir este nombre, se reemplaza el PPTX anterior.")
    st.subheader("Diseño e imágenes")
    estilo = st.selectbox(
        "Estilo visual",
        nombres_estilos(),
        index=1,
        format_func=lambda nombre: nombre.replace("_", " ").title(),
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
        help="Intenta imágenes aprobadas de la biblioteca y luego proveedores externos. También puedes elegir solo diseño o sin imágenes.",
    )
    distribucion = st.selectbox(
        "Distribución de imágenes",
        ["alternada", "fija", "aleatoria_controlada"],
        index=0,
        format_func=lambda nombre: nombre.replace("_", " ").title(),
    )
    st.subheader("Proveedores opcionales")
    pexels_key = st.text_input("PEXELS_API_KEY", value=os.getenv("PEXELS_API_KEY", ""), type="password")
    pixabay_key = st.text_input("PIXABAY_API_KEY", value=os.getenv("PIXABAY_API_KEY", ""), type="password")
    if pexels_key.strip():
        os.environ["PEXELS_API_KEY"] = pexels_key.strip()
    if pixabay_key.strip():
        os.environ["PIXABAY_API_KEY"] = pixabay_key.strip()
    st.info("Las claves se pueden pegar aquí, guardarlas en .env o exportarlas como variables de entorno.")

tab_editor, tab_convertidor, tab_curador = st.tabs(
    ["✦ Crear presentación", "⇩ Convertir PPTX a PDF", "▧ Curador de imágenes"]
)

with tab_editor:
    st.subheader("Contenido fuente")
    markdown = st.text_area("Contenido de la clase en Markdown", key="markdown_clase", height=560)

    clase_validada = parsear_markdown(markdown) if markdown.strip() else None
    validacion = validar_clase(markdown, clase_validada, ROOT) if clase_validada else None
    if validacion:
        met1, met2, met3 = st.columns(3)
        met1.metric("Diapositivas de contenido", validacion.diapositivas_contenido)
        met2.metric("Total estimado", validacion.diapositivas_estimadas)
        met3.metric("Imágenes locales", validacion.imagenes_locales)
        if validacion.errores:
            with st.container(border=True):
                st.error("Corrige estos problemas antes de generar")
                for mensaje in validacion.errores:
                    st.markdown(f"- {mensaje}")
        elif validacion.advertencias:
            with st.expander(f"Revisión previa: {len(validacion.advertencias)} recomendaciones", expanded=True):
                st.success("La presentación puede generarse. Revisa los avisos para evitar sorpresas en el resultado.")
                for mensaje in validacion.advertencias:
                    st.markdown(f"- {mensaje}")
        else:
            st.success("Revisión previa correcta: no se encontraron problemas.")
        if clase_validada.diapositivas:
            with st.expander("Vista previa de la estructura"):
                for numero, diapositiva in enumerate(clase_validada.diapositivas, start=1):
                    detalle = f"{diapositiva.tipo.title()} · {len(diapositiva.contenido)} puntos"
                    st.markdown(f"**{numero:02d}. {diapositiva.titulo or 'Sin título'}**  \n{detalle}")

    col1, col2 = st.columns([1, 1])
    generar = col1.button("Generar presentación", type="primary", disabled=not validacion or not validacion.valido)
    col2.button("Limpiar contenido", on_click=limpiar_contenido)

    if generar:
        if not markdown.strip():
            st.error("Pega el contenido de la clase antes de generar.")
        else:
            try:
                clase = clase_validada or parsear_markdown(markdown)
                nombre_seguro = normalizar_nombre_archivo(nombre_archivo)
                salida = SALIDAS / f"{nombre_seguro}.pptx"
                salida.resolve().relative_to(SALIDAS.resolve())
                with st.spinner("Generando PowerPoint. La búsqueda de imágenes puede tardar unos momentos..."):
                    ruta = generar_presentacion(
                        clase,
                        salida,
                        estilo_nombre=estilo,
                        modo_imagen=modo_imagen,
                        distribucion=distribucion,
                    )
                st.session_state.pptx_generado = str(ruta)
                st.session_state.pdf_generado = None
                st.session_state.markdown_generado = markdown
                st.session_state.firma_generacion = firma_generacion(
                    markdown, nombre_archivo, estilo, modo_imagen, distribucion
                )
                st.success(f"Presentacion generada: {ruta}")
                st.caption(
                    f"Diapositivas generadas: {contar_diapositivas_estimadas(clase)}. "
                    "Si usas el mismo nombre, el archivo anterior se reemplaza."
                )
            except Exception as exc:
                st.error(f"No se pudo generar la presentacion: {exc}")

    firma_actual = firma_generacion(markdown, nombre_archivo, estilo, modo_imagen, distribucion)
    resultado_actual = bool(st.session_state.pptx_generado and st.session_state.get("firma_generacion") == firma_actual)
    pptx_generado = (
        Path(st.session_state.pptx_generado)
        if resultado_actual
        else None
    )
    if st.session_state.pptx_generado and not resultado_actual:
        st.info(
            "El contenido o la configuración cambió desde la última generación. "
            "Genera nuevamente para descargar la versión actual."
        )
    if pptx_generado and pptx_generado.exists():
        st.divider()
        st.subheader("Descargar o convertir la presentación")
        st.caption("Primero descarga el PowerPoint. Si la computadora no tiene Microsoft Office, genera y descarga también el PDF.")
        with open(pptx_generado, "rb") as archivo:
            st.download_button(
                "1. Descargar PowerPoint (.pptx)",
                data=archivo,
                file_name=pptx_generado.name,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key="descargar_pptx_generado",
            )
        col_convertir, col_nota = st.columns([1, 2])
        if col_convertir.button("2. Convertir este PPTX a PDF", type="primary", key="convertir_pptx_actual"):
            with st.spinner("Convirtiendo el PowerPoint a PDF con LibreOffice..."):
                resultado_pdf = convertir_pptx_a_pdf(pptx_generado)
            if resultado_pdf.ok and resultado_pdf.ruta:
                st.session_state.pdf_generado = str(resultado_pdf.ruta)
                st.success(resultado_pdf.mensaje)
            else:
                st.warning(resultado_pdf.mensaje)
        col_nota.caption("La conversión usa LibreOffice; no requiere tener Microsoft Office instalado en la computadora donde presentarás.")

    pdf_generado = Path(st.session_state.pdf_generado) if st.session_state.pdf_generado else None
    if pdf_generado and pdf_generado.exists():
        st.markdown("**Paso 3 · Descargar el PDF**")
        with open(pdf_generado, "rb") as archivo_pdf:
            st.download_button(
                "Descargar PDF para presentar",
                data=archivo_pdf,
                file_name=pdf_generado.name,
                mime="application/pdf",
                key="descargar_pdf_generado",
            )

with tab_convertidor:
    mostrar_convertidor_pptx()

with tab_curador:
    st.subheader("Galería de imágenes")
    registros = leer_index()
    if not registros:
        st.info("Aún no hay imágenes descargadas en la biblioteca local.")
    else:
        st.caption(
            "Selecciona varias miniaturas para aprobarlas o rechazarlas de una vez. "
            "Pasa el cursor sobre una imagen para ver sus datos."
        )
        estados = ["pendiente", "aprobada", "favorita", "rechazada"]
        conteos = {estado: sum(1 for r in registros if r.get("estado", "pendiente") == estado) for estado in estados}
        st.write(
            f"Pendientes: {conteos['pendiente']} | Aprobadas: {conteos['aprobada']} | "
            f"Favoritas: {conteos['favorita']} | Rechazadas: {conteos['rechazada']}"
        )
        if "imagenes_seleccionadas" not in st.session_state:
            st.session_state.imagenes_seleccionadas = set()
        rutas_por_indice = {
            indice: str(ruta)
            for indice, registro in enumerate(registros)
            if (ruta := resolver_archivo_biblioteca(registro.get("archivo", "")))
        }
        filtro = st.radio(
            "Filtrar imágenes por estado",
            ["pendiente", "aprobada", "favorita", "rechazada", "todas"],
            horizontal=True,
            index=4,
        )
        registros_filtrados = [
            (indice, registro)
            for indice, registro in enumerate(registros)
            if filtro == "todas" or registro.get("estado", "pendiente") == filtro
        ]
        if not registros_filtrados:
            st.info("No hay imágenes en este filtro.")
        else:
            indices_visibles = {indice for indice, _ in registros_filtrados}
            seleccionadas = st.session_state.imagenes_seleccionadas
            col_seleccion, col_acciones = st.columns([1, 2])
            with col_seleccion:
                seleccionar, limpiar = st.columns(2)
                if seleccionar.button("Seleccionar visibles", key="seleccionar_todas_imagenes"):
                    seleccionadas.update(indices_visibles)
                    for indice in indices_visibles:
                        st.session_state[f"seleccionar_imagen_{indice}"] = True
                    st.rerun()
                if limpiar.button("Limpiar selección", key="limpiar_seleccion_imagenes"):
                    seleccionadas.clear()
                    for indice in range(len(registros)):
                        st.session_state[f"seleccionar_imagen_{indice}"] = False
                    st.rerun()

            with col_acciones:
                st.caption(f"{len(seleccionadas)} imágenes seleccionadas")
                masiva_1, masiva_2, masiva_3 = st.columns(3)
                if masiva_1.button("Aprobar seleccionadas", disabled=not seleccionadas, key="aprobar_imagenes_masivo"):
                    rutas = [rutas_por_indice[i] for i in seleccionadas if i in rutas_por_indice]
                    cantidad = actualizar_estados_archivos(rutas, "aprobada")
                    seleccionadas.clear()
                    for indice in range(len(registros)):
                        st.session_state[f"seleccionar_imagen_{indice}"] = False
                    st.success(f"Se aprobaron {cantidad} imágenes.")
                    st.rerun()
                if masiva_2.button("Marcar favoritas", disabled=not seleccionadas, key="favoritas_imagenes_masivo"):
                    rutas = [rutas_por_indice[i] for i in seleccionadas if i in rutas_por_indice]
                    cantidad = actualizar_estados_archivos(rutas, "favorita")
                    seleccionadas.clear()
                    for indice in range(len(registros)):
                        st.session_state[f"seleccionar_imagen_{indice}"] = False
                    st.success(f"Se marcaron {cantidad} imágenes como favoritas.")
                    st.rerun()
                if masiva_3.button("Rechazar seleccionadas", disabled=not seleccionadas, key="rechazar_imagenes_masivo"):
                    rutas = [rutas_por_indice[i] for i in seleccionadas if i in rutas_por_indice]
                    cantidad = actualizar_estados_archivos(rutas, "rechazada")
                    seleccionadas.clear()
                    for indice in range(len(registros)):
                        st.session_state[f"seleccionar_imagen_{indice}"] = False
                    st.success(f"Se rechazaron {cantidad} imágenes.")
                    st.rerun()

            columnas = st.columns(4)
            for posicion, (indice, registro) in enumerate(registros_filtrados):
                columna = columnas[posicion % len(columnas)]
                archivo = Path(rutas_por_indice[indice]) if indice in rutas_por_indice else None
                with columna.container(border=True):
                    st.checkbox(
                        "Seleccionar",
                        value=indice in seleccionadas,
                        key=f"seleccionar_imagen_{indice}",
                        label_visibility="collapsed",
                        on_change=actualizar_seleccion_imagen,
                        args=(indice,),
                    )
                    if archivo:
                        datos = (
                            f"Descripción: {registro.get('keyword') or 'Sin descripción'}\n"
                            f"Proveedor: {registro.get('proveedor', 'local')}\n"
                            f"Archivo: {registro.get('archivo', '')}\n"
                            f"Usos: {registro.get('usos', 0)}\n"
                            f"Estado: {registro.get('estado', 'pendiente')}"
                        )
                        if registro.get("url"):
                            datos += f"\nURL: {registro['url']}"
                        origen_imagen = escape(registro.get("keyword") or "Imagen de la biblioteca", quote=True)
                        st.markdown(
                            "<div class='image-gallery-card' tabindex='0'>"
                            f"<img src='{imagen_galeria_data_uri(archivo)}' alt='{origen_imagen}'>"
                            "<div class='image-metadata-tooltip'>"
                            + datos.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
                            + "</div></div>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.warning("Archivo no encontrado")
                    st.caption(f"Estado: {registro.get('estado', 'pendiente')} · Usos: {registro.get('usos', 0)}")
                    estado_actual = registro.get("estado", "pendiente")
                    estado = st.selectbox(
                        "Cambiar estado",
                        estados,
                        index=estados.index(estado_actual) if estado_actual in estados else 0,
                        key=f"estado_imagen_{indice}",
                    )
                    if st.button("Guardar estado", key=f"guardar_estado_{indice}"):
                        actualizar_estado(indice, estado)
                        st.success("Estado actualizado.")
