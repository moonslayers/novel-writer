# novel-writer | Motor de creación de novelas con IA v3.0

Este es un proyecto de tipo "Skills" diseñado para automatizar **todo el flujo de trabajo de escritura de una novela completa: desde el concepto inicial hasta el manuscrito final**. Simplemente describes la historia que quieres escribir utilizando lenguaje natural y la IA se encarga de todo el proceso: **conceptualización, construcción del mundo, diseño de personajes, esquematización de capítulos, redacción capítulo a capítulo y compilación del manuscrito final**.

Compatible con los principales editores de IA: Antigravity, Trae, Claude Code, Open Code y Cursor. ![ai_novel](assets/ai_novel.jpg)

***

## Capacidades

| Funcionalidad | Descripción |
| :--- | :--- |
| **Ideación creativa** | Discute con la IA elementos clave como el título del libro, la extensión, la perspectiva y el tono emocional |
| **Construcción del mundo** | Genera automáticamente documentos de ambientación para la época, ubicaciones clave, sistemas y normas sociales |
| **Diseño de personajes** | Crea fichas de personajes estructuradas (formato YAML) y mapas de relaciones entre personajes |
| **Esquema de volúmenes** | Diseña temas, conflictos centrales y arcos emocionales para tres volúmenes |
| **Esquemas de capítulos** | Genera resúmenes de la trama para todos los capítulos de cada volumen, siguiendo cuatro principios clave de progresión |
| **Redacción capítulo a capítulo** | Escribe automáticamente entre 2.500 y 3.500 palabras por capítulo, garantizando imágenes vívidas, inmersión y tensión conflictiva |
| **Verificación de personajes** | Identifica automáticamente nuevos personajes tras cada capítulo y crea fichas para los personajes clave |
| **Seguimiento de presagios** | Registra automáticamente los presagios introducidos para asegurar la coherencia narrativa |
| **Evolución de la experiencia** | Registra los comentarios y revisiones del usuario para mejorar continuamente la calidad de la escritura |
| **Mecanismo de puntos de control** | Crea automáticamente instantáneas en hitos clave; permite revertir cambios y recuperar el estado en cualquier momento |
| **Compilación final** | Fusiona todos los capítulos para generar los archivos `final.md` y `final.docx` | ***

## Limitaciones

- **No es una máquina de escritura totalmente automatizada** — Los hitos clave (esquemas de capítulos o volúmenes) requieren la confirmación del usuario antes de continuar.
- **No sustituye la revisión humana** — Se requiere la revisión y corrección por parte del usuario, basada en la retroalimentación, tras completar cada capítulo.
- **Sin garantía de calidad de publicación** — El contenido generado requiere un pulido humano para cumplir con los estándares de publicación.
- **Sin soporte multilingüe** — Actualmente optimizado principalmente para novelas extensas en chino.
- **Sin búsqueda web en tiempo real** — La construcción del mundo narrativo se basa en el conocimiento previo de la IA; los usuarios deben proporcionar material para temas especializados.

***

## 🚀 Inicio rápido

### 1. Instalar la Skill

**🤖 Antigravity / Gemini Code Assist:**

```bash
git clone https://github.com/AI-Practical-Lab/novel-writer.git .agent/skills/novel-writer

```

**🚀 Trae IDE:**

```bash
git clone https://github.com/AI-Practical-Lab/novel-writer.git .trae/skills/novel-writer
```

**🧠 Claude Code:**

```bash
git clone https://github.com/AI-Practical-Lab/novel-writer.git .claude/skills/novel-writer
```

**💻 Cursor / VSCode / General:**

```bash
git clone https://github.com/AI-Practical-Lab/novel-writer.git skills/novel-writer
```

### 2. Prueba a interactuar con la IA de esta manera

**Iniciar una nueva novela**

> "Quiero escribir una novela."

**Escribir en un género específico**

> "Ayúdame a escribir una novela romántica histórica extensa; hazla conmovedora."

**Continuar un trabajo anterior**

> "Continúa escribiendo *He Raised the Emperor*."

**Comprobar el progreso actual**

> "¿En qué punto de la novela estamos?"

**Volver a un punto de control**

> "Vuelve al estado posterior a la finalización del Capítulo 3."

**Revisar un capítulo escrito**

> "El ritmo del Capítulo 5 es demasiado lento; ayúdame a reescribirlo."

***

## 📦 Configuración del entorno

### Ruta de salida del proyecto

**Regla de ruta**: `~/Documents/{Título del libro}/`

- El nombre del directorio debe utilizar **únicamente caracteres chinos** y coincidir exactamente con el título del libro.
- Ejemplo: *He Raised the Emperor* → `~/Documents/他养大了皇帝/`

**Estructura de directorios**:

```
~/Documents/{Título del libro}/
├── config/
│   ├── project_info.md ​​​​       # Metadatos del proyecto
│   ├── worldbuilding.md       # Configuración de la construcción del mundo
│   ├── characters.md          # Perfiles de personajes
│   └── volume_outline.md      # Esquema del volumen
├── memory/
│   ├── character_cards.md     # Fichas de personajes (formato YAML)
│   ├── relationship_map.md    # Mapa de relaciones entre personajes
│   ├── foreshadowing.md       # Seguimiento de presagios (foreshadowing)
│   ├── lessons_learned.md     # Lecciones de escritura acumuladas
│   └── checkpoints/           # Instantáneas de puntos de control
├── chapters/
│   ├── vol1_chapter_01.md
│   ├── vol1_chapter_02.md
│   └── ...
├── deliverables/
│   ├── final.md               # Borrador consolidado
│   └── final.docx             # Documento exportado
└── status.md                  # Estado actual (Fuente única de verdad)
```

***

## 📂 Descripción de las carpetas

- `SKILL.md`: Instrucciones detalladas para la IA, incluyendo la máquina de estados y las reglas de validación obligatorias.
- `README.md`: Este documento (para el usuario).
- `scripts/`: Scripts de validación y gestión de puntos de control.
- `validate_step.py`: Script de validación obligatoria; debe ejecutarse en cada paso
- `checkpoint.py`: Creación de puntos de control y reversión
- `workflow.py`: Gestión del flujo de trabajo
- `sub-skills/`: Directorio de subhabilidades
- `novel-init/`: Inicialización del proyecto
- `novel-brainstorm/`: Lluvia de ideas creativa
- `novel-setup/`: Configuración del proyecto
- `novel-memory-load/`: Carga de memoria
- `novel-chapter-frame/`: Esquema/estructura del capítulo
- `novel-chapter-write/`: Escritura del capítulo
- `novel-chapter-character/`: Revisión de personajes
- `novel-chapter-update/`: Actualización del capítulo
- `novel-check-quality/`: Control de calidad

***

## ⚠️ Explicación de los mecanismos fundamentales

### Mecanismo de validación obligatoria

El script de validación debe ejecutarse tras completar cada paso; un fallo detiene el flujo de trabajo:

```bash
# Validar paso 2 (Inicialización del proyecto)
python scripts/validate_step.py --step 2 --book-name "BookTitle"

# Validar paso 3 (Construcción del mundo)
python scripts/validate_step.py --step 3 --book-name "BookTitle"

# Validar redacción del capítulo
python scripts/validate_step.py --step 6 --chapter 1_01 --book-name "BookTitle"
```

### Mecanismo de puntos de control (checkpoint)

Se crean instantáneas automáticamente en hitos clave, lo que permite revertir el estado en cualquier momento:

```bash
# Crear punto de control
python scripts/checkpoint.py create --book-name "Book Title" --name "step_3_complete"

# Revertir a un punto de control
python scripts/checkpoint.py rollback --book-name "Book Title" --name "step_3_complete"
```

### Flujo de trabajo de la máquina de estados

```
Paso 0: init → Paso 1: brainstorm → Paso 2: project_init
→ Paso 3: world_building → Paso 4: volume_outline
→ Paso 5: volume_chapter_outline → Paso 6: chapter_loop
→ Paso 7: final_assemble
```

### Cuatro principios de la progresión de la trama del capítulo

1. **Principio de cadena de causalidad**: La crisis de cada capítulo debe surgir de un problema latente en el capítulo anterior.
2. **Principio de elección y coste**: El protagonista debe tomar una decisión clara en cada capítulo, y toda elección conlleva un coste.
3. **Principio de escalada**: Las crisis deben intensificarse progresivamente; está prohibido repetir una crisis del mismo nivel.
4. **Principio de ritmo y ponderación**: El ritmo se refleja en el número de capítulos asignados a las fases de transición, preparación, clímax y conclusión.

***

## ⚠️ Preguntas frecuentes

1. **¿Cómo consulto el progreso actual de la escritura?**
Revisa el archivo `~/Documents/{Book Title}/status.md`; esta es la fuente única de información.
2. **¿Cómo modifico un capítulo que ya he escrito?**
Indícale a la IA: "Ayúdame a revisar el capítulo X". La IA lo reescribirá basándose en tus comentarios y registrará los cambios en `lessons_learned.md`.
3. **¿Qué pasa si falla la validación?**
El script de validación mostrará errores específicos; corrige los problemas siguiendo las indicaciones y vuelve a ejecutar la validación.
4. **¿Puedo saltarme un paso?**
No. Un mecanismo de validación obligatorio garantiza que cada paso se complete antes de pasar al siguiente.
5. **¿Cómo retomo el trabajo anterior?**
Dile a la IA: "Continúa escribiendo '[Título del libro]'"; leerá automáticamente `status.md` y retomará la tarea desde el último punto de control.
6. **¿Qué pasa si quiero revertir cambios a mitad del proceso?**
Dile a la IA: "Vuelve al punto de control XXX", y regresará al estado de dicho punto. ***

## 🔄 Cómo actualizar

Cuando se lancen nuevas funciones, podrás actualizar con un solo comando:

```bash
cd .trae/skills/novel-writer
git pull
```

***

## 🌟 Características principales (V3.0)

- **Verificación obligatoria**: Cada paso debe superar un script de verificación para garantizar la integridad del proceso.
- **Sistema de puntos de control**: Se crean instantáneas automáticamente en hitos clave, lo que facilita la reversión y recuperación.
- **Mecanismo de evolución**: Se registran los comentarios y ediciones del usuario para mejorar continuamente la calidad de la escritura.
- **Seguimiento de personajes**: Detecta automáticamente nuevos personajes y mantiene un mapa de relaciones entre ellos.
- **Gestión de presagios**: Registra automáticamente las tramas sembradas para asegurar la coherencia narrativa.
- **Conciencia del contexto**: Hace referencia automática al texto anterior, a los perfiles de personajes y a los detalles de los presagios mientras escribe.
- **Restricciones de calidad**: Cumple con ocho principios clave de escritura, incluyendo el control de extensión (2.500–3.500 palabras por capítulo), imágenes visuales, inmersión y tensión narrativa.

***

## Apoya el proyecto

Si este proyecto te resulta útil, considera apoyarlo. Tu apoyo impulsa directamente su desarrollo y mantenimiento continuos.
![good](assets/good.jpg)
