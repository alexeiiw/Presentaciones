# Formato Markdown de la clase

Usa este formato para pegar el contenido en la interfaz web. Si un LLM genera el Markdown, debe seguir estas reglas para producir presentaciones variadas, academicas y visualmente claras.

## Instrucciones para LLM

- Genera entre 12 y 24 diapositivas para una clase universitaria de 60 a 120 minutos.
- No uses el layout normal en todas las diapositivas: alterna `Tipo:` segun el proposito pedagogico.
- Usa `Tipo: contenido` o no escribas `Tipo:` solo para explicaciones conceptuales generales.
- Usa `Tipo: columnas` para comparaciones, ventajas/desventajas, antes/despues, serial/paralelo, PATA/SATA o problema/solucion.
- Usa `Tipo: ruta` para procesos, secuencias historicas, fases, evolucion de versiones, pasos de laboratorio o flujo de aprendizaje.
- Usa `Tipo: frase` para ideas centrales, principios de ingenieria, advertencias importantes o transiciones entre secciones.
- Usa `Tipo: seccion` para separar bloques grandes de la clase, por ejemplo pasar de USB a almacenamiento interno.
- Usa `Tipo: diagrama` para mapas conceptuales, componentes de arquitectura, relaciones entre capas, buses, controladores, hosts, dispositivos o protocolos.
- Usa `Tipo: actividad` para ejercicios de clase, analisis en grupo, mini laboratorio, preguntas guiadas o trabajo aplicado.
- Usa `Tipo: repositorio` para recursos finales, comandos, enlaces, lecturas, herramientas, documentacion o checklist de estudio.
- Usa `Tipo: codigo` solo cuando exista codigo real entre triple backtick.
- Nunca dejes una diapositiva con solo `## Diapositiva:` salvo que tenga `Tipo: seccion` y funcione como separador intencional.
- Todo bloque listado en `Contenido Presentacion:` debe tener al menos una diapositiva desarrollada despues.
- Si anuncias un tema en agenda, tambien debe aparecer en el contenido o en una actividad de cierre.
- No termines la clase inmediatamente despues de una seccion nueva; desarrolla el bloque con contenido, comparativa, diagrama, actividad o repositorio.
- Cada diapositiva debe tener maximo 6 bullets en `Contenido:`. Si hay mas, divide en varias diapositivas.
- Escribe bullets completos, tecnicos y explicativos; evita frases vagas como "concepto importante".
- Para `Imagen:`, escribe keywords especificas en ingles. Evita keywords genericas como `technology`, `math`, `computer` o `education`.
- Para temas tecnicos, prefiere keywords concretas como `usb type c connector close up`, `sata data cable motherboard`, `parallel ide cable`, `serial communication oscilloscope`, `printed circuit board data bus`.
- Incluye al menos una diapositiva `Tipo: actividad` antes del cierre.
- Incluye al menos dos diapositivas visuales avanzadas entre `columnas`, `ruta` o `diagrama` por cada 10 diapositivas de contenido.
- Para clases tecnicas, incluye al menos una comparativa `Tipo: columnas`, una secuencia `Tipo: ruta`, un mapa `Tipo: diagrama` y una practica `Tipo: actividad`.
- Usa formulas en texto simple cuando sean necesarias, pero mantenlas cortas y explicadas.

## Checklist de calidad antes de generar

- La presentacion desarrolla todos los bloques declarados en `Contenido Presentacion:`.
- La agenda no promete temas que luego quedan sin diapositivas.
- Ninguna diapositiva queda vacia por accidente.
- Cada `Tipo: seccion` va seguido por una diapositiva que desarrolla ese bloque.
- Hay al menos una comparativa tecnica con `Tipo: columnas`.
- Hay al menos una secuencia, flujo o evolucion con `Tipo: ruta`.
- Hay al menos un mapa conceptual o arquitectura con `Tipo: diagrama`.
- Hay al menos una practica o discusion con `Tipo: actividad`.
- Hay una diapositiva final de recursos con `Tipo: repositorio` cuando la clase requiere seguimiento.
- Las imagenes usan keywords tecnicas especificas en ingles.
- Los bullets explican ideas completas y no son etiquetas sueltas.

````markdown
# Clase: Titulo de la clase

Profesor: Nombre del profesor
Asignatura: Nombre de la asignatura
Universidad: Nombre de la universidad
Estilo: tecnologico_oscuro
Imagen Portada: assets/imagen_universidad.jpg
Logo Portada: assets/logo_universidad.png

Agenda:
- Bienvenida y contexto de la semana
- Revisión de conceptos previos
- Desarrollo del tema central
- Actividad practica

Contenido Presentacion:
- Bloque 1: Fundamentos conceptuales
- Bloque 2: Desarrollo tecnico principal
- Bloque 3: Comparativa o arquitectura
- Bloque 4: Actividad practica
- Bloque 5: Recursos y cierre

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
- `Imagen Portada:` o `Imagen Universidad:` puede ser una ruta local como `assets/universidad_umg.jpg`, solo el nombre como `universidad_umg.jpg`, o una busqueda para Pexels/Pixabay.
- `Logo Portada:` o `Logo Universidad:` puede ser una ruta local como `assets/logo_umg.png` o solo el nombre como `logo_umg.png` si esta dentro de `assets/`.
- Para presentaciones UMG, se recomienda usar `Imagen Portada: images.jpg` y `Logo Portada: Umg.png` cuando esos archivos esten disponibles en `assets/` o en la ruta local de trabajo.
- `Agenda:` crea una diapositiva automatica con puntos de clase.
- `Contenido Presentacion:` crea una diapositiva automatica con la estructura del material.
- Cada item de `Contenido Presentacion:` debe estar desarrollado por al menos una diapositiva posterior.
- `Aprendizajes:` alimenta la diapositiva final de cierre.
- `Frase Final:` agrega una frase motivacional al cierre.
- `Estilo:` puede usar cualquiera de los estilos listados abajo.
- Cada diapositiva empieza con `## Diapositiva:`.
- `Objetivo:` es opcional, pero recomendado.
- `Contenido:` contiene bullets iniciados con `-`.
- `Imagen:` puede ser una ruta local como `assets/diagrama_usb.png` o una busqueda en ingles para mejorar resultados en Pexels/Pixabay.
- `Tipo: codigo` activa una diapositiva con bloque de codigo.
- `Tipo:` tambien puede ser `columnas`, `ruta`, `frase`, `seccion`, `diagrama`, `actividad` o `repositorio`.
- Si Pexels falla o no hay API key, el sistema genera la diapositiva con diseno alternativo.

## Estilos disponibles

- `academico_formal`
- `tecnologico_oscuro`
- `alto_impacto`
- `ingenieria_codigo`
- `pizarra_matematica`
- `laboratorio_redes`
- `ciberseguridad`
- `minimalista_claro`
- `universitario_elegante`
- `seminario_ejecutivo`
- `taller_practico`
- `modo_examen`
- `clase_visual`

## Tipos avanzados

Usa `Tipo:` dentro de una diapositiva para cambiar su layout.

### `Tipo: columnas`

Uso recomendado: comparaciones, contrastes, ventajas/desventajas o dos perspectivas del mismo tema.

Reglas:

- Escribe de 4 a 8 bullets.
- Los primeros bullets alimentan la primera columna y los restantes la segunda.
- El titulo debe indicar claramente que hay comparacion.

```markdown
## Diapositiva: Comparacion de conceptos

Tipo: columnas

Contenido:
- Definicion del primer concepto.
- Ventaja principal.
- Riesgo o limitacion.
- Definicion del segundo concepto.
- Caso de uso.
- Criterio de decision.
```

### `Tipo: ruta`

Uso recomendado: procesos, pasos, evolucion historica, versionado, flujo de comunicacion o secuencia de laboratorio.

Reglas:

- Escribe de 3 a 5 bullets.
- Cada bullet debe ser un paso corto y accionable.
- No lo uses para listas largas de teoria.

```markdown
## Diapositiva: Ruta de aprendizaje

Tipo: ruta

Contenido:
- Concepto base
- Demostracion
- Practica
- Discusion
- Evidencia final
```

### `Tipo: frase`

Uso recomendado: mensaje central, principio tecnico, advertencia critica o separador entre bloques de la clase.

Reglas:

- Usa `Objetivo:` como frase principal.
- Opcionalmente agrega 1 bullet como comentario secundario.
- No uses mas de 2 bullets.

```markdown
## Diapositiva: Idea central

Tipo: frase

Objetivo: La tecnologia solo aporta valor cuando resuelve un problema real.

Contenido:
- Criterio para discutir en clase.
```

### `Tipo: seccion`

Uso recomendado: separador visual entre grandes bloques de contenido.

Reglas:

- Puede tener solo titulo si es una transicion intencional.
- Si agregas `Objetivo:`, se mostrara como subtitulo de la seccion.
- No uses bullets extensos; si necesitas explicar, usa `Tipo: contenido`.
- Debe ir seguido por una o mas diapositivas que desarrollen esa seccion.

```markdown
## Diapositiva: Almacenamiento Interno: PATA vs. SATA

Tipo: seccion

Objetivo: Pasamos de buses externos USB a interfaces internas de almacenamiento.

Imagen: sata data cable motherboard close up
```

### `Tipo: diagrama`

Uso recomendado: arquitectura, relaciones entre componentes, mapa conceptual, topologia o estructura de protocolo.

Reglas:

- Escribe de 4 a 6 bullets.
- Cada bullet debe ser un nodo del diagrama.
- El titulo funciona como nodo central.

```markdown
## Diapositiva: Mapa conceptual

Tipo: diagrama

Contenido:
- Nodo principal 1
- Nodo principal 2
- Nodo principal 3
- Nodo principal 4
```

## Ejemplo recomendado para PATA/SATA

Si `Contenido Presentacion:` anuncia almacenamiento interno, no basta con una seccion. Debe incluir al menos una diapositiva explicativa o comparativa.

```markdown
## Diapositiva: Comparativa: PATA vs. SATA

Tipo: columnas

Objetivo: Comparar la evolucion de las interfaces internas de almacenamiento.

Contenido:
- PATA: Utiliza transmision paralela mediante cable plano IDE de 40 u 80 hilos.
- PATA: Presenta problemas de diafonia, flujo de aire y sincronizacion a altas frecuencias.
- PATA: Alcanzo limites practicos cercanos a 133 MB/s en ATA/133.
- SATA: Utiliza transmision serial punto a punto con cables delgados y menor interferencia.
- SATA: Mejora la integridad de senal y simplifica la administracion fisica del gabinete.
- SATA: Evoluciona desde 1.5 Gbps hasta 6 Gbps en SATA III.

Imagen: sata data cable and ide ribbon cable comparison
```

### `Tipo: actividad`

Uso recomendado: practica, pregunta aplicada, resolucion de caso, mini laboratorio o discusion dirigida.

Reglas:

- Usa `Objetivo:` para describir la tarea que hara el estudiante.
- Escribe de 3 a 9 bullets.
- Los bullets se distribuyen en instrucciones, evidencia y cierre.

```markdown
## Diapositiva: Laboratorio en clase

Tipo: actividad

Objetivo: Aplicar el concepto en equipos.

Contenido:
- Formar grupos de trabajo.
- Resolver el caso propuesto.
- Presentar una evidencia.
```

### `Tipo: repositorio`

Uso recomendado: recursos, lecturas, comandos, checklist, enlaces o herramientas para continuar estudiando.

Reglas:

- Escribe de 3 a 6 bullets.
- Cada bullet debe ser un recurso concreto o accion de estudio.
- Es ideal para una de las ultimas diapositivas antes del cierre.

```markdown
## Diapositiva: Recursos de apoyo

Tipo: repositorio

Contenido:
- Lectura recomendada
- Documentacion oficial
- Video de apoyo
- Practica sugerida
```
