# Escritura de capítulos de novela

**Versión**: 2.0
**Función**: Paso 4.4 - Generación del texto principal

---

## Entrada

```yaml
framework: object
characters: object
memory: object
user_feedback: object        # Sugerencias de revisión (si las hay)
```

---

## Salida

```yaml
status: "success"
content: string              # Texto completo del capítulo
word_count: number
change_summary:
plot_progress: {...}
character_changes: {...}
new_characters: [...]
world_changes: [...]
next_chapter_hints: [...]
```

---

## Restricciones de escritura

### Gancho inicial (primeras 100 palabras)
✓ Conflicto/crisis/secreto/anomalía
✗ Sin descripciones ambientales ni exposición de trasfondo

### Control del ritmo
✓ Ligero avance de la trama cada 300 palabras
✓ Cambio emocional cada 800 palabras
✓ Liberación de tensión requerida tras ≤1500 palabras de acumulación

### Ingeniería de "satisfacción" (60%-20%-20%)
- Acumulación: Generar expectación, crear obstáculos, contener emociones
- Clímax: Momento desencadenante, revelar contraste, dominio inmediato
- Consecuencias: Reacciones de personajes secundarios (≥3 tipos), cambios en el entorno, nuevo gancho

### Estilo de escritura
✓ Centrarse en acciones; minimizar adjetivos
✓ Minimizar metáforas; presentar directamente
✓ Oraciones cortas; priorizar verbos
✓ Mostrar, no contar

### Restricciones creativas (Nuevas)
✓ Evitar copiar directamente tropos clásicos
✓ Diseño único para el "Dedo de Oro" (habilidad ventajosa/truco)
✓ Al menos un elemento "inesperado" por capítulo

### Verificación contra tropos (Prohibidos)
✗ Diálogos al estilo "Treinta años en la orilla este del río..."
✗ Maestro antiguo/espíritu oculto en un anillo o colgante de jade
✗ Prueba de aptitud pública seguida de humillación pública
✗ Prometida que llega para lanzar insultos

### Requisito de finalización
✓ Nuevo problema/crisis/interrogante
✗ Sin finales felices y cerrados
