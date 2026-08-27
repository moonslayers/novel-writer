#!/usr/bin/env python3
"""
Script de revisión de calidad de capítulos de novel-writer - Los 10 grandes estándares de la ficción.
Uso: python3 validate_chapter_quality.py <NombreDelLibro> <NumeroDeCapitulo>
"""

import sys
import re
from pathlib import Path

def get_project_path(book_name):
    """Obtiene la ruta del proyecto"""
    paths = [
        Path.home() / ".openclaw" / "workspace" / "content-projects" / book_name,
        Path.home() / "Documents" / book_name,
        Path.cwd() / book_name,
    ]
    for path in paths:
        if path.exists():
            return path
    return None

def load_chapter(project_path, chapter_code):
    """Carga el contenido del capítulo"""
    chapter_parts = chapter_code.split('_')
    if len(chapter_parts) != 2:
        return None
    volume, chapter_num = chapter_parts
    chapter_file = project_path / "chapters" / f"vol{volume}_chapter_{chapter_num}.md"
    if not chapter_file.exists():
        return None
    return chapter_file.read_text(encoding='utf-8')

def check_opening_hook(content):
    """Estándar 1: Gancho inicial - Los primeros 3 párrafos deben atrapar"""
    lines = content.split('\n')
    first_3_paragraphs = '\n'.join([l for l in lines[:15] if l.strip()][:3])
    
    # Buscar suspense, conflicto o emoción (adaptado a español y signos de interrogación/exclamación invertidos)
    hook_patterns = [
        r'[¿?¡!]',
        r'[""«»]',
        r'(muert|sangr|matar|muer|colaps|desesper|sorpresa|impacto|asombro|shock)',
        r'(per|sin embargo|de repente|súbitamente|inesperadamente|cuando menos)',
    ]
    
    hook_score = 0
    for pattern in hook_patterns:
        if re.search(pattern, first_3_paragraphs, re.IGNORECASE):
            hook_score += 1
    
    return min(hook_score, 2)  # Máximo 2 puntos

def check_pacing(content):
    """Estándar 2: Ritmo紧凑 (compacto) - Un mini-clímax cada 3-5 párrafos"""
    paragraphs = [p for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
    
    # Marcadores de clímax (conflicto, giros, diálogos intensos)
    climax_markers = ['"', '"', '«', '»', '¿', '?', '¡', '!', 'de repente', 'per', 'sin embargo', 'entonces', 'como resultado']
    
    climax_count = 0
    for para in paragraphs:
        if any(marker in para.lower() for marker in climax_markers):
            climax_count += 1
    
    # Promedio esperado: 1 clímax cada 5 párrafos
    expected_climax = len(paragraphs) / 5
    ratio = climax_count / max(expected_climax, 1)
    
    return min(int(ratio * 2), 2)  # Máximo 2 puntos

def check_conflict(content):
    """Estándar 3: Conflicto en cada capítulo - Al menos 2 conflictos"""
    conflict_patterns = [
        r'(desacuerdo|insatisfacción|rabia|enfado|ira|rebatir|refutar|reprochar|confrontar)',
        r'(rechaz|negativ|oposición|resistenci|luch|pele|discut)',
        r'(contradicción|conflict|oposición|luch|tensión)',
        r'[""«»].*?(no|nunca|jamás|vete|lárgate|idiota|estúpido|basura|maldición|caraj)[""«»]',
    ]
    
    conflict_count = 0
    for pattern in conflict_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            conflict_count += 1
    
    return min(conflict_count, 2)  # Máximo 2 puntos

def check_character_motivation(content):
    """Estándar 4: Motivación de personajes - Protagonista y antagonista con motivos claros"""
    motivation_markers = [
        r'(para|porque|quier|dese|esperanz|ilusión|tem|mied|preocupación)',
        r'(por qué|cómo es posible|qué diablos|qué pasa|qué demonios)',
        r'(no me rindo|no me conform|quier|debo|tengo que|necesito|exijo|juro)',
    ]
    
    motivation_count = 0
    for marker in motivation_markers:
        if re.search(marker, content, re.IGNORECASE):
            motivation_count += 1
    
    return min(motivation_count, 2)  # Máximo 2 puntos

def check_dialogue(content):
    """Estándar 5: Diálogos con chispa - Impulsan la trama, tienen subtexto"""
    # Extraer todos los diálogos (usando comillas latinas y españolas)
    dialogues = re.findall(r'[""«»]([^""«»]+)[""«»]', content)
    
    if len(dialogues) < 3:
        return 0
    
    # Verificar si los diálogos son dinámicos (cortos y con pronombres personales)
    good_dialogue = 0
    for dialogue in dialogues:
        # Diálogos cortos (< 60 chars) que incluyen interacción (tú, yo, me, te)
        if len(dialogue) < 60 and re.search(r'\b(tú|vos|usted|yo|me|te|se|nos)\b', dialogue, re.IGNORECASE):
            good_dialogue += 1
    
    ratio = good_dialogue / max(len(dialogues), 1)
    return min(int(ratio * 2), 2)  # Máximo 2 puntos

def check_ending_hook(content):
    """Estándar 6: Gancho final - Debe dejar suspense para el siguiente capítulo"""
    last_lines = '\n'.join(content.split('\n')[-10:])
    
    hook_patterns = [
        r'[¿?¡!]',
        r'(per|sin embargo|de repente|súbitamente|inesperadamente|resulta que|al final|para sorpresa)',
        r'(esper|lleg|son|vibr|retumb|escuch|pasos)',
        r'(puert|teléfon|móvil|celular|mensaj|voz|sonid|ruid|llamad)',
        r'[(（]Fin del capítulo.*[)）]',
    ]
    
    hook_score = 0
    for pattern in hook_patterns:
        if re.search(pattern, last_lines, re.IGNORECASE):
            hook_score += 1
    
    return min(hook_score, 2)  # Máximo 2 puntos

def check_information_density(content):
    """Estándar 7: Densidad de información - Nueva información cada ~100 palabras"""
    # En español contamos PALABRAS, no caracteres como en chino
    spanish_words = len(re.findall(r'\b\w+\b', content))
    
    # Puntos de nueva información (números, giros, revelaciones)
    info_patterns = [
        r'\d+',
        r'(per|sin embargo|de repente|inesperadamente|resulta que|al final|sin embargo)',
        r'(descubr|enter|darse cuenta|comprend|entend|revel|saber|notar)',
    ]
    
    info_count = 0
    for pattern in info_patterns:
        info_count += len(re.findall(pattern, content, re.IGNORECASE))
    
    # Promedio esperado: 1 punto de información cada 100 palabras
    expected_info = spanish_words / 100
    ratio = info_count / max(expected_info, 1)
    
    return min(int(ratio * 2), 2)  # Máximo 2 puntos

def check_imagery(content):
    """Estándar 8: Imágenes sensoriales - Descripciones de los 5 sentidos"""
    sensory_words = {
        'visual': ['vi', 'mir', 'luz', 'color', 'sombr', 'brill', 'oscur', 'blanc', 'nej', 'rj'],
        'auditivo': ['oí', 'escuch', 'sonid', 'ru', 'estruend', 'zumb', 'silenci', 'ruid', 'campan'],
        'olfativo': ['ol', 'arom', 'hedor', 'perfum', 'huel', 'apesta'],
        'táctil': ['tact', 'toc', 'sensación', 'frí', 'calient', 'tibio', 'cálid', 'tembl', 'escalofrí', 'eriz'],
        'gustativo': ['sabore', 'com', 'beb', 'dulc', 'amarg', 'ácid', 'picant', 'salad', 'sabor'],
    }
    
    sensory_count = 0
    for category, words in sensory_words.items():
        if any(word in content.lower() for word in words):
            sensory_count += 1
    
    return min(sensory_count, 2)  # Máximo 2 puntos

def check_emotion(content):
    """Estándar 9: Emociones reales - Las emociones tienen capas y matices"""
    emotion_words = [
        r'(ilusión|emocion|alegr|feliz|content|sonre|rí)',
        r'(sorprend|asombr|impact|estupefact|atónit|paraliz|petrificad)',
        r'(rabia|enfado|ira|furios|enojad|maldic|maldit|caraj|demonios)',
        r'(tristez|dolor|decepción|desesperación|angustia|pena|llor|lágrim)',
        r'(impotenci|cansanci|agotad|fatiga|incapaz|silenci|mud|resignación)',
        r'(esperanz|dese|decisión|determinación|firme|convicción|resolv)',
    ]
    
    emotion_count = 0
    for pattern in emotion_words:
        if re.search(pattern, content, re.IGNORECASE):
            emotion_count += 1
    
    return min(emotion_count, 2)  # Máximo 2 puntos

def check_ai_flavor(content):
    """Estándar 10: Eliminar rastro de IA - Lenguaje natural y fluido"""
    # Muletillas y estructuras típicas que delatan a la IA en español
    ai_patterns = [
        r'(En cierto sentido|Desde cierta perspectiva|En cierto modo)',
        r'(Cabe destacar|Es importante señalar|La clave está|El punto crucial|Vale la pena mencionar)',
        r'(Por un lado.*por otro lado|Tanto.*como.*per)',
        r'(Además|Asimismo|Por otro lado|Simultáneamente|Por lo tant|En consecuencia|Por ende|Así que)',
        r'(En conclusión|Finalmente|Para terminar|El resultado fue|El desenlace)',
        r'(background music|AI|LLM|prompt|como modelo de lenguaje)', # Palabras en inglés o meta-referencias
    ]
    
    ai_count = 0
    for pattern in ai_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            ai_count += 1
    
    # A mayor cantidad de patrones de IA, menor puntuación
    return max(2 - ai_count, 0)  # Máximo 2 puntos

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 validate_chapter_quality.py <NombreDelLibro> <NumeroDeCapitulo>")
        print("Ejemplo: python3 validate_chapter_quality.py El_Caballero_Audaz 1_01")
        sys.exit(1)
    
    book_name = sys.argv[1]
    chapter_code = sys.argv[2]
    
    project_path = get_project_path(book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{book_name}'")
        sys.exit(1)
    
    content = load_chapter(project_path, chapter_code)
    if not content:
        print(f"❌ Error: No se encontró el archivo del capítulo '{chapter_code}'")
        sys.exit(1)
    
    print(f"🔍 Revisión de los 10 grandes estándares de ficción: '{book_name}' Capítulo {chapter_code}")
    print("=" * 70)
    
    # Ejecutar las 10 verificaciones
    checks = [
        ("Gancho inicial", check_opening_hook, "Suspense/conflicto en los primeros 3 párrafos"),
        ("Ritmo", check_pacing, "Un mini-clímax cada 3-5 párrafos"),
        ("Conflicto", check_conflict, "Al menos 2 conflictos en el capítulo"),
        ("Motivación", check_character_motivation, "Motivos claros del protagonista/antagonista"),
        ("Diálogos", check_dialogue, "Diálogos que impulsan la trama, con subtexto"),
        ("Gancho final", check_ending_hook, "Deja suspense para el siguiente capítulo"),
        ("Densidad info", check_information_density, "Nueva información cada ~100 palabras"),
        ("Sensorial", check_imagery, "Descripciones que apelan a los 5 sentidos"),
        ("Emociones", check_emotion, "Emociones con capas y matices reales"),
        ("Cero IA", check_ai_flavor, "Lenguaje natural, sin muletillas de IA"),
    ]
    
    total_score = 0
    max_score = 0
    
    for name, check_func, desc in checks:
        score = check_func(content)
        total_score += score
        max_score += 2
        
        status = "✓" if score >= 1 else "⚠"
        bar = "█" * score + "░" * (2 - score)
        
        print(f"{status} {name:<15} [{bar}] {score}/2 - {desc}")
    
    print("=" * 70)
    percentage = (total_score / max_score) * 100
    
    if percentage >= 80:
        level = "¡Excelente!"
        emoji = "🌟"
    elif percentage >= 60:
        level = "Bueno"
        emoji = "✅"
    elif percentage >= 40:
        level = "Aceptable"
        emoji = "⚠️"
    else:
        level = "Requiere reescritura"
        emoji = "❌"
    
    print(f"{emoji} Puntuación total: {total_score}/{max_score} ({percentage:.1f}%) - {level}")
    
    if percentage < 80:
        print("\n💡 Sugerencias de mejora para el Agente:")
        if check_opening_hook(content) < 2:
            print("  - Refuerza el gancho inicial, añade más suspense o conflicto al principio.")
        if check_pacing(content) < 2:
            print("  - Acelera el ritmo, introduce un mini-clímax o giro cada pocos párrafos.")
        if check_conflict(content) < 2:
            print("  - Aumenta el conflicto, haz que el protagonista se enfrente activamente a obstáculos.")
        if check_character_motivation(content) < 2:
            print("  - Aclara la motivación de los personajes, añade más monólogo interno o deseos.")
        if check_dialogue(content) < 2:
            print("  - Mejora los diálogos, que tengan subtexto y hagan avanzar la trama.")
        if check_ending_hook(content) < 2:
            print("  - Refuerza el gancho final, deja una pregunta o evento sin resolver.")
        if check_information_density(content) < 2:
            print("  - Aumenta la densidad de información, revela detalles del mundo o trama constantemente.")
        if check_imagery(content) < 2:
            print("  - Añade descripciones sensoriales (vista, oído, tacto, olfato, gusto).")
        if check_emotion(content) < 2:
            print("  - Profundiza en las emociones, muestra reacciones físicas y matices psicológicos.")
        if check_ai_flavor(content) < 2:
            print("  - Elimina el 'sabor a IA': quita frases como 'Cabe destacar', 'En conclusión', 'Por un lado'.")
    
    print("\n✅ Revisión de calidad completada.")
    return 0 if percentage >= 60 else 1

if __name__ == "__main__":
    sys.exit(main())
