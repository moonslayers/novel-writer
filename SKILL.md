---
name: novel-writer
description: Motor de creación de novelas (v3.0). Incluye validación obligatoria, puntos de control y un mecanismo evolutivo. Admite todo el flujo de trabajo para escribir una novela completa, desde el concepto inicial hasta el manuscrito final. Se activa mediante comandos del usuario como "escribir una novela", "crear una historia" o "iniciar una serie".
metadata: {"clawdbot":{"emoji":"📚"}}
---

# novel-writer v3.0

**Filosofía fundamental**: Las restricciones basadas en código prevalecen sobre las directrices estilísticas. Utiliza scripts para la validación obligatoria, puntos de control para garantizar la capacidad de recuperación y un mecanismo evolutivo para la mejora continua. ---

## Ruta de salida del proyecto

**Regla de ruta**: `~/Documents/{BookTitle}/`

- El nombre del directorio utiliza **únicamente caracteres chinos**, coincidiendo exactamente con el título del libro. - Ejemplo: *He Raised the Emperor* → `~/Documents/他养大了皇帝/`
- Ejemplo: *The Hidden Prime Minister* → `~/Documents/隐相/`

**Estructura de directorios**:
```
~/Documents/{BookTitle}/
├── config/
│   ├── project_info.md ​​​​       # Metadatos del proyecto
│   ├── worldbuilding.md       # Configuración de la construcción del mundo
│   ├── characters.md          # Biografías de personajes
│   └── volume_outline.md      # Esquema del volumen
├── memory/
│   ├── character_cards.md     # Fichas de personajes (formato YAML)
│   ├── relationship_map.md    # Mapa de relaciones entre personajes
│   ├── foreshadowing.md       # Seguimiento de presagios
│   ├── lessons_learned.md     # Ideas creativas acumuladas
│   └── checkpoints/           # Instantáneas de puntos de control
├── chapters/
│   ├── vol1_chapter_01.md
│   ├── vol1_chapter_02.md
│   └── ...
├── deliverables/
│   ├── final.md               # Manuscrito consolidado
│   └── final.docx             # Documento exportado
└── status.md                  # Estado actual (Fuente única de verdad)
```

---

## Arquitectura central

```
Usuario ←→ novel-writer (Planificador)
│
├── scripts/validate_step.py (Validación obligatoria)
├── scripts/checkpoint.py (Instantánea/Reversión)
└── Sub-habilidades (Ejecución de tareas específicas)
```

**Reglas inquebrantables**:
1. El script de validación debe ejecutarse al finalizar cada paso.
2. Fallo en la validación = Bloqueo (no se puede omitir).
3. Los puntos de control se crean automáticamente en hitos clave. ---

## Máquina de estados (con validación obligatoria)

### Paso 0: init (Inicialización)
```
Acción: Inicializar el proyecto
Validación: scripts/validate_step.py --step 0
Salida: status.md (Estado inicial)
```

### Paso 1: brainstorm (Ideación creativa) ⚠️ Debe consultarse con el usuario
```
Acción: Debatir y confirmar los siguientes seis elementos con el usuario:
1. Título (Ofrecer entre 3 y 5 opciones para que el usuario elija, o aceptar el título propuesto por él)
2. Extensión (Relato corto/novela corta/novela; especificar el rango de recuento de palabras)
3. Perspectiva narrativa (Tercera persona/primera persona/perspectiva dual; explicar ventajas y desventajas)
4. Alcance de la historia (Enfoque en un periodo específico frente a la historia de toda una vida)
5. Tono emocional (p. ej., de suspense, conmovedor, apasionado/enérgico, desenfadado, etc.)
6. Estilo de escritura (Consultar la [Guía de selección de estilo de escritura] más abajo)

[Guía de selección de estilo de escritura]
El estilo de escritura es una especificación fundamental de la obra y debe determinarse durante la fase creativa.
``` Opciones comunes:

A. Estilo basado en verbos (Recomendado para novelas web)
- Características: Oraciones cortas, ritmo ágil, alta densidad de información, enfoque centrado en la acción
- Evitar: Acumulación de adjetivos, cláusulas largas o complejas, adjetivos que describen estados internos
- Ejemplos: *Da Feng Watchman* (大奉打更人), *Lord of the Mysteries* (诡秘之主)
- Adecuado para: Suspense, intriga política, géneros de supervivencia

B. Estilo sobrio y elegante
- Características: Emoción contenida, el arte de "dejar espacio" (sutileza), encanto clásico
- Evitar: Sentimentalismo excesivo, coloquialismos modernos, explicaciones redundantes
- Ejemplos: *Nirvana in Fire* (琅琊榜), *Joy of Life* (庆余年)
- Adecuado para: Drama histórico, intriga política, historias emotivas o centradas en los personajes

C. Estilo humorístico e ingenioso
- Características: Monólogo interno rico, memes modernos, tensión aliviada mediante el humor
- Evitar: Melodrama excesivo, atmósfera pesada u opresiva
- Ejemplos: *My Senior Brother is Too Steady* (我师兄实在太稳健了), *Da Feng Watchman*
- Adecuado para: Historias gratificantes (*Shuangwen*), transmigración, género de "Sistema"

D. Estilo intenso y apasionado
- Características: Citas memorables frecuentes, alta intensidad emocional, conflicto fuerte
- Evitar: Ritmo lento, vacilación, exceso de cálculos
- Ejemplos: *Battle Through the Heavens* (斗破苍穹), *Sword Snow Stride* (雪中悍刀行)
- Adecuado para: Fantasía (*Xuanhuan*), *Wuxia*, historias de progresión o subida de nivel

E. Estilo de suspense y opresivo
- Características: Creación de atmósfera, asimetría de información, revelaciones graduales
- Evitar: Revelaciones prematuras, narración plana o demasiado directa
- Ejemplos: *Lord of the Mysteries*, *The Lost Tomb* (盗墓笔记)
- Adecuado para: Suspense, *thriller*, géneros de detectives o misterio

【Plantilla de especificación del estilo de escritura】 (Escribir en `project_info.md` una vez confirmado)
- Tipo de estilo: estilo xxx
- Principio fundamental: (Resumir en una oración)
- Pautas de estructura de oraciones: (Longitud del párrafo, longitud de la oración)
- Vocabulario prohibido: (Lista de palabras prohibidas específicas)
- Monólogo interno/Descripción psicológica: (Cómo expresarlo)
- Pautas de diálogo: (Requisitos de formato)
- Ganchos de capítulo: (Requisitos para el final)

Bloqueo de estado (Escribir en `status.md`):
"Tarea actual: Esperando confirmación del usuario sobre {Nombre del elemento}"
Actualizar tras la confirmación de cada elemento: "- [x] Título del libro confirmado: xxx"
"- [x] Longitud confirmada: xxx"
"- [x] Estilo de escritura confirmado: xxx"
...

Validación:
scripts/validate_step.py --step 1 --book-name "{Título del libro}"

Lista de verificación:
□ status.md contiene "Título del libro confirmado"
□ status.md contiene "Longitud confirmada"
□ status.md contiene "Perspectiva confirmada"
□ status.md contiene "Alcance confirmado"
□ status.md contiene "Tono confirmado"
□ status.md contiene "Estilo de escritura confirmado"
□ project_info.md ​​contiene la [Plantilla de especificación del estilo de escritura] completa

Regla de bloqueo: Proceder al Paso 2 solo después de confirmar los seis elementos.
```

### Paso 2: project_init ⚠️ Primer punto de bloqueo obligatorio
```
Acción: Crear directorio del proyecto
Comando:
mkdir -p ~/Documents/{Título del libro}/{config,memory,chapters,deliverables}
echo "# {Título del libro}" > ~/Documents/{Título del libro}/config/project_info.md

Validación (todos deben cumplirse):
scripts/validate_step.py --step 2 --book-name "{Título del libro}"

Lista de verificación:
□ El directorio existe: ~/Documents/{Título del libro}/
□ Subdirectorios presentes: config/, memory/, chapters/, deliverables/
□ project_info.md ​​existe y no está vacío

Gestión de fallos: Informar del error y detenerse; no pasar al Paso 3
Punto de control: Crear automáticamente `step_2_complete.checkpoint` tras una validación exitosa
```

### Paso 3: world_building ⚠️ Segundo punto de bloqueo obligatorio
```
Acción: Elaborar la construcción del mundo y la configuración de los personajes
Resultados (todos obligatorios):
1. config/worldbuilding.md     - Época/entorno, ubicaciones clave, sistemas y normas de etiqueta
2. config/characters.md        - Biografías de personajes (protagonistas y secundarios)
3. memory/character_cards.md   - Fichas de personaje estructuradas (YAML)
4. memory/relationship_map.md  - Mapa de relaciones entre personajes

Validación:
scripts/validate_step.py --step 3 --book-name "{Book Name}"

Verificaciones:
□ Existen los cuatro archivos
□ Recuento de palabras por archivo > 500
□ `character_cards.md` contiene estructuras YAML para al menos 3 personajes

Gestión de fallos: Listar los archivos faltantes; impedir avanzar al Paso 4
Punto de control: Crear step_3_complete.checkpoint tras una validación exitosa
```

### Paso 4: volume_outline (Diseño del esquema de volúmenes)
```
Acción: Diseñar temas, conflictos centrales y arcos emocionales para tres volúmenes
Resultado: config/volume_outline.md
Confirmación: El usuario revisa y confirma explícitamente

Validación:
scripts/validate_step.py --step 4 --book-name "{Nombre del libro}"

Verificaciones:
□ Existe volume_outline.md
□ Contiene planes para al menos 3 volúmenes
□ Confirmado por el usuario (existe registro de confirmación en status.md)

Punto de control: Crear step_4_complete.checkpoint tras la confirmación
```

### Paso 5: volume_chapter_outline (Esquema completo de capítulos del volumen) ⚠️ Debe ejecutarse antes de comenzar cada volumen
```
Condiciones de activación:
- Inicio del primer volumen de un nuevo proyecto
- Finalización del volumen anterior y paso al siguiente

Acción: Generar resúmenes de la trama para todos los capítulos del volumen actual
Resultado: config/volume_{X}_chapter_outline.md

【Cuatro principios fundamentales de la progresión de la trama por capítulos】 ⚠️ No deben infringirse

**Principio 1: Principio de cadena de causalidad**
- La crisis de cada capítulo debe surgir de un problema latente del capítulo anterior
- No debe haber eventos aislados; cada capítulo debe derivar del anterior; no pueden aparecer nuevas crisis de la nada
- Requisito de formato: Los esquemas detallados de cada capítulo deben especificar la "Fuente de la crisis" (de qué problema latente del capítulo anterior se origina)

**Principio 2: Principio de elección y coste**
- El protagonista debe tomar una decisión clara en cada capítulo (elección activa, no resistencia pasiva)
- Toda elección conlleva un coste; este coste se convierte en la crisis del siguiente capítulo
- Requisito de formato: Los esquemas detallados de cada capítulo deben especificar la "Elección del protagonista" y el "Problema latente sembrado"

**Principio 3: Principio de escalada/progresión**
- La crisis debe intensificarse por etapas, tensándose como una cuerda que se tira con fuerza.
- Progresión secuencial: "exposición potencial" → "exposición inminente" → "exposición real".
- No repetir el mismo nivel de crisis.

**Principio 4: Ritmo y peso narrativo** ⚠️ Utiliza el número de capítulos para reflejar el ritmo.
- **Fase de transición**: Avanza con rapidez; dedica solo un capítulo por año o evento, o incluso combina varios sucesos en un único capítulo.
- **Fase de acumulación**: Aumenta la tensión; cada capítulo acerca la historia al núcleo de la crisis más que el anterior.
- **Fase de clímax**: Desarrolla con detalle; divide un evento importante en 3 a 6 capítulos, ocupando más del 40 % de la extensión total del volumen.
- **Fase de resolución**: Liberación emocional y cierre rápido; resuelve un asunto por capítulo.

【Estándares de peso narrativo】
| Peso | Significado | Cantidad de capítulos sugerida | Propósito |
|-----|------|-----------|------|
| ⭐ | Transición | 1 capítulo/año o menos | Avanzar en el tiempo, establecer la vida cotidiana |
| ⭐⭐ | Acumulación | 1–2 capítulos | Acumular tensión, señales iniciales de crisis |
| ⭐⭐⭐ | Punto de inflexión | 2–3 capítulos | Cambios importantes, agravamiento de la situación |
| ⭐⭐⭐⭐ | Preclímax | 3–4 capítulos | Preparación para el enfrentamiento final, confrontación directa |
| ⭐⭐⭐⭐⭐ | Gran clímax | 4–6 capítulos | El punto culminante del libro; desarrollo detallado |

【Requisitos de formato para el esquema detallado】
Cada capítulo debe incluir los siguientes elementos:
```
Capítulo X: Título del capítulo
- Tiempo: Momento específico en el tiempo
- Peso: ⭐–⭐⭐⭐⭐⭐
- Fuente de la crisis: ¿Qué amenaza oculta del capítulo anterior?
- Conflicto central: ¿Qué asunto se resuelve en este capítulo?
- Decisión del protagonista: ¿Qué decisión toma el protagonista?
- Semillas del conflicto: ¿Qué nueva crisis genera esta decisión?
- Enlace: ¿Cómo se conecta con el siguiente capítulo?
```

【Restricciones obligatorias】 ⚠️ Prohibido incumplirlas
1. **Escribir solo el contenido del volumen actual**: Limitarse estrictamente al marco temporal y a la trama definidos en `volume_outline.md`.
2. **No incluir contenido del siguiente volumen**: Los puntos de la trama del próximo volumen quedan totalmente excluidos del esquema detallado del volumen actual. 4. **Asegura transiciones fluidas entre volúmenes**:
- Capítulo inicial del volumen actual: Explica brevemente la situación tal como continúa desde el volumen anterior.
- Capítulo final del volumen actual: Definir claramente la situación final y preparar el terreno para el siguiente volumen.
5. **Cronología clara**: La marca temporal de cada capítulo debe situarse dentro del marco temporal definido para el volumen actual.

Ejemplos de infracción (prohibido):
❌ Incluir capítulos pertenecientes a los "Años en los aposentos del servicio del palacio" (Volumen 2) en el esquema detallado del Volumen 1.
❌ Escribir el capítulo final del Volumen 1 abarcando el ascenso al trono (esto corresponde al Volumen 3).
❌ Incluir referencias de dependencia como "ver detalles en el siguiente volumen" dentro del esquema del volumen actual.

Ejemplos correctos:
✅ Capítulo final del Volumen 1: Liu Bingyi es indultado y liberado de prisión; el capítulo termina a las puertas de los aposentos del servicio del palacio (preparando el escenario para el Volumen 2).
✅ Primer capítulo del Volumen 2: Comienza con la vida en los aposentos del servicio del palacio, mencionando brevemente el indulto recibido "hace dos años".

Proceso:
1. Leer `config/volume_outline.md` para comprender la temática y el alcance argumental del volumen.
2. [Verificar límites temporales] Confirmar los momentos de inicio y fin del volumen; respetar estrictamente estos límites.
3. Asignar puntos de la trama a cada capítulo según el número total de capítulos del volumen.
4. [Autoverificación] Comprobar si hay contenido que exceda el alcance del volumen actual.
5. Escribir en `config/volume_{X}_chapter_outline.md`.
6. ⚠️ [Ciclo de revisión automatizada] Ejecutar `scripts/validate_volume_outline.py` para la revisión.
- Revisar el esquema comparándolo con los "10 estándares principales para excelentes novelas web".
- Si la revisión falla, invocar automáticamente un Modelo de Lenguaje Extenso (LLM) para realizar revisiones.
- Repetir el ciclo "Revisar → Corregir → Volver a revisar" hasta 5 veces.
- Pasar al siguiente paso solo tras superar la revisión.
7. Pasar al paso 6 solo tras la confirmación del usuario. Verificación:
`scripts/validate_step.py --step 5 --book-name "{Book Title}" --volume {X}`

Lista de comprobación:
□ El archivo `volume_{X}_chapter_outline.md` existe.
□ `scripts/validate_volume_outline.py` se ejecutó correctamente.
□ El resultado de la revisión es "Aprobado" (o hay un informe de revisión disponible).
□ El usuario ha confirmado.
□ Incluye resúmenes de la trama para todos los capítulos del volumen.
□ [Nuevo] Sin expansión repetitiva de contenido del volumen anterior.
□ [Nuevo] Sin revelación prematura de contenido del siguiente volumen. 
□ [Nuevo] La cronología se sitúa totalmente dentro del alcance del volumen actual.
□ El usuario ha confirmado.

Punto de control: Crear tras la confirmación. `volume_{X}_outline_complete.checkpoint`
```

### Paso 6: chapter_loop (Bucle capítulo a capítulo)
```
Comprobaciones al inicio:
- ¿Es este el primer capítulo del volumen?
- ¿Existe ya el archivo `volume_{X}_chapter_outline.md` para este volumen?
- Si no es así, ejecutar primero el Paso 5.

Actualizar `status.md` al inicio:
"Tarea actual: Volumen {X}, Capítulo {Y} - A la espera de la discusión sobre el esquema del capítulo"

├─ 6.1: chapter_outline (Esquema del capítulo individual)
│   【Comprobación previa】
│     1. Leer `config/volume_{X}_chapter_outline.md` para confirmar la trama de este capítulo.
│     2. Si no es el primer capítulo, leer el capítulo anterior: `chapters/vol{X}_chapter_{Y-1}.md`.
│     3. 【Comprobación de continuidad】 Verificar la coherencia con el capítulo anterior en cuanto a cronología, estado de los personajes y progresión de la trama.
│        - Tiempo: ¿Cuándo transcurre este capítulo en relación con el anterior? (Mismo día / Día siguiente / Días después)
│        - Personajes: ¿Coinciden la ubicación y el estado al final del capítulo anterior con el inicio de este capítulo?
│        - Trama: ¿Hay elementos de anticipación (foreshadowing) del final del capítulo anterior que deban resolverse en este capítulo?
│   【Restricción de ritmo】 Escribir estrictamente siguiendo el esquema del capítulo; No comprimir ni expandir el contenido.
│
│   Salida: memory/chapter_{X}_{Y}_outline.md
│   Verificación: El archivo existe + recuento de palabras > 300
│
│   【Confirmación obligatoria】⚠️ Debe ejecutarse
│     - Tras crear el esquema del capítulo, debe hacer una pausa y presentar el contenido del esquema al usuario.
│     - Pregunte explícitamente: "Por favor, confirme el esquema del capítulo; la redacción comenzará tras la confirmación".
│     - Una vez confirmada por el usuario, actualice status.md a: "Volumen {X} Capítulo {Y} - Esquema confirmado, a la espera de redacción".
│     - ❌ Prohibido: Pasar directamente al paso 6.2 (redacción) sin confirmación.
│
├─ 6.2: chapter_write (Redacción del capítulo)
│   Requisito previo: Comprobar status.md; el estado debe ser "Esquema confirmado".
│
│   【Script de validación】⚠️ Debe superarse antes de redactar
│     python3 scripts/validate_outline_confirmation.py <BookTitle> <ChapterNumber>
│     - Fallo en la validación = Proceso detenido; primero debe confirmarse el esquema del capítulo.
│
│   【Preparación del contexto】⚠️ Debe leer el siguiente contenido antes de redactar
│
│   1. Ubicación del esquema del capítulo: config/volume_{X}_chapter_outline.md
│      - Leer los resúmenes de la trama de los tres capítulos anteriores (Capítulos Y-3, Y-2, Y-1), si existen.
│      - Leer el resumen de la trama del capítulo actual (Capítulo Y).
│      - Leer los resúmenes de la trama de los tres capítulos siguientes (Capítulos Y+1, Y+2, Y+3), si existen.
│      - ⚠️ Definir límites: Qué escribir en este capítulo, qué se ha escrito en capítulos anteriores y qué está planeado para capítulos futuros.
│      - ⚠️ Evitar repeticiones: No escribir contenido ya tratado en capítulos anteriores.
│      - ⚠️ Evitar adelantarse: No escribir contenido destinado a capítulos futuros.
│
│   2. Contenido completo del capítulo anterior (a menos que sea el primer capítulo): chapters/vol{X}_chapter_{Y-1}.md
│      - Ya incluye el final; no se requiere lectura adicional.
│      - Asegurar la continuidad temporal y la coherencia en el estado de los personajes.
│
│   3. Fichas de personajes: memory/character_cards.md (Personajes que aparecen en este capítulo)
│
│   4. Registro de presagios: memory/foreshadowing.md (Si corresponde)
│
│   5. [Directrices de estilo de escritura] ⚠️ Deben leerse y seguirse estrictamente
│      Leer: [Plantilla de estilo de escritura] en config/project_info.md
│      - Tipo de estilo: Confirmar el estilo utilizado para este capítulo
│      - Estructura de las oraciones: Longitud de los párrafos y de las oraciones
│      - Vocabulario prohibido: Estrictamente prohibido
│      - Monólogo interno/Descripción psicológica: Expresar según los requisitos de estilo
│      - Directrices de diálogo: El formato debe cumplir con lo establecido
│      - Gancho del capítulo: Debe incluir un elemento de intriga o gancho al final
│
│      [Lista de verificación de estilo de escritura] (Autocontrol durante la redacción)
│      □ No más de 3 oraciones por párrafo
│      □ No más de 15 palabras por oración
│      □ Sin uso de vocabulario prohibido
│      □ Estados internos expresados ​​mediante acciones o escenas, no adjetivos
│      □ Diálogo: Línea nueva para cada intervención hablada; máximo dos oraciones por turno
│      □ Gancho potente al final del capítulo
│      □ Nueva información o acción cada 100 caracteres
│
│   [Restricciones de alcance] ⚠️ Deben respetarse
│     - Escribir solo el contenido especificado en el esquema de este capítulo
│     - No escribir contenido ya tratado en capítulos anteriores
│     - No escribir contenido destinado a capítulos futuros
│     - Terminar con suspenso para preparar el siguiente capítulo
│
│   Salida: chapters/vol{X}_chapter_{Y}.md
│   Extensión: 3000-4000 caracteres (Obligatorio)
│
│   [Principios de escritura] ⚠️ Deben respetarse
│
│   [Requisito obligatorio: Eliminar "ismos de IA"] ⚠️ Quedan estrictamente prohibidas las siguientes estructuras oracionales características de la IA
│
│   I. Prohibición de estructuras tipo "No X, sino Y"
│     - ❌ Estrictamente prohibido: "No X, sino Y", "No es realmente X, sino Y", "Más que X, es Y"
│     - ❌ Ejemplos incorrectos: "No tenía miedo, sino ira"; "Esto no es el final, sino el comienzo"
│     - ✅ Enfoque correcto: Transmitir mediante acciones y expresiones; p. ej., "Apretó los puños, con las venas hinchadas en la frente".
│     - ✅ Enfoque correcto: Presentar mediante escenas concretas; p. ej., "La puerta se cerró; una nueva tormenta estaba a punto de comenzar".
│
│   II. Expresiones típicas de la IA prohibidas
│     - ❌ Prohibido: "En cierto sentido", "Desde cierta perspectiva", "En otras palabras"
│     - ❌ Prohibido: "Cabe destacar que", "La clave reside en", "En el fondo se trata de"
│     - ❌ Prohibido: "Por un lado... por otro lado...", "Tanto... como..." (uso excesivo)
│     - ❌ Prohibido: "Como dijo [alguien]", "Tal como..." (uso excesivo de metáforas o símiles)
│     - ❌ Prohibido: "Quizás", "Tal vez", "Posiblemente" (uso excesivo que debilita la certeza)
│     - ❌ Prohibido: "De repente", "Súbitamente", "Abruptamente" (uso excesivo para crear tensión artificial)
│     - ❌ Prohibido: "Sin embargo", "Pero", "No obstante" (introducir un contraste o giro en cada párrafo)
│     - ❌ Prohibido: "En última instancia", "Finalmente", "El resultado es" (resúmenes excesivos)
│
│   I. Priorizar las imágenes visuales
│     - Utiliza detalles y descripciones de la escena para permitir que los lectores "vean" en lugar de que se les "cuente"
│     - ❌ Incorrecto: Estaba nervioso.
│     - ✅ Correcto: Sus dedos tamborileaban involuntariamente sobre la mesa y finas gotas de sudor se formaban en su frente. │     - Involucra los cinco sentidos: vista, oído, olfato, tacto y gusto
│
│   II. Crear inmersión
│     - Sitúa al lector en la escena; permítele sentir las emociones y situaciones de los personajes
│     - Describe la atmósfera: iluminación, temperatura, olores y sonidos
│     - Transmite información a través de las experiencias sensoriales de los personajes
│
│   III. Conflicto y tensión
│     - Cada escena debe contener conflicto o suspenso
│     - Tipos de conflicto: interpersonal, persona contra el entorno y conflicto interno
│     - Termina la escena con un final en suspenso (*cliffhanger*) o un gancho narrativo
│
│   IV. Diálogo atractivo
│     - El diálogo debe hacer avanzar la trama y revelar rasgos de los personajes
│     - ❌ Incorrecto: "¿Qué opinas?" "No creo que sea muy bueno."
│     - ✅ Correcto: "¿Qué opinas?" Tomó su taza de té, aunque su mirada no se posó en la otra persona. │     - Interrumpir el diálogo con acciones y expresiones para evitar un ritmo repetitivo de «ida y vuelta».
│     - Incluir subtexto en el diálogo; no explicar explícitamente cada significado.
│
│   V. Control del ritmo
│     - Alternar entre oraciones largas y cortas para evitar la monotonía.
│     - Usar oraciones cortas en escenas de acción para generar tensión.
│     - Usar oraciones largas en escenas emocionales para establecer la atmósfera.
│     - Mantener los párrafos concisos para facilitar la lectura.
│
│   VI. El arte del «espacio en blanco» (sutileza)
│     - No escribir todo de forma explícita.
│     - Permitir que los lectores usen su imaginación y hagan inferencias.
│     - Usar insinuaciones y sugerencias en lugar de afirmaciones directas.
│
│   VII. Un inicio cautivador
│     - Incluir un «gancho» justo al principio.
│     - Opciones: suspenso, conflicto, diálogo o una escena específica.
│     - Evitar comenzar con una larga exposición de antecedentes.
│
│   VIII. Resonancia emocional
│     - Lograr que a los lectores les importe el destino de los personajes.
│     - Revelar las vulnerabilidades y los dilemas de los personajes.
│     - Usar eventos concretos en lugar de descripciones abstractas.
│

IX. Gancho final ⚠️ Debe dejar un gancho para el siguiente capítulo
- El final debe conectar estrechamente con el siguiente capítulo, dejando un gancho claro.
- Tipos de ganchos:
- Gancho de suspenso: Una pregunta sin resolver («Pasos tras la puerta... ¿quién será?»).
- Gancho de acción: Una acción inminente de un personaje («Se puso en pie y caminó hacia la puerta de la prisión»).
- Gancho de diálogo: Terminar con un diálogo que insinúe lo que está por venir («—Mi señor, el emisario ha llegado»).
- Gancho de noticias: Entrega de información importante («Llegaron noticias del Palacio Ganquan: el adivino había avistado un presagio celestial inusual»).
- Gancho de escena: Un cambio de escena que insinúe una transformación («A lo lejos, el sonido de cascos se acercaba»).
- Ser específico; evita las generalizaciones (❌ "Se acerca una tormenta" → ✅ "Se oye el galope de cascos; las tropas de Guo Rang han llegado").
- Apunta a eventos específicos del próximo capítulo, haciendo que los lectores se pregunten «qué pasará después».
- No resumas el capítulo actual; en su lugar, genera suspense para el siguiente.
│   Verificación (todos los puntos deben cumplirse):
│     1. Validación básica:
│        scripts/validate_step.py --step 6 --chapter {X}_{Y} --book-name "{Book Title}"
│        □ El archivo existe
│        □ Recuento de palabras en el rango de 3000 a 4000
│        □ El inicio presenta puntuación o diálogo
│        □ Incluye descripciones sensoriales
│        □ Incluye diálogo
│
│     2. ⚠️ [Nuevo] Revisión según los 10 estándares para novelas web excelentes (obligatorio):
│        scripts/validate_chapter_quality.py "{Book Title}" "{X}_{Y}"
│        □ Inicio atractivo (2 puntos): suspense, conflicto o intriga en los primeros 3 párrafos
Introducción
│        □ Ritmo ágil (2 pts) - Un clímax menor cada 3-5 párrafos
│        □ Conflicto en cada capítulo (2 pts) - Al menos 2 conflictos
│        □ Motivación de los personajes (2 pts) - Motivaciones claras para el protagonista y el antagonista
│        □ Diálogo atractivo (2 pts) - El diálogo impulsa la trama; contiene subtexto
│        □ Gancho final (2 pts) - Genera suspenso para el siguiente capítulo
│        □ Densidad de información (2 pts) - Información nueva cada 100 palabras
│        □ Imágenes visuales/sensoriales (2 pts) - Descripciones que involucran los cinco sentidos
│        □ Emoción auténtica (2 pts) - Emociones con profundidad o matices
│        □ Sin "toque de IA" (2 pts) - Natural y fluido; sin rastros de escritura por IA
│
│        Criterios de puntuación:
│        - 80-100% (16-20 pts): Excelente 🌟
│        - 60-79% (12-15 pts): Bueno ✅ (Aprobado)
│        - 40-59% (8-11 pts): Aprobado ⚠️ (Se recomienda revisión)
│        - <40% (<8 pts): No aprobado ❌ (Requiere reescritura)
│
│   Actualización: status.md = "Volumen {X} Capítulo {Y} - Completado, pendiente de revisión"
│   Punto de control: Crear chapter_{X}_{Y}_complete.checkpoint
│   ⚠️ Ejecutar 6.3 inmediatamente al finalizar; no se puede omitir
│
├─ 6.3: character_check (Verificación de personajes) ⚠️ Obligatorio tras cada capítulo
│   【Activador】Ejecución automática inmediatamente después del paso 6.2; no se puede omitir
│   【Acción】Verificar los personajes que aparecen en este capítulo; crear fichas para los nuevos personajes
│   【Proceso】
│     1. 【Extraer personajes】Analizar el contenido del capítulo; extraer la lista de todos los personajes que aparecen
│     2. 【Contrastar con fichas de personajes】Leer memory/character_cards.md; marcar personajes sin ficha
│     3. 【Evaluar importancia】Para personajes sin ficha:
│        - Leer config/volume_outline.md (Esquema del volumen)
│        - Leer config/volume_{X}_chapter_outline.md (Esquema detallado de este volumen)
│        - Buscar el nombre del personaje para determinar si aparece en capítulos posteriores
│        - Si aparece ≥2 veces → Personaje importante; se debe crear una ficha de personaje
│        - Si aparece solo una vez → Personaje menor o funcional; la creación es opcional
│     4. [Crear ficha de personaje] Crear una ficha para los personajes importantes, incluyendo:
│        - id: ID basado en Pinyin
│        - name: Nombre completo
│        - roles: Lista de identidades/roles
│        - significance: Papel en la historia
│        - key_events: Eventos clave (opcional)
│     5. [Actualizar mapa de relaciones] Actualizar relationship_map.md si hay nuevas relaciones entre personajes
│   [Salida] Actualizar memory/character_cards.md (si es necesario)
│   [Verificación] Confirmar que todos los personajes importantes tienen ficha
│   [Al finalizar] Proceder al paso 6.4 para esperar la revisión del usuario
│
├─ 6.4: user_review (Revisión del usuario)
│   Satisfecho → Proceder al siguiente capítulo
│   Requiere revisiones → Volver al paso 6.1 o 6.2
│   Evolución: Registrar en lessons_learned.md (comentarios del usuario, áreas de mejora)
│
└─ 6.5: volume_complete (Verificación de finalización del volumen)
Volumen incompleto → Volver al paso 6.1 para discutir el siguiente capítulo
Volumen terminado → Confirmación del usuario, crear punto de control del volumen, proceder al siguiente volumen (Paso 5)
```

### Paso 7: final_assemble (Compilación final)
```
Acción: Fusionar todos los capítulos
Salida:
- deliverables/final.md
- deliverables/final.docx (opcional)

Verificación:
scripts/validate_step.py --step 6 --book-name "{Título del libro}"

Lista de comprobación:
□ Existe final.md
□ Incluye todos los capítulos
□ El recuento total de palabras cumple con las expectativas
```

---

## Uso del script de verificación

**Debe ejecutarse antes de cada transición de paso**:

```bash
# Verificar el paso 2 (Inicialización del proyecto)
python3 scripts/validate_step.py --step 2 --book-name "He Raised the Emperor"

# Verificar el paso
3 (Construcción del mundo)
python3 scripts/validate_step.py --step 3 --book-name "He Raised the Emperor"

# Validar el paso 5 (Escritura del capítulo)
python3 scripts/validate_step.py --step 5 --chapter 1_01 --book-name
``` "Crié al Emperador"
```

**Valores de retorno**:
- 0 = Validación superada
- 1 = Validación fallida (se mostrarán errores específicos)

---

## Mecanismo de puntos de control (Checkpoint)

**Crear punto de control**:
```bash
python3 scripts/checkpoint.py create --book-name "{Nombre del libro}" --name "step_3_complete"
```

**Revertir al punto de control**:
```bash
python3 scripts/checkpoint.py rollback --book-name "{Nombre del libro}" --name "step_3_complete"
```

**Ubicación de almacenamiento de puntos de control**:
```
~/Documents/{Nombre del libro}/memory/checkpoints/
├── step_2_complete.checkpoint
├── step_3_complete.checkpoint
├── step_4_complete.checkpoint
└── chapter_1_01_complete.checkpoint
```

---

## Mecanismo de evolución

**Tras completar cada capítulo**, escribe en `memory/lessons_learned.md`:
```markdown
## Capítulo: Volumen 1, Capítulo 1

### Comentarios del usuario/Revisiones
- El ritmo al principio era demasiado lento
- La entrada del protagonista carecía de impacto

### Áreas de mejora
- Introducir conflicto en los primeros 3 párrafos del siguiente capítulo
- Aumentar la tensión en los diálogos de los personajes

### Conclusiones clave
- Presagio (foreshadowing) exitoso: Identidad del misterioso anciano
- Recuento de palabras bien gestionado: 3.200 palabras
```

**Tras completar cada volumen**, genera `memory/volume_{X}_retrospective.md`:
```markdown
## Retrospectiva del Volumen 1

### Ejecución de la temática
- Progresión del conflicto central
- Cierre del arco emocional

### Desarrollo de personajes
- Trayectoria de crecimiento del protagonista
- Evaluación de personajes secundarios

### Seguimiento de presagios (foreshadowing)
- Plantados: 5 casos
- Resueltos: 2 casos
- Pendientes de resolución: 3 elementos (a tratar en el Volumen 2)

### Plan de mejora
- Acelerar el ritmo en el Volumen 2
- Aumentar el tiempo en escena del/los antagonista(s)
```

---

## Gestión de errores

### Fallo de validación
1. Detener el proceso actual
2. Mostrar detalles específicos del error
3. Esperar instrucciones del usuario (las correcciones, reversiones u omisiones requieren una acción explícita del usuario) autorización)

### Fallo en la ejecución de una sub-tarea
1. Reintentar 3 veces
2. Si el fallo persiste → Intervención manual
3. Opción de revertir al punto de control anterior

### Insatisfacción del usuario
1. Registrar comentarios/notas de revisión en `lessons_learned.md`
2. Iterar las revisiones hasta lograr la satisfacción
3. Revalidar tras cada revisión

---

## Formato del archivo de estado (`status.md`)

```markdown
# {Título del libro} - Estado de la escritura

**Etapa actual**: Paso 5 - chapter_loop
**Tarea actual**: Volumen 1, Capítulo 3 - Esquema del capítulo confirmado; pendiente de redacción
**Última actualización**: 2026-03-04 12:30

## Estadísticas de progreso
- Capítulos completados: 2
- Recuento actual de palabras: 6.500 palabras
- Recuento objetivo de palabras: 300.000 palabras

## Registro de puntos de control
- 2026-03-04 10:00: step_3_complete.checkpoint
- 2026-03-04 11:00: step_4_complete.checkpoint
- 2026-03-04 12:00: chapter_1_02_complete.checkpoint

## Registro de confirmación del usuario
- 2026-03-04 11:00: Esquema del volumen confirmado
- 2026-03-04 12:00: Esquema del Volumen 1, Capítulo 1 confirmado
```

---

## Uso

Activar diciendo "Quiero escribir una novela". **Empezar desde cero**: Comenzar en el Paso 0
**Continuar escribiendo**: Leer `status.md` y reanudar desde el estado registrado
**Reanudar la escritura**: Opción de revertir a un punto de control específico

---

**Recuerda**: No está terminado sin verificación, y no es correcto sin revisión.
