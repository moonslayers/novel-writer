#!/usr/bin/env python3
"""
Script de validación de pasos de novel-writer - Validación obligatoria de cada etapa.
Uso: python3 validate_step.py --step <N> --book-name "NombreDelLibro" [--chapter X_Y]
"""

import argparse
import os
import sys
import re
from pathlib import Path

def get_project_path(book_name):
    """Obtiene la ruta del proyecto"""
    # Prioridad: workspace, luego Documents, luego directorio actual
    paths = [
        Path.home() / ".openclaw" / "workspace" / "content-projects" / book_name,
        Path.home() / "Documents" / book_name,
        Path.cwd() / book_name,  # Añadido: también busca en el directorio actual
    ]
    for path in paths:
        if path.exists():
            return path
    return None

def validate_step_0(args):
    """Valida Step 0: init"""
    print("✓ Step 0: La fase de inicialización no requiere validación")
    return True

def validate_step_1(args):
    """Valida Step 1: brainstorm - Los 5 elementos deben estar confirmados"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    status_file = project_path / "status.md"
    if not status_file.exists():
        print(f"❌ Error: status.md no existe")
        return False
    
    content = status_file.read_text(encoding='utf-8')
    
    checks = [
        ("Título confirmado", r"(?:título|nombre).*(?:confirmado|aprobado|definido)"),
        ("Extensión confirmada", r"(?:extensión|longitud|duración).*(?:confirmado|aprobado|definido)"),
        ("Perspectiva confirmada", r"(?:perspectiva|narrador|punto de vista).*(?:confirmado|aprobado|definido)"),
        ("Alcance confirmado", r"(?:alcance|ámbito|cobertura).*(?:confirmado|aprobado|definido)"),
        ("Tono confirmado", r"(?:tono|estilo|ambiente).*(?:confirmado|aprobado|definido)"),
    ]
    
    all_passed = True
    for name, pattern in checks:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"✓ {name}")
        else:
            print(f"❌ {name} - No se encontró marca de confirmación")
            all_passed = False
    
    return all_passed

def validate_step_2(args):
    """Valida Step 2: project_init - Estructura de directorios"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    required_dirs = ['config', 'memory', 'chapters', 'deliverables']
    required_files = ['config/project_info.md']
    
    all_passed = True
    
    # Verificar directorios
    for dir_name in required_dirs:
        dir_path = project_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"✓ Directorio existe: {dir_name}/")
        else:
            print(f"❌ Directorio faltante: {dir_name}/")
            all_passed = False
    
    # Verificar archivos
    for file_path in required_files:
        full_path = project_path / file_path
        if full_path.exists() and full_path.stat().st_size > 0:
            print(f"✓ Archivo existe y no está vacío: {file_path}")
        else:
            print(f"❌ Archivo faltante o vacío: {file_path}")
            all_passed = False
    
    return all_passed

def validate_step_3(args):
    """Valida Step 3: world_building - Mundo y personajes"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    required_files = [
        ('config/worldbuilding.md', 500),
        ('config/characters.md', 500),
        ('memory/character_cards.md', 100),
        ('memory/relationship_map.md', 100),
    ]
    
    all_passed = True
    
    for file_path, min_size in required_files:
        full_path = project_path / file_path
        if not full_path.exists():
            print(f"❌ Archivo faltante: {file_path}")
            all_passed = False
            continue
        
        size = full_path.stat().st_size
        if size >= min_size:
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} contenido insuficiente ({size} < {min_size} bytes)")
            all_passed = False
    
    # Verificar estructura YAML de fichas de personajes
    character_cards = project_path / "memory" / "character_cards.md"
    if character_cards.exists():
        content = character_cards.read_text(encoding='utf-8')
        # Contar cuántas veces aparece "id:" (definición de personaje en YAML)
        role_count = len(re.findall(r'^\s*-?\s*id\s*:', content, re.MULTILINE))
        if role_count >= 3:
            print(f"✓ Fichas de personajes contienen al menos 3 personajes ({role_count})")
        else:
            print(f"❌ Número insuficiente de personajes ({role_count} < 3)")
            all_passed = False
    
    return all_passed

def validate_step_4(args):
    """Valida Step 4: volume_outline - Diseño de volúmenes"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    outline_file = project_path / "config" / "volume_outline.md"
    if not outline_file.exists():
        print(f"❌ Archivo faltante: config/volume_outline.md")
        return False
    
    content = outline_file.read_text(encoding='utf-8')
    
    # Verificar si contiene al menos 3 volúmenes (formato en español)
    volume_count = len(re.findall(r'(?:Volumen|Vol\.?)\s*\d+|##\s*(?:Volumen|Vol\.?)\s*\d+', content, re.IGNORECASE))
    if volume_count >= 3:
        print(f"✓ El esquema de volúmenes contiene planificación para al menos 3 volúmenes ({volume_count})")
    else:
        print(f"❌ Número insuficiente de volúmenes ({volume_count} < 3)")
        return False
    
    # Verificar confirmación del usuario
    status_file = project_path / "status.md"
    if status_file.exists():
        status_content = status_file.read_text(encoding='utf-8')
        if re.search(r'(?:esquema de volúmenes|volume_outline).*(?:confirmado|aprobado)', status_content, re.IGNORECASE):
            print("✓ El usuario ha confirmado el esquema de volúmenes")
            return True
    
    print("⚠ Advertencia: No se encontró registro de confirmación del usuario (se recomienda confirmar antes de continuar)")
    return True  # Advertencia pero no bloquea

def validate_step_5(args):
    """Valida Step 5: volume_chapter_outline - Esquema de capítulos del volumen actual"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    # Obtener número de volumen actual
    status_file = project_path / "status.md"
    current_volume = 1
    if status_file.exists():
        content = status_file.read_text(encoding='utf-8')
        match = re.search(r'(?:Volumen|Vol\.?)\s*(\d+)', content, re.IGNORECASE)
        if match:
            current_volume = int(match.group(1))
    
    outline_file = project_path / "config" / f"volume_{current_volume}_chapter_outline.md"
    if not outline_file.exists():
        # Intentar otros formatos de nombre
        outline_file = project_path / "config" / "volume_1_chapter_outline.md"
    
    if not outline_file.exists():
        print(f"❌ Archivo faltante: archivo de esquema de capítulos")
        return False
    
    content = outline_file.read_text(encoding='utf-8')
    
    # Verificar si contiene capítulos (formato en español)
    chapter_count = len(re.findall(r'(?:Capítulo|Cap\.?)\s*\d+', content, re.IGNORECASE))
    if chapter_count >= 1:
        print(f"✓ El esquema de capítulos contiene {chapter_count} capítulos")
    else:
        print(f"❌ No se encontraron definiciones de capítulos en el esquema")
        return False
    
    return True

def validate_step_6(args):
    """Valida Step 6: chapter_loop - Escritura de capítulo individual"""
    if not args.chapter:
        print("❌ Error: Se requiere el parámetro --chapter para validar capítulo")
        return False
    
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    # Analizar número de capítulo (ej: "1_01" = Volumen 1, Capítulo 1)
    chapter_parts = args.chapter.split('_')
    if len(chapter_parts) != 2:
        print(f"❌ Error: El formato del número de capítulo debe ser 'X_Y' (ej. 1_01)")
        return False
    
    volume, chapter_num = chapter_parts
    chapter_file = project_path / "chapters" / f"vol{volume}_chapter_{chapter_num}.md"
    
    if not chapter_file.exists():
        print(f"❌ Archivo faltante: {chapter_file.name}")
        return False
    
    content = chapter_file.read_text(encoding='utf-8')
    
    # Contar palabras en español (no caracteres como en chino)
    spanish_words = len(re.findall(r'\b\w+\b', content))
    
    # Verificación de longitud: se requieren 2500-3500 palabras para un capítulo en español
    if spanish_words < 2500:
        print(f"❌ Longitud insuficiente: {spanish_words} palabras (se requieren 2500-3500 palabras)")
        return False
    elif spanish_words > 3500:
        print(f"⚠ Longitud excesiva: {spanish_words} palabras (se recomiendan 2500-3500 palabras)")
    else:
        print(f"✓ Longitud correcta: {spanish_words} palabras")
    
    # Verificar si hay gancho inicial
    first_lines = '\n'.join(content.split('\n')[:10])
    hook_indicators = ['.', '?', '!', '"', '"', "'", '...', '—', '¿', '¡']
    has_hook = any(indicator in first_lines for indicator in hook_indicators)
    
    if has_hook:
        print("✓ El inicio tiene signos de puntuación/diálogo")
    else:
        print("⚠ Sugerencia: Añadir un gancho más atractivo al principio")
    
    # Verificar descripciones sensoriales
    sensory_words = ['ver', 'mir', 'oí', 'escuch', 'ol', 'toc', 'sensación', 'luz', 'sonido', 'olor', 'temperatura',
                     'vista', 'oído', 'olfato', 'tacto', 'gusto']
    has_sensory = any(word in content.lower() for word in sensory_words)
    
    if has_sensory:
        print("✓ Contiene descripciones sensoriales")
    else:
        print("⚠ Sugerencia: Añadir detalles sensoriales (vista, oído, tacto, olfato, gusto)")
    
    # Verificar diálogos
    dialogue_count = len(re.findall(r'["""«»].*?["""«»]', content))
    if dialogue_count >= 3:
        print(f"✓ Contiene diálogos ({dialogue_count} instancias)")
    else:
        print(f"⚠ Pocos diálogos ({dialogue_count} instancias), se recomienda aumentar las conversaciones entre personajes")
    
    return True

def validate_step_7(args):
    """Valida Step 7: final_assemble - Compilación final"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    final_md = project_path / "deliverables" / "final.md"
    
    if not final_md.exists():
        print(f"❌ Archivo faltante: deliverables/final.md")
        return False
    
    size = final_md.stat().st_size
    print(f"✓ Archivo de compilación existe ({size} bytes)")
    
    # Verificar si contiene todos los capítulos
    content = final_md.read_text(encoding='utf-8')
    chapter_count = len(re.findall(r'(?:Capítulo|Cap\.?)\s*\d+', content, re.IGNORECASE))
    print(f"✓ La compilación contiene aproximadamente {chapter_count} capítulos")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Script de validación de pasos de novel-writer')
    parser.add_argument('--step', type=int, required=True, help='Paso a validar (0-7)')
    parser.add_argument('--book-name', type=str, required=True, help='Nombre del libro')
    parser.add_argument('--chapter', type=str, help='Número de capítulo (ej. 1_01)')
    parser.add_argument('--volume', type=int, help='Número de volumen')
    
    args = parser.parse_args()
    
    validators = {
        0: validate_step_0,
        1: validate_step_1,
        2: validate_step_2,
        3: validate_step_3,
        4: validate_step_4,
        5: validate_step_5,
        6: validate_step_6,
        7: validate_step_7,
    }
    
    if args.step not in validators:
        print(f"❌ Error: Número de paso inválido {args.step}")
        sys.exit(1)
    
    print(f"\n🔍 Validando Step {args.step}: {args.book_name}\n")
    
    result = validators[args.step](args)
    
    print()
    if result:
        print("✅ Validación exitosa")
        sys.exit(0)
    else:
        print("❌ Validación fallida")
        sys.exit(1)

if __name__ == '__main__':
    main()
