# novel-brainstorm

**Versión**: 2.0
**Función**: Pasos 1 y 3 – Clarificación de requisitos y lluvia de ideas (interactiva)

---

## Principio de diseño fundamental

**Sin interacción directa con el usuario**; todas las interacciones se canalizan a través de la Skill principal (orquestador). ```
Usuario ←→ Skill principal ←→ novel-brainstorm
↑
Responsable de presentar preguntas y recopilar respuestas
```

---

## Interfaz de entrada

```yaml
mode: "generate_question" | "process_answer" |
``` "finalizar"

# modo = generate_question
contexto:
project_path: string
current_confirmed: object      # Elementos del esquema confirmados
pending_dimensions: array      # Lista de dimensiones pendientes de discusión
last_answer: null              # Sin respuesta del usuario

# modo = process_answer
contexto:
project_path: string
current_confirmed: object
pending_dimensions: array
last_answer:                   # Respuesta del usuario
question_id: string
answer_text: string
selected_option: string      # Si aplica

# modo = finalize
contexto:
project_path: string
current_confirmed: object      # Todas las confirmaciones completadas
```

---

## Interfaz de salida

```yaml
# acción = ask_user (requiere interacción adicional)
status: "in_progress"
action: "ask_user"
question:
id: string                     # Identificador único de la pregunta
dimension: string              # Dimensión asociada
text: string                   # Texto de la pregunta
description: string            # Motivo de la pregunta
options:                       # Opciones (si aplica)
- id: "A"
text: "Descripción de la opción A"
- id: "B"
text: "Descripción de la opción B"
- id: "C"
text: "Otro: ___"
allow_free_input: boolean      # Si se permite entrada de texto libre

confirmed_update: object         # Contenido confirmado recién añadido/actualizado
next_dimension: string           # Siguiente dimensión sugerida
progress:                        # Estado del progreso
current: number
total: number

---

# acción = continue (continuación automática, no requiere entrada del usuario)
status: "in_progress"
action: "continue"
message: string                  # Explicación para continuar
confirmed_update: object
next_dimension: string

---

# acción = complete (todas las tareas finalizadas)
status: "completed"
action: "complete"
confirmed_elements: object       # Elementos completos del esquema de seis dimensiones
file_updates:
- path:
``` "memory/brainstorm-result.yaml"
content: "..."
next_step: "proceed_to_setup" | "proceed_to_outline"
```

---

## Lista de verificación de seis dimensiones

| N.º | Dimensión | Preguntas clave |
|:---:|------|---------|
| 1 | arco_del_protagonista | Punto de partida y de llegada del protagonista, y puntos de giro clave |
| 2 | conflictos | Conflictos internos y obstáculos externos |
| 3 | eventos_clave | Acontecimientos centrales y diseño de "momentos satisfactorios" (emociones fuertes/recompensas narrativas) |
| 4 | relaciones | Evolución de las relaciones importantes |
| 5 | hitos | Hitos en cuanto a habilidades o estatus |
| 6 | ganchos_trama | Anticipaciones y su resolución |

---

## Ejemplo de flujo de interacción

### Ronda 1: Generación de la primera pregunta

**Entrada**:
```yaml
mode: "generate_question"
current_confirmed: {}
pending_dimensions: ["protagonist_arc", "conflicts", ...]
```

**Salida**:
```yaml
status: "in_progress"
action: "ask_user"
question:
id: "q1_protagonist_start"
dimension: "protagonist_arc"
text: "¿Cuál es la situación del protagonista al inicio?" 
description: "Esto determina el punto de partida de la historia y la sensación de inmersión del lector."
``` opciones:
- id: "A"
text: "Ya se encuentra en una situación desesperada (p. ej., compromiso roto, poderes anulados, siendo perseguido)"
- id: "B"
text: "Moderadamente desafortunado (p. ej., origen humilde, talento no reconocido)"
- id: "C"
text: "Aparentemente glamuroso (pero con problemas ocultos subyacentes)"
allow_free_input: true
confirmed_update: {}
next_dimension: "protagonist_arc"
progress:
current: 1
total: 6
```

### Ronda 2: Procesamiento de la respuesta del usuario

**Entrada**:
```yaml
mode: "process_answer"
current_confirmed: {}
last_answer:
question_id: "q1_protagonist_start"
selected_option: "A"
answer_text: "El chico inútil cuyo compromiso fue cancelado"

```

**Salida**:

```yaml
status: "in_progress"
action: "ask_user"
question:

id: "q2_protagonist_end"

dimension: "protagonist_arc"

text: "¿Qué tipo de final quieres que tenga?"

opciones:

- id: "A"

texto: "Estar en la cima del mundo"

- id: "B"

texto: "Encontrar el amor verdadero y retirarse"

- id: "C"

texto: "Vengarse con éxito pero perderlo todo"

actualización_confirmada:

arco_del_protagonista:

inicio: "El chico inútil cuyo compromiso fue anulado"

siguiente_dimensión: "arco_del_protagonista"

progreso:

actual: 1

total: 6

```

### Ronda final: Completar

**Entrada**:

```yaml
modo: "finalizar"

confirmado_actualmente:

arco_del_protagonista: {...}
conflictos: {...}
...
```

**Salida**:
```yaml
estado: "completado"
acción: "completar"
elementos_confirmados:
arco_del_protagonista: {...}
conflictos: {...}
eventos_clave: {...}
relaciones: {...}
hitos: {...}
ganchos_trama: {...}
actualizaciones_archivo:
- ruta: "memory/brainstorm-result.yaml"
contenido: "..."
siguiente_paso: "proceder_a_configuración"
```

---

## Uso

Llamado por la Habilidad principal (novel-writer):

```javascript
// primera ronda
const result = await callSubSkill('novel-brainstorm', {
mode: 'generate_question',
context: { current_confirmed: {}, pending_dimensions: [...] }
});

// Mostrar al usuario y recopilar respuestas.

const userAnswer = await presentToUser(result.question);

// Siguiente ronda
const result2 = await callSubSkill('novel-brainstorm', {
mode: 'process_answer',
context: {
current_confirmed: result.confirmed_update,

last_answer: userAnswer

}
});

// Repetir hasta que result.action === 'complete'

```

---

## Mejores prácticas

1. **Haz solo 1 o 2 preguntas por ronda** para evitar abrumar al usuario.
2. **Ofrece opciones junto con la posibilidad de respuestas abiertas** para reducir la carga cognitiva de la toma de decisiones.
3. **Explica el motivo de la pregunta** para que el usuario comprenda su valor. 4. **Mostrar el progreso** para informar al usuario de cuánto queda.
5. **Permitir retroceder** para que los usuarios puedan modificar respuestas anteriores.
