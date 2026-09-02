# Presentaciones

Generador de presentaciones academicas de alto impacto usando Python, Streamlit, python-pptx y Pexels.

## Instalacion en GitHub Codespaces

```bash
pip install -r requirements.txt
```

## Configuracion de Pexels

La aplicacion lee la clave desde la variable `PEXELS_API_KEY`.

En desarrollo local puedes usar el archivo `.env`.

```bash
PEXELS_API_KEY=tu_clave
```

## Ejecutar interfaz web

```bash
streamlit run app.py
```

## Generar desde terminal

```bash
python generar_desde_md.py ejemplos/redes_computadoras.md --salida salidas/redes_computadoras.pptx --estilo tecnologico_oscuro
```

## Uso

- Pega el Markdown de la clase.
- Selecciona estilo visual.
- Selecciona modo de imagen.
- Genera y descarga el archivo `.pptx`.

## Modos de imagen

- `pexels_o_diseno`: intenta Pexels y si falla crea diseno visual.
- `pexels`: intenta Pexels y si falla deja el area sin imagen.
- `solo_diseno`: no usa API, crea diseno visual.
- `sin_imagen`: genera solo contenido textual.

## Formato de entrada

Revisa `FORMATO_CLASE.md` y `ejemplos/redes_computadoras.md`.
