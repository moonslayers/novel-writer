# estructura-de-capítulo-de-novela

**Versión**: 2.0
**Función**: Paso 4.2 - Concepción del esquema del capítulo

---

## Entrada

```yaml
chapter_number: número
previous_chapter_summary: cadena_de_texto
memory_context: objeto
outline_requirement: cadena_de_texto
```

---

## Salida

```yaml
status: "success"
framework:
chapter: número
type: "setup" | "climax" | "aftermath" | "transition"
goal:
narrative: cadena_de_texto
emotion: cadena_de_texto
word_count: 3000
structure:
setup: [beat1, beat2, ...]      # 60%
climax: [beat1, beat2]          # 20%
aftermath: [beat1, beat2]       # 20%
characters:
required: [name1, name2]
optional: [name3]
new: [{name, role, importance}]
hooks:
resolve: [hook_id]
plant: [{description, importance}]
remind: [hook_id]
```

---

## Verificación de restricciones

- Planteamiento (Setup) ≤ 60%
- Clímax ≥ 20%
- Desenlace (Aftermath) ≥ 20%
- Regenerar si no se cumplen las restricciones
