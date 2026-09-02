# Formato Markdown de la clase

Usa este formato para pegar el contenido en la interfaz web.

````markdown
# Clase: Titulo de la clase

Profesor: Nombre del profesor
Asignatura: Nombre de la asignatura
Universidad: Nombre de la universidad
Estilo: tecnologico_oscuro

## Diapositiva: Titulo de la diapositiva

Objetivo: Objetivo pedagogico de esta diapositiva.

Contenido:
- Primer punto clave.
- Segundo punto clave.
- Tercer punto clave.

Imagen: english image keyword

## Diapositiva: Ejemplo con codigo

Tipo: codigo

Objetivo: Explicar el objetivo del codigo.

```python
def ejemplo():
    return "Hola clase"
```

Imagen: programming code
````

## Reglas

- `# Clase:` define el titulo de la presentacion.
- `Estilo:` puede ser `academico_formal`, `tecnologico_oscuro` o `alto_impacto`.
- Cada diapositiva empieza con `## Diapositiva:`.
- `Objetivo:` es opcional, pero recomendado.
- `Contenido:` contiene bullets iniciados con `-`.
- `Imagen:` debe escribirse preferiblemente en ingles para mejorar la busqueda en Pexels.
- `Tipo: codigo` activa una diapositiva con bloque de codigo.
- Si Pexels falla o no hay API key, el sistema genera la diapositiva con diseno alternativo.
