from pathlib import Path
import random
import re

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

from biblioteca_imagenes import buscar_en_biblioteca, guardar_en_biblioteca
from estilos import EstiloPresentacion, obtener_estilo
from parser_markdown import Clase, Diapositiva
from proveedores_imagenes import obtener_imagen, proveedores_desde_modo


ANCHO = Inches(13.333)
ALTO = Inches(7.5)


def generar_presentacion(
    clase: Clase,
    salida: Path,
    estilo_nombre: str | None = None,
    modo_imagen: str = "biblioteca_pexels_pixabay",
    distribucion: str = "alternada",
) -> Path:
    prs = Presentation()
    prs.slide_width = ANCHO
    prs.slide_height = ALTO
    estilo = obtener_estilo(estilo_nombre or clase.estilo)
    imagenes_usadas: set[str] = set()

    _crear_portada(prs, clase, estilo)
    for indice, diapositiva in enumerate(clase.diapositivas):
        imagen = _resolver_imagen(diapositiva.imagen, modo_imagen, imagenes_usadas)
        layout = _layout_para_diapositiva(indice, distribucion)

        if diapositiva.tipo == "codigo" or diapositiva.codigo:
            _crear_diapositiva_codigo(prs, diapositiva, estilo, imagen, modo_imagen, layout)
        else:
            _crear_diapositiva_contenido(prs, diapositiva, estilo, imagen, modo_imagen, layout)

    salida.parent.mkdir(parents=True, exist_ok=True)
    prs.save(salida)
    return salida


def _crear_portada(prs: Presentation, clase: Clase, estilo: EstiloPresentacion) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _pintar_fondo(slide, estilo.fondo)
    _agregar_banda_visual(slide, estilo)

    tam_titulo = 38 if len(clase.titulo) > 55 else 42
    _texto(slide, clase.titulo, Inches(0.8), Inches(1.35), Inches(8.15), Inches(2.6), tam_titulo, estilo.titulo, estilo.fuente_titulo, negrita=True)
    subtitulo = " | ".join(x for x in [clase.asignatura, clase.universidad] if x)
    if subtitulo:
        _texto(slide, subtitulo, Inches(0.85), Inches(4.15), Inches(7.7), Inches(0.8), 17, estilo.texto, estilo.fuente_texto)
    if clase.profesor:
        _texto(slide, clase.profesor, Inches(0.85), Inches(6.05), Inches(6.4), Inches(0.4), 16, estilo.acento, estilo.fuente_texto)


def _resolver_imagen(keyword: str, modo_imagen: str, imagenes_usadas: set[str]) -> Path | None:
    if not keyword or modo_imagen in {"solo_diseno", "sin_imagen"}:
        return None

    if "biblioteca" in modo_imagen:
        local = buscar_en_biblioteca(keyword, imagenes_usadas)
        if local:
            imagenes_usadas.add(str(local))
            return local

    proveedores = proveedores_desde_modo(modo_imagen)
    if not proveedores:
        return None

    resultado = obtener_imagen(keyword, Path("temp") / "imagenes", proveedores, imagenes_usadas)
    if not resultado:
        return None

    ruta, proveedor, url = resultado
    guardada = guardar_en_biblioteca(keyword, ruta, proveedor, url)
    imagenes_usadas.add(str(guardada))
    return guardada


def _layout_para_diapositiva(indice: int, distribucion: str) -> str:
    if distribucion == "fija":
        return "imagen_derecha"
    if distribucion == "aleatoria_controlada":
        return random.choice(["imagen_derecha", "imagen_izquierda"])
    return "imagen_izquierda" if indice % 2 else "imagen_derecha"


def _crear_diapositiva_contenido(prs: Presentation, d: Diapositiva, estilo: EstiloPresentacion, imagen: Path | None, modo_imagen: str, layout: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _pintar_fondo(slide, estilo.fondo)

    if layout == "imagen_izquierda":
        texto_x = Inches(5.85)
        imagen_x = Inches(0)
    else:
        texto_x = Inches(0.55)
        imagen_x = Inches(8.05)

    tam_titulo = 26 if len(d.titulo) > 42 else 30
    _texto(slide, d.titulo, texto_x, Inches(0.25), Inches(7.0), Inches(1.15), tam_titulo, estilo.titulo, estilo.fuente_titulo, negrita=True)
    _linea_acento(slide, estilo, texto_x, Inches(1.48), Inches(1.5))

    if imagen:
        _imagen_cover(slide, imagen, imagen_x, Inches(0.0), Inches(5.28), ALTO)
    elif modo_imagen in {"pexels_o_diseno", "solo_diseno", "biblioteca_pexels_pixabay", "biblioteca_pexels", "pexels_pixabay", "solo_biblioteca", "pixabay"}:
        _fallback_visual(slide, estilo, imagen_x, Inches(0.0), Inches(5.28), ALTO)

    y = Inches(1.72)
    if d.objetivo:
        _caja_objetivo(slide, d.objetivo, estilo, texto_x, y, Inches(6.9), Inches(0.9))
        y = Inches(2.82)

    _bullets(slide, d.contenido[:6], texto_x + Inches(0.2), y, Inches(6.55), Inches(3.95), estilo)


def _crear_diapositiva_codigo(prs: Presentation, d: Diapositiva, estilo: EstiloPresentacion, imagen: Path | None, modo_imagen: str, layout: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _pintar_fondo(slide, estilo.fondo)
    tam_titulo = 25 if len(d.titulo) > 48 else 28
    _texto(slide, d.titulo, Inches(0.55), Inches(0.25), Inches(9.0), Inches(1.05), tam_titulo, estilo.titulo, estilo.fuente_titulo, negrita=True)
    _linea_acento(slide, estilo, Inches(0.55), Inches(1.42), Inches(1.5))

    if d.objetivo:
        _texto(slide, d.objetivo, Inches(0.6), Inches(1.58), Inches(5.8), Inches(0.55), 14, estilo.texto, estilo.fuente_texto)

    codigo = d.codigo or "\n".join(d.contenido)
    _bloque_codigo(slide, codigo, estilo, Inches(0.6), Inches(2.25), Inches(7.1), Inches(4.55))

    if imagen:
        _imagen_cover(slide, imagen, Inches(8.2), Inches(1.35), Inches(4.65), Inches(5.45))
    elif modo_imagen in {"pexels_o_diseno", "solo_diseno", "biblioteca_pexels_pixabay", "biblioteca_pexels", "pexels_pixabay", "solo_biblioteca", "pixabay"}:
        _fallback_visual(slide, estilo, Inches(8.2), Inches(1.35), Inches(4.65), Inches(5.45))


def _pintar_fondo(slide, color: RGBColor) -> None:
    fondo = slide.background.fill
    fondo.solid()
    fondo.fore_color.rgb = color


def _agregar_banda_visual(slide, estilo: EstiloPresentacion) -> None:
    forma = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.1), 0, Inches(4.3), ALTO)
    forma.fill.solid()
    forma.fill.fore_color.rgb = estilo.fondo_secundario
    forma.line.fill.background()
    for i in range(5):
        barra = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.45 + i * 0.45), Inches(1.1 + i * 0.55), Inches(0.08), Inches(4.8 - i * 0.35))
        barra.fill.solid()
        barra.fill.fore_color.rgb = estilo.acento
        barra.line.fill.background()


def _linea_acento(slide, estilo: EstiloPresentacion, x, y, w) -> None:
    linea = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.06))
    linea.fill.solid()
    linea.fill.fore_color.rgb = estilo.acento
    linea.line.fill.background()


def _texto(slide, texto: str, x, y, w, h, tam: int, color: RGBColor, fuente: str, negrita: bool = False) -> None:
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = _limpiar_texto(texto)
    p.font.size = Pt(tam)
    p.font.color.rgb = color
    p.font.name = fuente
    p.font.bold = negrita


def _caja_objetivo(slide, objetivo: str, estilo: EstiloPresentacion, x, y, w, h) -> None:
    caja = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    caja.fill.solid()
    caja.fill.fore_color.rgb = estilo.caja
    caja.line.color.rgb = estilo.acento
    _texto(slide, f"Objetivo: {objetivo}", x + Inches(0.18), y + Inches(0.12), w - Inches(0.35), h - Inches(0.2), 13, estilo.texto, estilo.fuente_texto)


def _bullets(slide, bullets: list[str], x, y, w, h, estilo: EstiloPresentacion) -> None:
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.clear()
    for idx, item in enumerate(bullets):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = _limpiar_texto(item)
        p.level = 0
        p.font.size = Pt(18)
        p.font.name = estilo.fuente_texto
        p.font.color.rgb = estilo.texto
        p.space_after = Pt(8)


def _bloque_codigo(slide, codigo: str, estilo: EstiloPresentacion, x, y, w, h) -> None:
    caja = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    caja.fill.solid()
    caja.fill.fore_color.rgb = estilo.codigo_fondo
    caja.line.color.rgb = estilo.acento
    box = slide.shapes.add_textbox(x + Inches(0.22), y + Inches(0.18), w - Inches(0.44), h - Inches(0.36))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = _limpiar_texto(codigo[:1800])
    p.font.name = estilo.fuente_codigo
    p.font.size = Pt(13)
    p.font.color.rgb = estilo.codigo_texto


def _fallback_visual(slide, estilo: EstiloPresentacion, x, y, w, h) -> None:
    caja = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    caja.fill.solid()
    caja.fill.fore_color.rgb = estilo.fondo_secundario
    caja.line.fill.background()
    for i in range(6):
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.35 + i * 0.65), y + Inches(0.8 + i * 0.75), Inches(1.1), Inches(1.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = estilo.acento
        shape.fill.transparency = 0.45
        shape.line.fill.background()


def _imagen_cover(slide, ruta: Path, x, y, w, h) -> None:
    with Image.open(ruta) as img:
        img_w, img_h = img.size

    img_aspect = img_w / img_h
    box_aspect = w / h
    pic = slide.shapes.add_picture(str(ruta), x, y, width=w, height=h)

    if img_aspect > box_aspect:
        visible_w = box_aspect * img_h
        crop = max(0, (img_w - visible_w) / (2 * img_w))
        pic.crop_left = crop
        pic.crop_right = crop
    else:
        visible_h = img_w / box_aspect
        crop = max(0, (img_h - visible_h) / (2 * img_h))
        pic.crop_top = crop
        pic.crop_bottom = crop


def _limpiar_texto(texto: str) -> str:
    texto = texto.replace("\\(", "").replace("\\)", "")
    texto = texto.replace("**", "").replace("*", "")
    texto = re.sub(r"\\text\{([^}]*)\}", r"\1", texto)
    texto = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"\1 / \2", texto)
    texto = texto.replace("\\left", "").replace("\\right", "")
    texto = texto.replace("\\times", "x").replace("\\approx", "~")
    texto = texto.replace("\\eta", "eta").replace("\\mu", "micro")
    texto = texto.replace("\\", "")
    return texto
