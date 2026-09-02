# Formato Markdown de la clase

Usa este formato para pegar el contenido en la interfaz web.

````markdown
# Clase: Titulo de la clase

Profesor: Nombre del profesor
Asignatura: Nombre de la asignatura
Universidad: Nombre de la universidad
Estilo: tecnologico_oscuro
Imagen Universidad: assets/imagen_universidad.jpg

Agenda:
- Bienvenida y contexto de la semana
- Revisión de conceptos previos
- Desarrollo del tema central
- Actividad practica

Contenido Presentacion:
- Objetivo de la clase
- Tema principal
- Ejemplo tecnico
- Actividad o caso aplicado
- Cierre y aprendizajes

Aprendizajes:
- Primer aprendizaje esperado.
- Segundo aprendizaje esperado.
- Tercer aprendizaje esperado.

Frase Final: Una frase motivacional breve para cerrar la clase.

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
- `Imagen Universidad:` puede ser una ruta local como `assets/universidad_umg.jpg` o una busqueda para Pexels/Pixabay.
- `Agenda:` crea una diapositiva automatica con puntos de clase.
- `Contenido Presentacion:` crea una diapositiva automatica con la estructura del material.
- `Aprendizajes:` alimenta la diapositiva final de cierre.
- `Frase Final:` agrega una frase motivacional al cierre.
- `Estilo:` puede ser `academico_formal`, `tecnologico_oscuro`, `alto_impacto`, `ingenieria_codigo`, `pizarra_matematica`, `laboratorio_redes`, `ciberseguridad` o `minimalista_claro`.
- Cada diapositiva empieza con `## Diapositiva:`.
- `Objetivo:` es opcional, pero recomendado.
- `Contenido:` contiene bullets iniciados con `-`.
- `Imagen:` puede ser una ruta local como `assets/diagrama_usb.png` o una busqueda en ingles para mejorar resultados en Pexels/Pixabay.
- `Tipo: codigo` activa una diapositiva con bloque de codigo.
- Si Pexels falla o no hay API key, el sistema genera la diapositiva con diseno alternativo.
