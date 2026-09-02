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
    "ingenieria_codigo": EstiloPresentacion(
        nombre="ingenieria_codigo",
        fondo=RGBColor(12, 16, 24),
        fondo_secundario=RGBColor(24, 31, 45),
        titulo=RGBColor(230, 237, 243),
        texto=RGBColor(201, 209, 217),
        acento=RGBColor(63, 185, 80),
        caja=RGBColor(22, 27, 34),
        codigo_fondo=RGBColor(1, 4, 9),
        codigo_texto=RGBColor(125, 211, 252),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "pizarra_matematica": EstiloPresentacion(
        nombre="pizarra_matematica",
        fondo=RGBColor(19, 46, 38),
        fondo_secundario=RGBColor(29, 78, 63),
        titulo=RGBColor(245, 245, 220),
        texto=RGBColor(235, 241, 222),
        acento=RGBColor(245, 203, 92),
        caja=RGBColor(23, 63, 52),
        codigo_fondo=RGBColor(10, 35, 29),
        codigo_texto=RGBColor(245, 245, 220),
        fuente_titulo="Georgia",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "laboratorio_redes": EstiloPresentacion(
        nombre="laboratorio_redes",
        fondo=RGBColor(239, 246, 255),
        fondo_secundario=RGBColor(219, 234, 254),
        titulo=RGBColor(15, 23, 42),
        texto=RGBColor(30, 41, 59),
        acento=RGBColor(37, 99, 235),
        caja=RGBColor(255, 255, 255),
        codigo_fondo=RGBColor(15, 23, 42),
        codigo_texto=RGBColor(191, 219, 254),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "ciberseguridad": EstiloPresentacion(
        nombre="ciberseguridad",
        fondo=RGBColor(8, 13, 10),
        fondo_secundario=RGBColor(12, 26, 18),
        titulo=RGBColor(220, 252, 231),
        texto=RGBColor(187, 247, 208),
        acento=RGBColor(34, 197, 94),
        caja=RGBColor(5, 20, 12),
        codigo_fondo=RGBColor(0, 0, 0),
        codigo_texto=RGBColor(74, 222, 128),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "minimalista_claro": EstiloPresentacion(
        nombre="minimalista_claro",
        fondo=RGBColor(255, 255, 255),
        fondo_secundario=RGBColor(245, 245, 245),
        titulo=RGBColor(24, 24, 27),
        texto=RGBColor(63, 63, 70),
        acento=RGBColor(82, 82, 91),
        caja=RGBColor(250, 250, 250),
        codigo_fondo=RGBColor(39, 39, 42),
        codigo_texto=RGBColor(244, 244, 245),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "universitario_elegante": EstiloPresentacion(
        nombre="universitario_elegante",
        fondo=RGBColor(250, 248, 244),
        fondo_secundario=RGBColor(232, 226, 214),
        titulo=RGBColor(32, 32, 32),
        texto=RGBColor(64, 64, 64),
        acento=RGBColor(0, 136, 170),
        caja=RGBColor(255, 255, 255),
        codigo_fondo=RGBColor(35, 35, 35),
        codigo_texto=RGBColor(245, 245, 245),
        fuente_titulo="Georgia",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "seminario_ejecutivo": EstiloPresentacion(
        nombre="seminario_ejecutivo",
        fondo=RGBColor(246, 247, 251),
        fondo_secundario=RGBColor(226, 232, 240),
        titulo=RGBColor(15, 23, 42),
        texto=RGBColor(51, 65, 85),
        acento=RGBColor(124, 58, 237),
        caja=RGBColor(255, 255, 255),
        codigo_fondo=RGBColor(30, 41, 59),
        codigo_texto=RGBColor(226, 232, 240),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "taller_practico": EstiloPresentacion(
        nombre="taller_practico",
        fondo=RGBColor(255, 251, 235),
        fondo_secundario=RGBColor(254, 243, 199),
        titulo=RGBColor(69, 26, 3),
        texto=RGBColor(92, 45, 10),
        acento=RGBColor(234, 88, 12),
        caja=RGBColor(255, 255, 255),
        codigo_fondo=RGBColor(67, 20, 7),
        codigo_texto=RGBColor(254, 215, 170),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "modo_examen": EstiloPresentacion(
        nombre="modo_examen",
        fondo=RGBColor(248, 250, 252),
        fondo_secundario=RGBColor(226, 232, 240),
        titulo=RGBColor(127, 29, 29),
        texto=RGBColor(31, 41, 55),
        acento=RGBColor(220, 38, 38),
        caja=RGBColor(255, 255, 255),
        codigo_fondo=RGBColor(31, 41, 55),
        codigo_texto=RGBColor(254, 226, 226),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
    "clase_visual": EstiloPresentacion(
        nombre="clase_visual",
        fondo=RGBColor(17, 24, 39),
        fondo_secundario=RGBColor(31, 41, 55),
        titulo=RGBColor(255, 255, 255),
        texto=RGBColor(229, 231, 235),
        acento=RGBColor(251, 146, 60),
        caja=RGBColor(24, 24, 27),
        codigo_fondo=RGBColor(0, 0, 0),
        codigo_texto=RGBColor(253, 186, 116),
        fuente_titulo="Aptos Display",
        fuente_texto="Aptos",
        fuente_codigo="Consolas",
    ),
}


def nombres_estilos() -> list[str]:
    return list(ESTILOS.keys())


def obtener_estilo(nombre: str) -> EstiloPresentacion:
    return ESTILOS.get(nombre, ESTILOS["academico_formal"])
