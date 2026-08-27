# novel-chapter-character

**Versión**: 2.0
**Función**: Paso 4.3 - Configuración de personajes

---

## Entrada

```yaml
framework: object            # Requisitos del personaje según el esquema del capítulo
chapter_number: number
project_path: string
```

---

## Salida

```yaml
status: "success"
character_configs:
existing:
- name: string
source: "existing"
current_state: object
offline_changes: string  # Se genera cuando la diferencia es ≥ 10 capítulos
new:
- name: string
source: "created"
profile: object
archive_decision: "yes" | "no"
```

---

## Reglas de actualización de personajes fuera de pantalla

```
Diferencia < 10 capítulos: Sin cambios
Diferencia ≥ 10 capítulos: Generar cambios según sea necesario

Tipos de cambio:
A. Sin cambios
B. Progreso menor
C. Avance significativo
D. Evento inesperado

Criterios de selección: Requisitos de la trama > Objetivos del personaje > Aleatorio pero plausible
```
