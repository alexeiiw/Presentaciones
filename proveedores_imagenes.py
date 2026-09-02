import os
from pathlib import Path
from uuid import uuid4

import requests


class ErrorImagen(Exception):
    pass


def buscar_imagen_pexels(query: str, destino: Path) -> Path | None:
    api_key = os.getenv("PEXELS_API_KEY", "").strip()
    if not api_key or not query:
        return None

    destino.mkdir(parents=True, exist_ok=True)
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}

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

        url = fotos[0]["src"].get("large2x") or fotos[0]["src"].get("large")
        if not url:
            return None

        imagen = requests.get(url, timeout=20)
        imagen.raise_for_status()
        ruta = destino / f"pexels_{uuid4().hex}.jpg"
        ruta.write_bytes(imagen.content)
        return ruta
    except requests.RequestException:
        return None
    except (KeyError, ValueError):
        return None


def obtener_imagen(query: str, destino: Path, proveedor: str = "pexels") -> Path | None:
    if proveedor == "pexels":
        return buscar_imagen_pexels(query, destino)
    return None
