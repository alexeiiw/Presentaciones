import os
import random
from pathlib import Path
from uuid import uuid4

import requests


class ErrorImagen(Exception):
    pass


def buscar_imagen_pexels(query: str, destino: Path, usadas: set[str] | None = None) -> tuple[Path, str, str] | None:
    api_key = os.getenv("PEXELS_API_KEY", "").strip()
    if not api_key or not query:
        return None

    destino.mkdir(parents=True, exist_ok=True)
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": 15, "orientation": "landscape"}

    try:
        respuesta = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=15,
        )
        respuesta.raise_for_status()
        data = respuesta.json()
        fotos = data.get("photos", [])
        if not fotos:
            return None

        random.shuffle(fotos)
        foto = _elegir_no_usada(fotos, usadas)
        url = foto["src"].get("large2x") or foto["src"].get("large")
        if not url:
            return None

        imagen = requests.get(url, timeout=20)
        imagen.raise_for_status()
        ruta = destino / f"pexels_{uuid4().hex}.jpg"
        ruta.write_bytes(imagen.content)
        return ruta, "pexels", url
    except requests.RequestException:
        return None
    except (KeyError, ValueError):
        return None


def buscar_imagen_pixabay(query: str, destino: Path, usadas: set[str] | None = None) -> tuple[Path, str, str] | None:
    api_key = os.getenv("PIXABAY_API_KEY", "").strip()
    if not api_key or not query:
        return None

    destino.mkdir(parents=True, exist_ok=True)
    params = {
        "key": api_key,
        "q": query,
        "image_type": "photo",
        "orientation": "horizontal",
        "per_page": 20,
        "safesearch": "true",
    }

    try:
        respuesta = requests.get("https://pixabay.com/api/", params=params, timeout=15)
        respuesta.raise_for_status()
        data = respuesta.json()
        fotos = data.get("hits", [])
        if not fotos:
            return None

        random.shuffle(fotos)
        foto = _elegir_no_usada(fotos, usadas, campo_id="largeImageURL")
        url = foto.get("largeImageURL") or foto.get("webformatURL")
        if not url:
            return None

        imagen = requests.get(url, timeout=20)
        imagen.raise_for_status()
        ruta = destino / f"pixabay_{uuid4().hex}.jpg"
        ruta.write_bytes(imagen.content)
        return ruta, "pixabay", url
    except requests.RequestException:
        return None
    except (KeyError, ValueError):
        return None


def obtener_imagen(query: str, destino: Path, proveedores: list[str], usadas: set[str] | None = None) -> tuple[Path, str, str] | None:
    for proveedor in proveedores:
        if proveedor == "pexels":
            resultado = buscar_imagen_pexels(query, destino, usadas)
        elif proveedor == "pixabay":
            resultado = buscar_imagen_pixabay(query, destino, usadas)
        else:
            resultado = None
        if resultado:
            return resultado
    return None


def proveedores_desde_modo(modo_imagen: str) -> list[str]:
    if "pexels_pixabay" in modo_imagen:
        return ["pexels", "pixabay"]
    if "pixabay" in modo_imagen:
        return ["pixabay"]
    if "pexels" in modo_imagen:
        return ["pexels"]
    return []


def _elegir_no_usada(fotos: list[dict], usadas: set[str] | None, campo_id: str = "url") -> dict:
    usadas = usadas or set()
    for foto in fotos:
        identificador = str(foto.get(campo_id) or foto.get("id") or "")
        if identificador and identificador not in usadas:
            usadas.add(identificador)
            return foto
    return fotos[0]
