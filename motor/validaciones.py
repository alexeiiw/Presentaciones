from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

from .parser_markdown import Clase


TIPOS_SOPORTADOS = {
    "contenido",
    "codigo",
    "columnas",
    "ruta",
    "frase",
    "seccion",
    "diagrama",
    "actividad",
    "repositorio",
}
DIAGRAMAS_SOPORTADOS = {
    "cdn", "content delivery network", "flujo", "flow", "flowchart", "secuencia", "sequence",
    "bloques", "bloque", "block", "blocks", "casos de uso", "caso de uso", "use case", "use cases",
    "arquitectura", "topologia", "protocolo", "mapa conceptual",
}


@dataclass
class ResultadoValidacion:
    errores: list[str] = field(default_factory=list)
    advertencias: list[str] = field(default_factory=list)
    diapositivas_estimadas: int = 0
    diapositivas_contenido: int = 0
    imagenes_locales: int = 0
    imagenes_no_encontradas: list[str] = field(default_factory=list)

    @property
    def valido(self) -> bool:
        return not self.errores


def validar_clase(markdown: str, clase: Clase | None = None, directorio_base: Path | None = None) -> ResultadoValidacion:
    from .parser_markdown import parsear_markdown

    clase = clase or parsear_markdown(markdown)
    resultado = ResultadoValidacion(diapositivas_contenido=len(clase.diapositivas))
    base = Path(directorio_base) if directorio_base else Path.cwd()
    lineas = markdown.splitlines()

    if not clase.titulo.strip() or clase.titulo == "Presentacion academica":
        resultado.advertencias.append("Agrega un título de clase descriptivo.")
    if not clase.diapositivas:
        resultado.errores.append("No se encontraron diapositivas. Usa al menos un encabezado '## Diapositiva: Título'.")

    titulos: dict[str, int] = {}
    for indice, diapositiva in enumerate(clase.diapositivas, start=1):
        titulo = diapositiva.titulo.strip()
        if not titulo:
            resultado.errores.append(f"La diapositiva {indice} no tiene título.")
        llave = titulo.casefold()
        titulos[llave] = titulos.get(llave, 0) + 1
        if diapositiva.tipo not in TIPOS_SOPORTADOS:
            resultado.errores.append(f"Diapositiva {indice} ('{titulo}'): tipo '{diapositiva.tipo}' no soportado.")
        if diapositiva.tipo == "diagrama" and diapositiva.diagrama and diapositiva.diagrama not in DIAGRAMAS_SOPORTADOS:
            resultado.advertencias.append(
                f"Diapositiva {indice} ('{titulo}'): diagrama '{diapositiva.diagrama}' no reconocido; se usará el mapa conceptual."
            )
        if diapositiva.tipo != "seccion" and not diapositiva.objetivo and not diapositiva.contenido and not diapositiva.codigo:
            resultado.advertencias.append(f"Diapositiva {indice} ('{titulo}') no tiene contenido y se mostrará como separador.")
        if diapositiva.tipo == "seccion" and indice < len(clase.diapositivas):
            siguiente = clase.diapositivas[indice]
            if siguiente.tipo == "seccion" or (
                not siguiente.contenido and not siguiente.objetivo and not siguiente.codigo
            ):
                resultado.advertencias.append(
                    f"La sección '{titulo}' no va seguida inmediatamente por una diapositiva desarrollada."
                )
        if len(diapositiva.contenido) > 6 and diapositiva.tipo not in {"diagrama", "repositorio", "actividad"}:
            resultado.advertencias.append(f"Diapositiva {indice} ('{titulo}') tiene más de 6 bullets; revisa densidad y legibilidad.")
        if len(diapositiva.contenido) > 7 and diapositiva.tipo == "diagrama":
            resultado.advertencias.append(f"Diapositiva {indice} ('{titulo}') tiene más de 7 nodos de diagrama.")
        if diapositiva.tipo == "codigo" and not diapositiva.codigo and not diapositiva.contenido:
            resultado.errores.append(f"Diapositiva {indice} ('{titulo}') es de código pero no contiene código.")
        if diapositiva.tipo == "ruta" and not diapositiva.contenido:
            resultado.advertencias.append(f"Diapositiva {indice} ('{titulo}') usa una ruta sin pasos; agrega de 3 a 5.")
        if diapositiva.tipo == "columnas" and len(diapositiva.contenido) < 2:
            resultado.advertencias.append(f"Diapositiva {indice} ('{titulo}') necesita al menos dos puntos para comparar.")
        if diapositiva.imagen:
            ruta = _resolver_imagen_local(diapositiva.imagen, base)
            if ruta:
                resultado.imagenes_locales += 1
            elif _parece_ruta_local(diapositiva.imagen):
                resultado.imagenes_no_encontradas.append(diapositiva.imagen)

    for titulo, cantidad in titulos.items():
        if cantidad > 1:
            resultado.advertencias.append(f"El título '{titulo}' se repite en {cantidad} diapositivas.")

    for campo in (clase.imagen_universidad, clase.logo_portada):
        if campo and _parece_ruta_local(campo):
            ruta = _resolver_imagen_local(campo, base)
            if ruta:
                resultado.imagenes_locales += 1
            else:
                resultado.imagenes_no_encontradas.append(campo)

    if resultado.imagenes_no_encontradas:
        lista = ", ".join(f"'{valor}'" for valor in resultado.imagenes_no_encontradas)
        resultado.advertencias.append(f"No se encontraron estas imágenes locales: {lista}.")
    if any(linea.strip().startswith("```") for linea in lineas) and sum(
        1 for linea in lineas if linea.strip().startswith("```")
    ) % 2:
        resultado.advertencias.append("Hay un bloque de código sin cierre de triple acento grave; se capturará hasta el final.")

    agenda = _normalizar_items(clase.agenda)
    contenido = _normalizar_items(clase.contenido_presentacion)
    desarrollados = [
        _normalizar_tema(titulo)
        for diapositiva in clase.diapositivas
        if diapositiva.tipo != "seccion"
        for titulo in [diapositiva.titulo, *diapositiva.contenido]
    ]
    if clase.fechas_parciales:
        desarrollados.append(_normalizar_tema("Fechas de parciales"))
        desarrollados.extend(_normalizar_items(clase.fechas_parciales))
    if clase.aprendizajes or clase.frase_final:
        desarrollados.append(_normalizar_tema("Qué aprendiste"))
        desarrollados.extend(_normalizar_items(clase.aprendizajes))
    if clase.pendientes:
        desarrollados.append(_normalizar_tema("Qué queda pendiente"))
        desarrollados.extend(_normalizar_items(clase.pendientes))
    titulos_estructura = [_normalizar_tema(d.titulo) for d in clase.diapositivas]
    titulos_estructura.extend(
        _normalizar_tema(titulo)
        for titulo in (
            "Agenda de la clase",
            "Contenido de la presentacion",
            "Fechas de parciales",
            "Qué aprendiste",
            "Qué queda pendiente",
            "sintesis final",
            "sintesis conceptual y cierre",
        )
    )
    titulos_estructura.extend(_normalizar_tema(tema) for tema in clase.agenda)
    for bloque in contenido:
        if not _tema_desarrollado(bloque, desarrollados) and not _tema_desarrollado(bloque, titulos_estructura):
            resultado.advertencias.append(f"El bloque '{bloque}' de Contenido Presentacion no parece tener una diapositiva desarrollada.")
    for tema in agenda:
        if not _tema_desarrollado(tema, desarrollados) and not _tema_desarrollado(tema, titulos_estructura):
            resultado.advertencias.append(f"El tema de agenda '{tema}' no parece estar desarrollado en las diapositivas.")

    if not clase.fechas_parciales and not any(
        d.titulo.casefold().startswith("fechas de parciales") for d in clase.diapositivas
    ):
        resultado.advertencias.append("No se definieron fechas de parciales. Si no aplican a esta clase, puedes ignorar esta advertencia.")
    if not clase.aprendizajes:
        resultado.advertencias.append("No se definió la sección Aprendizajes; el cierre se inferirá de los títulos de diapositiva.")
    if not clase.pendientes and not any(
        d.titulo.casefold().startswith(("qué queda pendiente", "que queda pendiente")) for d in clase.diapositivas
    ):
        resultado.advertencias.append("No se definió Qué queda pendiente; puedes agregarla si aplica al avance del curso.")

    avanzada = sum(1 for d in clase.diapositivas if d.tipo in {"columnas", "ruta", "diagrama"})
    if len(clase.diapositivas) >= 10 and avanzada < max(2, len(clase.diapositivas) // 10 * 2):
        resultado.advertencias.append("Hay pocos layouts visuales avanzados para la cantidad de diapositivas; considera agregar comparativas, rutas o diagramas.")

    resultado.diapositivas_estimadas = (
        1
        + (len(clase.agenda) + 6) // 7
        + (len(clase.contenido_presentacion or [d.titulo for d in clase.diapositivas]) + 9) // 10
        + len(clase.diapositivas)
        + int(bool(clase.aprendizajes or clase.frase_final or clase.diapositivas))
        + int(bool(clase.fechas_parciales))
        + (len(clase.pendientes) + 6) // 7
    )
    return resultado


def _normalizar_items(items: list[str]) -> list[str]:
    return [_normalizar_tema(item) for item in items if item.strip()]


def _normalizar_tema(texto: str) -> str:
    texto = texto.casefold()
    texto = re.sub(r"^(?:bloque|tema|unidad)\s+\w+\s*[:.-]\s*", "", texto)
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(caracter for caracter in texto if not unicodedata.combining(caracter))
    return re.sub(r"[^a-z0-9]+", " ", texto).strip()


def _tema_desarrollado(tema: str, desarrollados: list[str]) -> bool:
    normalizado = _normalizar_tema(tema)
    if not normalizado:
        return True
    palabras = [p for p in normalizado.split() if len(p) > 2]
    for desarrollado in desarrollados:
        if normalizado in desarrollado or desarrollado in normalizado:
            return True
        palabras_desarrolladas = set(desarrollado.split())
        coincidencias = sum(palabra in palabras_desarrolladas for palabra in palabras)
        if len(palabras) <= 3 and coincidencias >= min(2, len(palabras)):
            return True
        if len(palabras) > 3 and (
            coincidencias / len(palabras) >= 0.5 or SequenceMatcher(None, normalizado, desarrollado).ratio() >= 0.55
        ):
            return True
    return False


def _parece_ruta_local(valor: str) -> bool:
    return bool(Path(valor.strip().strip('"')).suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".bmp"})


def _resolver_imagen_local(valor: str, base: Path) -> Path | None:
    ruta = Path(valor.strip().strip('"'))
    raiz_proyecto = Path(__file__).resolve().parents[1]
    candidatas = [ruta] if ruta.is_absolute() else [base / ruta, base / "assets" / ruta.name, raiz_proyecto / ruta, raiz_proyecto / "assets" / ruta.name]
    return next((c.resolve() for c in candidatas if c.exists() and c.is_file()), None)
