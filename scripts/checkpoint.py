#!/usr/bin/env python3
"""
Script de puntos de control (checkpoints) de novel-writer - Crear y revertir puntos de control.
Uso:
  python3 checkpoint.py create --book-name "NombreDelLibro" --name "nombre_del_checkpoint"
  python3 checkpoint.py rollback --book-name "NombreDelLibro" --name "nombre_del_checkpoint"
  python3 checkpoint.py list --book-name "NombreDelLibro"
  python3 checkpoint.py delete --book-name "NombreDelLibro" --name "nombre_del_checkpoint"
"""

import argparse
import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

def get_project_path(book_name):
    """Obtiene la ruta del proyecto"""
    paths = [
        Path.home() / ".openclaw" / "workspace" / "content-projects" / book_name,
        Path.home() / "Documents" / book_name,
        Path.cwd() / book_name,  # Añadido: también busca en el directorio actual
    ]
    for path in paths:
        if path.exists():
            return path
    return None

def get_checkpoint_dir(project_path):
    """Obtiene el directorio de puntos de control"""
    checkpoint_dir = project_path / "memory" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    return checkpoint_dir

def create_checkpoint(args):
    """Crea un punto de control"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    checkpoint_dir = get_checkpoint_dir(project_path)
    checkpoint_name = args.name
    checkpoint_file = checkpoint_dir / f"{checkpoint_name}.checkpoint"
    
    # Recopilar estado del proyecto
    checkpoint_data = {
        "name": checkpoint_name,
        "created_at": datetime.now().isoformat(),
        "book_name": args.book_name,
        "files": {}
    }
    
    # Archivos clave a respaldar
    key_files = [
        "status.md",
        "config/project_info.md",
        "config/worldbuilding.md",
        "config/characters.md",
        "config/volume_outline.md",
    ]
    
    # Búsqueda dinámica de archivos de capítulos
    chapters_dir = project_path / "chapters"
    if chapters_dir.exists():
        for chapter_file in sorted(chapters_dir.glob("vol*_chapter_*.md")):
            relative_path = chapter_file.relative_to(project_path)
            key_files.append(str(relative_path))
    
    # Leer y almacenar contenido de archivos
    for file_path in key_files:
        full_path = project_path / file_path
        if full_path.exists():
            try:
                content = full_path.read_text(encoding='utf-8')
                checkpoint_data["files"][file_path] = content
                print(f"✓ Respaldado: {file_path}")
            except Exception as e:
                print(f"⚠ Omitido {file_path}: {e}")
    
    # Guardar punto de control
    checkpoint_file.write_text(json.dumps(checkpoint_data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"\n✅ Punto de control creado: {checkpoint_name}")
    print(f"   Ubicación: {checkpoint_file}")
    print(f"   Fecha/Hora: {checkpoint_data['created_at']}")
    print(f"   Número de archivos: {len(checkpoint_data['files'])}")
    
    return True

def rollback_checkpoint(args):
    """Revierte a un punto de control"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    checkpoint_dir = get_checkpoint_dir(project_path)
    checkpoint_name = args.name
    checkpoint_file = checkpoint_dir / f"{checkpoint_name}.checkpoint"
    
    if not checkpoint_file.exists():
        print(f"❌ Error: El punto de control '{checkpoint_name}' no existe")
        print(f"   Puntos de control disponibles:")
        list_checkpoints(args)
        return False
    
    # Leer datos del punto de control
    checkpoint_data = json.loads(checkpoint_file.read_text(encoding='utf-8'))
    
    print(f"\n⚠️  A punto de revertir al punto de control: {checkpoint_name}")
    print(f"   Fecha de creación: {checkpoint_data['created_at']}")
    print(f"   Esto sobrescribirá los siguientes archivos del proyecto actual:")
    
    for file_path in checkpoint_data["files"].keys():
        print(f"     - {file_path}")
    
    if not args.force:
        print(f"\n¿Confirmar reversión? Escribe 'yes' para continuar:")
        confirmation = input().strip().lower()
        if confirmation != 'yes':
            print("Reversión cancelada")
            return False
    
    # Ejecutar reversión
    restored_count = 0
    for file_path, content in checkpoint_data["files"].items():
        full_path = project_path / file_path
        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            print(f"✓ Restaurado: {file_path}")
            restored_count += 1
        except Exception as e:
            print(f"❌ Fallo al restaurar {file_path}: {e}")
    
    print(f"\n✅ Reversión completada, se restauraron {restored_count} archivos")
    return True

def list_checkpoints(args):
    """Lista todos los puntos de control"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    checkpoint_dir = get_checkpoint_dir(project_path)
    
    checkpoints = sorted(checkpoint_dir.glob("*.checkpoint"))
    
    if not checkpoints:
        print(f"📭 No se encontraron puntos de control")
        return True
    
    print(f"\n📋 Lista de puntos de control ({len(checkpoints)}):\n")
    print(f"{'Nombre':<40} {'Fecha de creación':<25} {'Archivos':<10}")
    print("-" * 75)
    
    for cp_file in checkpoints:
        try:
            data = json.loads(cp_file.read_text(encoding='utf-8'))
            name = data.get('name', cp_file.stem)
            created = data.get('created_at', 'unknown')[:19]
            file_count = len(data.get('files', {}))
            print(f"{name:<40} {created:<25} {file_count:<10}")
        except Exception as e:
            print(f"{cp_file.stem:<40} {'Error de lectura':<25} {'?':<10}")
    
    return True

def delete_checkpoint(args):
    """Elimina un punto de control"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el directorio del proyecto '{args.book_name}'")
        return False
    
    checkpoint_dir = get_checkpoint_dir(project_path)
    checkpoint_file = checkpoint_dir / f"{args.name}.checkpoint"
    
    if not checkpoint_file.exists():
        print(f"❌ Error: El punto de control '{args.name}' no existe")
        return False
    
    checkpoint_file.unlink()
    print(f"✅ Punto de control eliminado: {args.name}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Script de gestión de puntos de control de novel-writer')
    parser.add_argument('action', choices=['create', 'rollback', 'list', 'delete'], 
                        help='Tipo de acción')
    parser.add_argument('--book-name', type=str, required=True, help='Nombre del libro')
    parser.add_argument('--name', type=str, help='Nombre del punto de control')
    parser.add_argument('--force', action='store_true', help='Forzar reversión sin pedir confirmación')
    
    args = parser.parse_args()
    
    if args.action in ['create', 'rollback', 'delete'] and not args.name:
        parser.error(f"La acción '{args.action}' requiere el parámetro --name")
    
    actions = {
        'create': create_checkpoint,
        'rollback': rollback_checkpoint,
        'list': list_checkpoints,
        'delete': delete_checkpoint,
    }
    
    result = actions[args.action](args)
    
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
