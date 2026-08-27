# configuración-de-novela

**Versión**: 2.0
**Función**: Paso 2 - Generación del entorno

---

## Entrada

```yaml
brainstorm_result: object    # Elementos confirmados durante la lluvia de ideas
project_path: string
```

---

## Salida

```yaml
status: "success"
generated_files:
essential:                 # Contenido completado
- world-setting.md
- protagonist.md
- power-system.md       # O political-system.md, si corresponde
extension:                 # Solo estructuras base
- organizations.md
- geography.md
- artifacts.md
- timeline.md
- races.md
- culture.md
user_prompt: |
Se ha creado la estructura para los elementos extendidos del entorno. ¿Cuáles de los siguientes ya tienes planificados?

□ Facciones/Organizaciones
□ Mapa/Lugares clave
□ Sistema de objetos/elementos
□ Historia/Cronología
□ Razas/Bestiario
□ Cultura/Normas sociales

Completaré el contenido de los elementos que marques; los no marcados permanecerán como 'Pendientes'.
next_action: "wait_user_selection"
```

---

## Acciones de ejecución

1. Generar 3 tipos de elementos esenciales del entorno (basados ​​en los resultados de la lluvia de ideas)
2. Crear 6 tipos de elementos extendidos (estructuras base + marcadores de 'Pendiente')
3. Preguntar al usuario cuáles requieren desarrollo inmediato

---

## Lista de 13 categorías del entorno

### Esenciales (3 tipos)
1. world-setting.md
2. protagonist.md
3. power-system.md / political-system.md

### Extendidos (6 tipos)
4. organizations.md
5. geography.md
6. artifacts.md
7. timeline.md
8. races.md
9. culture.md

### Dinámicos (Se actualizan durante la escritura)
10-13. Personajes secundarios, presagios, percepciones, resúmenes de capítulos
