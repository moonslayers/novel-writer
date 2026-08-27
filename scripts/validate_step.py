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
    chapter_count = len(re.findall(r'(?:Capítulo|Cap\.?)\s
