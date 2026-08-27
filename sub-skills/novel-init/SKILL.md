# novel-init

**Versión**: 2.0
**Función**: Paso 0 - Inicialización del proyecto

---

## Entrada

```yaml
project_name: string    # Nombre del proyecto (proporcionado por el usuario)
```

---

## Salida

```yaml
status: "success"
message: "Proyecto creado"
project_path: string
file_tree:
- config/status.md
- config/prompts.yaml
- memory/world-setting.md
- memory/protagonist.md
- memory/power-system.md
- memory/organizations.md
- memory/geography.md
- memory/artifacts.md
- memory/timeline.md
- memory/races.md
- memory/culture.md
- memory/outline.md
- memory/plot-hooks.md
- memory/cognitive-log.md
- memory/chapter-summaries.md
- memory/characters/core/
- memory/characters/secondary/
- memory/characters/archive/
- chapters/
- deliverables/
next_action: "proceed_to_brainstorm"
```

---

## Acciones de ejecución

1. Crear la estructura de directorios (Directorio raíz: `~/Documents/novel-projects/{project_name}`)
2. Generar el archivo `status.md` inicial
3. Generar `prompts.yaml` (configuración de prompts)
4. Devolver mensaje de éxito

---

## Notas

- **La ruta de salida está fijada en `~/Documents/novel-projects/`**
- Si el directorio ya existe, solicitar al usuario que elija entre sobrescribirlo o utilizar un nombre diferente
- El nombre del proyecto admite caracteres chinos
