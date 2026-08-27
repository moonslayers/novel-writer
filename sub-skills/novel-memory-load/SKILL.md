# novel-memory-load

**Versión**: 2.0
**Función**: Cargar de forma inteligente la memoria necesaria para la escritura

---

## Entrada

```yaml
chapter_number: number
framework: object
project_path: string
```

---

## Salida

```yaml
status: "success"
memory:
essential:
- world_setting
- protagonist
- power_system
- outline
relevant:
- active_hooks
- previous_chapter
- previous_summary
- characters: [...]
filtered: boolean
```

---

## Estrategia de carga

1. Cargar la memoria esencial
2. Recuperar los ganchos narrativos activos
3. Recuperar el capítulo anterior
4. Cargar los personajes presentes según el marco de trabajo (framework)
- Verificar el tiempo transcurrido (desde la última aparición)
- Si el intervalo es ≥ 10 capítulos: Generar cambios
5. Recuento de tokens (≤8000)
6. Truncar según relevancia si se supera el límite
