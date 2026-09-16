from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ResultadoExportacion:
    formato: str
    ruta: Path | None
    ok: bool
    mensaje: str


def detectar_libreoffice() -> str | None:
    for comando in ("libreoffice", "soffice"):
        ruta = shutil.which(comando)
        if ruta:
            return ruta
    return None


def convertir_pptx_a_pdf(pptx: Path, salida_pdf: Path | None = None) -> ResultadoExportacion:
    pptx = Path(pptx)
    if not pptx.exists():
        return ResultadoExportacion("pdf", None, False, f"No existe el PPTX base: {pptx}")

    comando = detectar_libreoffice()
    if not comando:
        return ResultadoExportacion(
            "pdf",
            None,
            False,
            "LibreOffice no esta instalado o no esta disponible en PATH. El PPTX sigue disponible.",
        )

    salida_pdf = Path(salida_pdf) if salida_pdf else pptx.with_suffix(".pdf")
    salida_pdf.parent.mkdir(parents=True, exist_ok=True)

    try:
        proceso = subprocess.run(
            [
                comando,
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(salida_pdf.parent),
                str(pptx),
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return ResultadoExportacion("pdf", None, False, "LibreOffice tardo demasiado en convertir el PDF. El PPTX sigue disponible.")
    except OSError as exc:
        return ResultadoExportacion("pdf", None, False, f"No se pudo ejecutar LibreOffice: {exc}")

    generado = salida_pdf.parent / f"{pptx.stem}.pdf"
    if generado.exists() and generado != salida_pdf:
        if salida_pdf.exists():
            salida_pdf.unlink()
        generado.replace(salida_pdf)

    if proceso.returncode != 0 or not salida_pdf.exists():
        detalle = (proceso.stderr or proceso.stdout or "Error desconocido de LibreOffice").strip()
        return ResultadoExportacion("pdf", None, False, f"No se pudo generar PDF: {detalle}")

    return ResultadoExportacion("pdf", salida_pdf, True, f"PDF generado: {salida_pdf}")


def normalizar_salida_pptx(salida: Path) -> Path:
    salida = Path(salida)
    if salida.suffix.lower() != ".pptx":
        salida = salida.with_suffix(".pptx")
    return salida
