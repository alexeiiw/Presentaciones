# Configuracion de claves

El proyecto usa variables de entorno para las claves de proveedores de imagenes.

## Archivo local recomendado

Crea un archivo llamado `.env` en la raiz del proyecto con este contenido:

```bash
PEXELS_API_KEY=tu_clave_de_pexels
PIXABAY_API_KEY=tu_clave_de_pixabay
```

El archivo `.env` esta ignorado por Git y no se sube al repositorio.

## Alternativa en Codespaces

Tambien puedes exportar las claves en la terminal:

```bash
export PEXELS_API_KEY="tu_clave_de_pexels"
export PIXABAY_API_KEY="tu_clave_de_pixabay"
python3 -m streamlit run app.py
```

## Alternativa en la interfaz

La barra lateral de Streamlit permite pegar `PEXELS_API_KEY` y `PIXABAY_API_KEY` para la sesion actual.
