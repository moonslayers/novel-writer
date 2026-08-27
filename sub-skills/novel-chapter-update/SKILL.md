# actualización-de-capítulo-de-novela

**Versión**: 2.0
**Función**: Paso 4.7 - Actualización de memoria

---

## Entrada

```yaml
chapter_number: number
chapter_content: string
change_summary: object
project_path: string
```

---

## Salida

```yaml
status: "success"
updated_files:
- chapters/chapter-{N}.md
- memory/protagonist.md
- memory/characters/{name}.md
- memory/plot-hooks.md
- memory/cognitive-log.md
- memory/chapter-summaries.md
- config/status.md
```

---

## Secuencia de actualización

1. Guardar el texto del cuerpo del capítulo
2. Actualizar el perfil del protagonista
3. Actualizar/crear perfiles de personajes secundarios
4. Actualizar el registro de ganchos argumentales
5. Añadir al registro cognitivo
6. Añadir el resumen del capítulo
7. Actualizar el estado del proyecto

Todas las actualizaciones son atómicas; es posible revertir los cambios en caso de fallo.
