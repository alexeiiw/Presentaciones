import json
import random
import re
from pathlib import Path
from shutil import copyfile


BASE_BIBLIOTECA = Path("biblioteca_imagenes")
DIR_IMAGENES = BASE_BIBLIOTECA / "imagenes"
INDEX_PATH = BASE_BIBLIOTECA / "index.json"


def buscar_en_biblioteca(keyword: str, usadas: set[str] | None = None) -> Path | None:
    usadas = usadas or set()
    registros = leer_index()
    normalizada = _normalizar_keyword(keyword)
    candidatas = [
        r
        for r in registros
        if r.get("keyword_normalizada") == normalizada
        and r.get("archivo") not in usadas
        and r.get("estado", "pendiente") != "rechazada"
    ]
    if not candidatas:
        return None

    prioridad = {"favorita": 0, "aprobada": 1, "pendiente": 2}
    candidatas.sort(key=lambda r: (prioridad.get(r.get("estado", "pendiente"), 2), r.get("usos", 0)))
    elegida = random.choice(candidatas[: min(3, len(candidatas))])
    elegida["usos"] = elegida.get("usos", 0) + 1
    guardar_index(registros)
    ruta = Path(elegida["archivo"])
    return ruta if ruta.exists() else None


def guardar_en_biblioteca(keyword: str, ruta_origen: Path, proveedor: str, url: str = "") -> Path:
    DIR_IMAGENES.mkdir(parents=True, exist_ok=True)
    registros = leer_index()
    normalizada = _normalizar_keyword(keyword)
    extension = ruta_origen.suffix.lower() or ".jpg"
    nombre = f"{normalizada}_{len(registros) + 1:04d}{extension}"
    destino = DIR_IMAGENES / nombre
    copyfile(ruta_origen, destino)

    registros.append(
        {
            "keyword": keyword,
            "keyword_normalizada": normalizada,
            "archivo": str(destino),
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
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def guardar_index(registros: list[dict]) -> None:
    BASE_BIBLIOTECA.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")


def actualizar_estado(indice: int, estado: str) -> None:
    registros = leer_index()
    if 0 <= indice < len(registros):
        registros[indice]["estado"] = estado
        guardar_index(registros)


def _normalizar_keyword(keyword: str) -> str:
    texto = keyword.lower().strip()
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_") or "imagen"
