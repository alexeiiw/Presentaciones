from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from pptx import Presentation

from motor import biblioteca_imagenes, proveedores_imagenes
from motor.estilos import nombres_estilos
from motor.generador_clases import contar_diapositivas_estimadas, generar_presentacion
from motor.parser_markdown import parsear_markdown
from motor.validaciones import validar_clase
from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


class RespuestaFalsa:
    def __init__(self, data=None, content=b"imagen"):
        self._data = data or {}
        self.content = content

    def raise_for_status(self):
        return None

    def json(self):
        return self._data


class PruebasDeOperacion(unittest.TestCase):
    @contextmanager
    def _directorio_temporal(self, ruta: Path):
        anterior = Path.cwd()
        os.chdir(ruta)
        try:
            yield
        finally:
            os.chdir(anterior)

    def test_ejemplo_de_repositorio_pasa_revision_sin_errores(self):
        archivo = ROOT / "ejemplos" / "redes_computadoras.md"
        markdown = archivo.read_text(encoding="utf-8")
        clase = parsear_markdown(markdown)
        resultado = validar_clase(markdown, clase, ROOT)

        self.assertTrue(resultado.valido, resultado.errores)
        self.assertGreaterEqual(resultado.diapositivas_estimadas, len(clase.diapositivas))
        self.assertFalse(any("no parece tener una diapositiva desarrollada" in aviso for aviso in resultado.advertencias))
        self.assertFalse(any("no parece estar desarrollado" in aviso for aviso in resultado.advertencias))

    def test_validacion_distingue_errores_y_recomendaciones(self):
        markdown = """# Clase: Control de validación

Contenido Presentacion:
- Redes y seguridad

## Diapositiva: Inicio

Tipo: valor_inventado
"""
        resultado = validar_clase(markdown)
        self.assertFalse(resultado.valido)
        self.assertTrue(any("no soportado" in error for error in resultado.errores))
        self.assertTrue(any("no parece tener" in aviso for aviso in resultado.advertencias))

    def test_detecta_secciones_sin_desarrollo_y_bloques_sin_cierre(self):
        markdown = """# Clase: Secciones

## Diapositiva: Cambio de tema
Tipo: seccion

## Diapositiva: Segunda sección
Tipo: seccion

## Diapositiva: Código
Tipo: codigo
```python
print('hola')
"""
        resultado = validar_clase(markdown)
        self.assertTrue(any("no va seguida" in aviso for aviso in resultado.advertencias))
        self.assertTrue(any("sin cierre" in aviso for aviso in resultado.advertencias))
        self.assertTrue(resultado.valido)

    def test_parser_acepta_fechas_pendientes_y_codigo_sin_cierre(self):
        markdown = """# Clase: Parser

Fechas de Parciales:
- Parcial final: 30 de octubre

Qué queda pendiente:
- Revisar direccionamiento IPv6

## Diapositiva: Código
```python
print('fin')
"""
        clase = parsear_markdown(markdown)
        self.assertEqual(clase.fechas_parciales, ["Parcial final: 30 de octubre"])
        self.assertEqual(clase.pendientes, ["Revisar direccionamiento IPv6"])
        self.assertEqual(clase.diapositivas[0].codigo, "print('fin')")

    def test_generacion_cubre_layouts_y_cierre_en_todos_los_estilos(self):
        markdown = """# Clase: Suite de layouts
Agenda:
- Contexto
Contenido Presentacion:
- Componentes de red
Fechas Parciales:
- Parcial 1: 15 de octubre
Aprendizajes:
- Explicar componentes de red.
Qué queda pendiente:
- Estudiar enrutamiento avanzado.

## Diapositiva: Contenido general
Objetivo: Comprender la arquitectura.
Contenido:
- Un router conecta redes.
- Un switch conecta equipos.

## Diapositiva: Comparación
Tipo: columnas
Contenido:
- TCP prioriza fiabilidad.
- UDP prioriza baja latencia.

## Diapositiva: Camino de un paquete
Tipo: ruta
Contenido:
- Aplicación
- Transporte
- Red

## Diapositiva: Principio de red
Tipo: frase
Objetivo: Una red conecta equipos para intercambiar información.

## Diapositiva: Arquitectura
Tipo: diagrama
Diagrama: bloques
Contenido:
- Cliente: origina la solicitud.
- Router: conecta las redes.

## Diapositiva: Código
Tipo: codigo
```python
print('red')
```

## Diapositiva: Material de consulta
Tipo: repositorio
Contenido:
- Documentación técnica oficial.

## Diapositiva: Práctica previa heredada
Tipo: actividad
Contenido:
- Analizar una topología.
"""
        clase = parsear_markdown(markdown)
        with tempfile.TemporaryDirectory() as temporal:
            for estilo in nombres_estilos():
                salida = Path(temporal) / f"{estilo}.pptx"
                generar_presentacion(clase, salida, estilo_nombre=estilo, modo_imagen="sin_imagen")
                self.assertTrue(salida.exists(), estilo)
                presentacion = Presentation(salida)
                # Portada + agenda + índice + 8 diapositivas fuente + parcial + aprendizajes + pendientes.
                self.assertEqual(len(presentacion.slides), 14, estilo)
                titulos = [shape.text for slide in presentacion.slides for shape in slide.shapes if shape.has_text_frame]
                self.assertTrue(any("Suite de layouts" in titulo for titulo in titulos), estilo)
                self.assertTrue(any("Fechas de parciales" in titulo for titulo in titulos), estilo)
                self.assertTrue(any("Qué aprendiste" in titulo for titulo in titulos), estilo)
                self.assertTrue(any("Qué queda pendiente" in titulo for titulo in titulos), estilo)

    def test_generacion_funciona_desde_otro_directorio_y_resuelve_assets(self):
        markdown = """# Clase: Rutas independientes
Imagen Portada: images.jpg
Logo Portada: Umg.png

## Diapositiva: Prueba local
Tipo: contenido
Contenido:
- Las rutas resuelven desde la raíz del proyecto.
"""
        clase = parsear_markdown(markdown)
        with tempfile.TemporaryDirectory() as temporal:
            salida = Path(temporal) / "fuera_del_proyecto.pptx"
            with patch("pathlib.Path.cwd", return_value=Path(temporal)):
                generar_presentacion(clase, salida, modo_imagen="sin_imagen")
            presentacion = Presentation(salida)
            imagenes_incrustadas = [shape for slide in presentacion.slides for shape in slide.shapes if shape.shape_type == 13]
            self.assertEqual(len(imagenes_incrustadas), 2)

    def test_mismo_nombre_reemplaza_pptx_y_actualiza_contenido(self):
        salida = Path(tempfile.gettempdir()) / "presentaciones_test_reemplazo.pptx"
        try:
            for titulo in ("Primera versión", "Segunda versión"):
                clase = parsear_markdown(f"# Clase: {titulo}\n\n## Diapositiva: Tema\n\nContenido:\n- Punto\n")
                generar_presentacion(clase, salida, modo_imagen="sin_imagen")
                presentacion = Presentation(salida)
                textos = [shape.text for shape in presentacion.slides[0].shapes if shape.has_text_frame]
                self.assertIn(titulo, textos)
        finally:
            salida.unlink(missing_ok=True)

    def test_proveedores_no_reusan_resultados_agotados(self):
        usadas = set()
        fotos = [{"id": 101}, {"id": 202}]
        primera = proveedores_imagenes._elegir_no_usada(fotos, usadas, "pexels")
        segunda = proveedores_imagenes._elegir_no_usada(fotos, usadas, "pexels")
        tercera = proveedores_imagenes._elegir_no_usada(fotos, usadas, "pexels")
        self.assertIsNotNone(primera)
        self.assertIsNotNone(segunda)
        self.assertNotEqual(primera["id"], segunda["id"])
        self.assertIsNone(tercera)

    def test_busqueda_de_proveedor_entrega_imagen_unica(self):
        destino = Path(tempfile.gettempdir()) / "prueba_proveedor_presentaciones"
        usadas = set()
        respuesta_api = RespuestaFalsa({"photos": [
            {"id": 7, "src": {"large2x": "https://img/7.jpg"}},
            {"id": 8, "src": {"large2x": "https://img/8.jpg"}},
        ]})
        respuesta_img = RespuestaFalsa(content=b"fake-jpeg")
        try:
            with patch.dict("os.environ", {"PEXELS_API_KEY": "prueba"}), patch.object(
                proveedores_imagenes.requests, "get", side_effect=[respuesta_api, respuesta_img, respuesta_api, respuesta_img]
            ):
                primera = proveedores_imagenes.buscar_imagen_pexels("network router", destino, usadas)
                segunda = proveedores_imagenes.buscar_imagen_pexels("network router", destino, usadas)
            self.assertIsNotNone(primera)
            self.assertIsNotNone(segunda)
            self.assertNotEqual(primera[2], segunda[2])
            self.assertEqual(len(list(destino.glob("*.jpg"))), 2)
        finally:
            for imagen in destino.glob("*.jpg"):
                imagen.unlink()
            destino.rmdir() if destino.exists() else None

    def test_biblioteca_usa_rutas_estables_y_no_pierde_imagenes(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            origen = raiz / "origen.jpg"
            origen.write_bytes(b"test-image")
            with patch.multiple(
                biblioteca_imagenes,
                BASE_BIBLIOTECA=raiz / "biblioteca_imagenes",
                DIR_IMAGENES=raiz / "biblioteca_imagenes" / "imagenes",
                INDEX_PATH=raiz / "biblioteca_imagenes" / "index.json",
            ):
                imagen = biblioteca_imagenes.guardar_en_biblioteca("redes y seguridad", origen, "local")
                registro = biblioteca_imagenes.leer_index()[0]
                self.assertEqual(Path(registro["archivo"]).parts[0], "biblioteca_imagenes")
                self.assertTrue(imagen.exists())
                (raiz / "otro_directorio").mkdir()
                with self._directorio_temporal(raiz / "otro_directorio"):
                    seleccionada = biblioteca_imagenes.buscar_en_biblioteca("redes y seguridad")
                self.assertEqual(seleccionada, imagen.resolve())
                self.assertEqual(biblioteca_imagenes.buscar_en_biblioteca("redes y seguridad"), imagen.resolve())
                self.assertEqual(biblioteca_imagenes._normalizar_keyword("ciberseguridad y redes"), "ciberseguridad_y_redes")

    def test_interfaz_abre_valida_y_genera_con_el_flujo_normal(self):
        nombre_prueba = "prueba_interfaz_automatizada"
        salida = ROOT / "salidas" / f"{nombre_prueba}.pptx"
        previo = salida.read_bytes() if salida.exists() else None
        try:
            app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
            self.assertFalse(app.exception, [str(error.message) for error in app.exception])
            self.assertEqual(len(app.metric), 3)
            self.assertFalse(app.button[0].disabled)
            app.text_input[0].set_value(nombre_prueba).run()
            app.button[0].click().run()
            self.assertFalse(app.exception, [str(error.message) for error in app.exception])
            self.assertTrue(any("Presentacion generada" in aviso.value for aviso in app.success))
            self.assertTrue(salida.exists())
            self.assertTrue(Presentation(salida).slides)
            app.text_input[0].set_value("otro_nombre").run()
            self.assertTrue(any("configuración cambió" in aviso.value for aviso in app.info))
            self.assertFalse(any(boton.label.startswith("Descargar") for boton in app.button))
            app.text_input[0].set_value(nombre_prueba).run()
            self.assertTrue(any(boton.label == "Generar PDF desde este PPTX" for boton in app.button))
            app.button[0].click().run()
            self.assertTrue(any(boton.label == "Generar PDF desde este PPTX" for boton in app.button))
            app.selectbox[0].set_value("academico_formal").run()
            self.assertFalse(any(boton.label == "Descargar PPTX" for boton in app.button))
        finally:
            if previo is None:
                salida.unlink(missing_ok=True)
            else:
                salida.write_bytes(previo)

    def test_claves_locales_no_se_incluyen_en_el_diff_publicable(self):
        resultado = subprocess.run(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        archivos_cambiados = {linea[3:] for linea in resultado.stdout.splitlines() if len(linea) > 3}
        self.assertFalse(any("claves.txt" in archivo or archivo.endswith(".env") for archivo in archivos_cambiados))


if __name__ == "__main__":
    unittest.main()
