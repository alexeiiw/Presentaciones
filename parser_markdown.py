from dataclasses import dataclass, field


@dataclass
class Diapositiva:
    titulo: str
    objetivo: str = ""
    contenido: list[str] = field(default_factory=list)
    imagen: str = ""
    tipo: str = "contenido"
    codigo: str = ""
    lenguaje: str = ""


@dataclass
class Clase:
    titulo: str = "Presentacion academica"
    profesor: str = ""
    asignatura: str = ""
    universidad: str = ""
    estilo: str = "academico_formal"
    diapositivas: list[Diapositiva] = field(default_factory=list)


def parsear_markdown(texto: str) -> Clase:
    clase = Clase()
    actual: Diapositiva | None = None
    leyendo_contenido = False
    leyendo_codigo = False
    codigo_lineas: list[str] = []

    for linea_original in texto.splitlines():
        linea = linea_original.strip()

        if leyendo_codigo:
            if linea.startswith("```"):
                leyendo_codigo = False
                if actual:
                    actual.codigo = "\n".join(codigo_lineas).strip()
                    actual.tipo = "codigo"
                codigo_lineas = []
                continue
            codigo_lineas.append(linea_original)
            continue

        if not linea:
            continue

        if linea.startswith("# Clase:"):
            clase.titulo = linea.split(":", 1)[1].strip()
            continue
        if linea.startswith("Profesor:"):
            clase.profesor = linea.split(":", 1)[1].strip()
            continue
        if linea.startswith("Asignatura:"):
            clase.asignatura = linea.split(":", 1)[1].strip()
            continue
        if linea.startswith("Universidad:"):
            clase.universidad = linea.split(":", 1)[1].strip()
            continue
        if linea.startswith("Estilo:"):
            clase.estilo = linea.split(":", 1)[1].strip()
            continue

        if linea.startswith("## Diapositiva:"):
            actual = Diapositiva(titulo=linea.split(":", 1)[1].strip())
            clase.diapositivas.append(actual)
            leyendo_contenido = False
            continue

        if not actual:
            continue

        if linea.startswith("Tipo:"):
            actual.tipo = linea.split(":", 1)[1].strip().lower()
            continue
        if linea.startswith("Objetivo:"):
            actual.objetivo = linea.split(":", 1)[1].strip()
            leyendo_contenido = False
            continue
        if linea.startswith("Imagen:"):
            actual.imagen = linea.split(":", 1)[1].strip()
            leyendo_contenido = False
            continue
        if linea.startswith("Contenido:"):
            leyendo_contenido = True
            continue
        if linea.startswith("```"):
            leyendo_codigo = True
            actual.lenguaje = linea.replace("```", "").strip()
            codigo_lineas = []
            continue
        if leyendo_contenido and linea.startswith("-"):
            actual.contenido.append(linea[1:].strip())

    return clase
