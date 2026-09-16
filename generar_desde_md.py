import argparse
from pathlib import Path

from dotenv import load_dotenv

from motor.exportadores import convertir_pptx_a_pdf, normalizar_salida_pptx
from motor.generador_clases import generar_presentacion
from motor.parser_markdown import parsear_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera una presentacion .pptx desde un archivo Markdown.")
    parser.add_argument("archivo", help="Ruta del archivo Markdown de entrada.")
    parser.add_argument("--salida", default="salidas/presentacion_clase.pptx", help="Ruta del archivo .pptx de salida.")
    parser.add_argument("--pdf", action="store_true", help="Genera tambien un PDF desde el PPTX usando LibreOffice headless.")
    parser.add_argument("--estilo", default=None, help="academico_formal, tecnologico_oscuro o alto_impacto.")
    parser.add_argument(
        "--modo-imagen",
        default="pexels_o_diseno",
        choices=["biblioteca_pexels_pixabay", "biblioteca_pexels", "pexels_pixabay", "pexels_o_diseno", "pexels", "pixabay", "solo_biblioteca", "solo_diseno", "sin_imagen"],
        help="Estrategia para insertar imagenes.",
    )
    parser.add_argument(
        "--distribucion",
        default="alternada",
        choices=["alternada", "fija", "aleatoria_controlada"],
        help="Estrategia de posicion para cada diapositiva.",
    )
    args = parser.parse_args()

    load_dotenv()
    markdown = Path(args.archivo).read_text(encoding="utf-8")
    clase = parsear_markdown(markdown)
    salida_pptx = normalizar_salida_pptx(Path(args.salida))
    salida = generar_presentacion(
        clase,
        salida_pptx,
        estilo_nombre=args.estilo,
        modo_imagen=args.modo_imagen,
        distribucion=args.distribucion,
    )
    print(f"Presentacion generada: {salida}")
    if args.pdf:
        resultado_pdf = convertir_pptx_a_pdf(salida)
        if resultado_pdf.ok:
            print(resultado_pdf.mensaje)
        else:
            print(f"Advertencia: {resultado_pdf.mensaje}")


if __name__ == "__main__":
    main()
