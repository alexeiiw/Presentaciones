import json
import random
import re
import unicodedata
from pathlib import Path
from shutil import copyfile


BASE_BIBLIOTECA = Path(__file__).resolve().parents[1] / "biblioteca_imagenes"
DIR_IMAGENES = BASE_BIBLIOTECA / "imagenes"
INDEX_PATH = BASE_BIBLIOTECA / "index.json"


def buscar_en_biblioteca(keyword: str, usadas: set[str] | None = None) -> Path | None:
    if usadas is None:
        usadas = set()
    registros = leer_index()
    normalizada = _normalizar_keyword(keyword)
    candidatas = [
        r
        for r in registros
        if r.get("keyword_normalizada") == normalizada
        and str(_resolver_archivo(r.get("archivo", ""))) not in usadas
        and r.get("estado", "pendiente") != "rechazada"
    ]
    if not candidatas:
        return None

    prioridad = {"favorita": 0, "aprobada": 1, "pendiente": 2}
    candidatas.sort(key=lambda r: (prioridad.get(r.get("estado", "pendiente"), 2), r.get("usos", 0)))
    rutas_candidatas = {id(registro): _resolver_archivo(registro.get("archivo", "")) for registro in candidatas}
    candidatas = [registro for registro in candidatas if rutas_candidatas[id(registro)]]
    if not candidatas:
        return None
    elegida = random.choice(candidatas[: min(3, len(candidatas))])
    elegida["usos"] = elegida.get("usos", 0) + 1
    guardar_index(registros)
    return rutas_candidatas[id(elegida)]


def guardar_en_biblioteca(keyword: str, ruta_origen: Path, proveedor: str, url: str = "") -> Path:
    DIR_IMAGENES.mkdir(parents=True, exist_ok=True)
    registros = leer_index()
    normalizada = _normalizar_keyword(keyword)
    extension = ruta_origen.suffix.lower() or ".jpg"
    existentes = [
        int(match.group(1))
        for registro in registros
        if (match := re.search(r"_(\d+)(?:\.[^.]+)?$", Path(registro.get("archivo", "")).name))
    ]
    secuencia = max(existentes, default=0) + 1
    destino = DIR_IMAGENES / f"{normalizada}_{secuencia:04d}{extension}"
    while destino.exists():
        secuencia += 1
        destino = DIR_IMAGENES / f"{normalizada}_{secuencia:04d}{extension}"
    copyfile(ruta_origen, destino)

    registros.append(
        {
            "keyword": keyword,
            "keyword_normalizada": normalizada,
            "archivo": str(destino.relative_to(BASE_BIBLIOTECA.parent)),
            "proveedor": proveedor,
            "url": url,
            "usos": 1,
            "estado": "pendiente",
        }
    )
    guardar_index(registros)
    return destino


def leer_index() -> list[dict]:
    if not INDEX_PATH.exists():
        return []
    try:
        contenido = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        return contenido if isinstance(contenido, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def guardar_index(registros: list[dict]) -> None:
    BASE_BIBLIOTECA.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")


def actualizar_estado(indice: int, estado: str) -> None:
    registros = leer_index()
    if 0 <= indice < len(registros):
        registros[indice]["estado"] = estado
        guardar_index(registros)


def actualizar_estados(indices: list[int], estado: str) -> int:
    if estado not in {"pendiente", "aprobada", "favorita", "rechazada"}:
        raise ValueError(f"Estado de imagen no válido: {estado}")
    registros = leer_index()
    actualizados = 0
    for indice in set(indices):
        if 0 <= indice < len(registros):
            registros[indice]["estado"] = estado
            actualizados += 1
    if actualizados:
        guardar_index(registros)
    return actualizados


def actualizar_estados_archivos(archivos: list[str], estado: str) -> int:
    if estado not in {"pendiente", "aprobada", "favorita", "rechazada"}:
        raise ValueError(f"Estado de imagen no válido: {estado}")
    rutas_objetivo = {str(Path(archivo).resolve()) for archivo in archivos}
    registros = leer_index()
    actualizados = 0
    for registro in registros:
        ruta = _resolver_archivo(registro.get("archivo", ""))
        if ruta and str(ruta) in rutas_objetivo:
            registro["estado"] = estado
            actualizados += 1
    if actualizados:
        guardar_index(registros)
    return actualizados


def _normalizar_keyword(keyword: str) -> str:
    texto = unicodedata.normalize("NFKD", keyword.lower().strip())
    texto = "".join(caracter for caracter in texto if not unicodedata.combining(caracter))
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_") or "imagen"


def _resolver_archivo(valor: str) -> Path | None:
    ruta = Path(valor)
    candidatas = [ruta] if ruta.is_absolute() else [BASE_BIBLIOTECA.parent / ruta, BASE_BIBLIOTECA / ruta.name]
    return next((c.resolve() for c in candidatas if c.exists() and c.is_file()), None)
