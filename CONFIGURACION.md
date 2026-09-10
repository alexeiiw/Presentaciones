# Configuracion de claves

El proyecto usa variables de entorno para las claves de proveedores de imagenes.

## Archivo local recomendado

Crea un archivo llamado `.env` en la raiz del proyecto con este contenido:

```bash
PEXELS_API_KEY=tu_clave_de_pexels
PIXABAY_API_KEY=tu_clave_de_pixabay
```

El archivo `.env` esta ignorado por Git y no se sube al repositorio.

Tambien se ignora cualquier archivo llamado `claves.txt`. Si prefieres guardar notas locales de claves, usa ese nombre y no se subira a GitHub.

## Alternativa en Codespaces

Tambien puedes exportar las claves en la terminal:

```bash
export PEXELS_API_KEY="tu_clave_de_pexels"
export PIXABAY_API_KEY="tu_clave_de_pixabay"
python3 -m streamlit run app.py
```

## Alternativa en la interfaz

La barra lateral de Streamlit permite pegar `PEXELS_API_KEY` y `PIXABAY_API_KEY` para la sesion actual.

## Exportacion a PDF con LibreOffice

La aplicacion genera PPTX con `python-pptx`. Para convertir ese PPTX a PDF sin Microsoft PowerPoint, usa LibreOffice en modo headless.

En GitHub Codespaces instala LibreOffice asi:

```bash
sudo apt-get update
sudo apt-get install -y libreoffice
libreoffice --version
```

Uso manual de referencia:

```bash
libreoffice --headless --convert-to pdf --outdir salidas salidas/presentacion_clase.pptx
```

Notas operativas:

- El PPTX se genera primero y no depende de LibreOffice.
- El PDF se crea despues desde el PPTX generado.
- Si LibreOffice no esta instalado, la aplicacion conserva el PPTX y muestra una advertencia.
- Revisa visualmente el PDF antes de publicarlo, porque la fidelidad puede variar levemente respecto a PowerPoint.
- Los PDF generados en `salidas/` estan excluidos de Git por defecto.
