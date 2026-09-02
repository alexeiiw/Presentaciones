from dataclasses import dataclass

from pptx.dml.color import RGBColor


@dataclass(frozen=True)
class EstiloPresentacion:
    nombre: str
    fondo: RGBColor
    fondo_secundario: RGBColor
    titulo: RGBColor
    texto: RGBColor
    acento: RGBColor
    caja: RGBColor
    codigo_fondo: RGBColor
    codigo_texto: RGBColor
    fuente_titulo: str
    fuente_texto: str
    fuente_codigo: str


ESTILOS = {
    "academico_formal": EstiloPresentacion(
        nombre="academico_formal",
        fondo=RGBColor(248, 249, 250),
        fondo_secundario=RGBColor(235, 239, 244),
        titulo=RGBColor(32, 45, 64),
        texto=RGBColor(45, 55, 72),
        acento=RGBColor(42, 91, 142),
        caja=RGBColor(255, 255, 255),
        codigo_fondo=RGBColor(31, 41, 55),
        codigo_texto=RGBColor(229, 231, 235),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "tecnologico_oscuro": EstiloPresentacion(
        nombre="tecnologico_oscuro",
        fondo=RGBColor(10, 18, 32),
        fondo_secundario=RGBColor(17, 34, 64),
        titulo=RGBColor(234, 246, 255),
        texto=RGBColor(203, 213, 225),
        acento=RGBColor(34, 211, 238),
        caja=RGBColor(15, 23, 42),
        codigo_fondo=RGBColor(2, 6, 23),
        codigo_texto=RGBColor(186, 230, 253),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "alto_impacto": EstiloPresentacion(
        nombre="alto_impacto",
        fondo=RGBColor(18, 18, 18),
        fondo_secundario=RGBColor(35, 35, 35),
        titulo=RGBColor(255, 255, 255),
        texto=RGBColor(240, 240, 240),
        acento=RGBColor(255, 184, 0),
        caja=RGBColor(25, 25, 25),
        codigo_fondo=RGBColor(0, 0, 0),
        codigo_texto=RGBColor(245, 245, 245),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
}


def obtener_estilo(nombre: str) -> EstiloPresentacion:
    return ESTILOS.get(nombre, ESTILOS["academico_formal"])
