#!/usr/bin/env python3
"""
Script de control de flujo de trabajo de novel-writer - Asegura que cada etapa tenga validación.
Uso: python3 workflow.py <comando> [argumentos]
"""

import argparse
import sys
import subprocess
from pathlib import Path

def run_validation(script_name, *args):
    """Ejecuta un script de validación"""
    script_dir = Path(__file__).parent
    script_path = script_dir / script_name
    
    if not script_path.exists():
        print(f"❌ Error: El script de validación no existe {script_name}")
        return False
    
    cmd = ['python3', str(script_path)] + list(args)
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def cmd_create_outline(args):
    """Flujo de validación después de crear el esquema del capítulo"""
    print("\n📋 Paso 6.1: Crear esquema del capítulo\n")
    
    # Validar formato del esquema
    if not run_validation('validate_chapter_outline.py', args.book_name, args.chapter):
        print("\n❌ Validación del formato del esquema falló")
        return False
    
    print("\n✅ Esquema del capítulo creado exitosamente")
    print(f"\nSiguiente paso:")
    print(f"1. Por favor, revisa el esquema: memory/chapter_{args.chapter}_outline.md")
    print(f"2. Después de confirmar, actualiza status.md con 'Volumen X, Capítulo Y - Esquema confirmado'")
    print(f"3. Ejecuta: python3 workflow.py confirm-outline {args.book_name} {args.chapter}")
    return True

def cmd_confirm_outline(args):
    """Flujo de validación después de confirmar el esquema"""
    print("\n✅ Paso 6.1 completado: Esquema confirmado\n")
    
    # Validar estado de confirmación del esquema
    if not run_validation('validate_outline_confirmation.py', args.book_name, args.chapter):
        print("\n❌ El esquema no está confirmado, no se puede entrar a la fase de escritura")
        return False
    
    print("\n✅ Validación de confirmación del esquema exitosa")
    print(f"\nSiguiente paso:")
    print(f"Ejecuta: python3 workflow.py write {args.book_name} {args.chapter}")
    return True

def cmd_write(args):
    """Flujo de validación antes de escribir"""
    print("\n✍️  Paso 6.2: Escritura del capítulo\n")
    
    # Debe validar que el esquema esté confirmado
    if not run_validation('validate_outline_confirmation.py', args.book_name, args.chapter):
        print("\n❌ Bloqueado: El esquema no está confirmado, no se puede empezar a escribir")
        print("Por favor, completa primero:")
        print(f"1. Crear esquema: python3 workflow.py create-outline {args.book_name} {args.chapter}")
        print(f"2. Después de confirmación del usuario: python3 workflow.py confirm-outline {args.book_name} {args.chapter}")
        return False
    
    print("\n✅ Validación previa a escritura exitosa, se puede comenzar a escribir")
    return True

def cmd_after_write(args):
    """Flujo de validación después de completar la escritura"""
    print("\n📝 Paso 6.2 completado: Escritura del capítulo\n")
    
    # Validar capítulo
    if not run_validation('validate_step.py', '--step', '6', '--book-name', args.book_name, '--chapter', args.chapter):
        print("\n⚠️  La validación del capítulo tiene advertencias, se recomienda revisar")
    
    print("\nSiguiente paso:")
    print(f"Ejecuta: python3 workflow.py character-check {args.book_name} {args.chapter}")
    return True

def cmd_character_check(args):
    """Flujo de verificación de personajes"""
    print("\n🎭 Paso 6.3: Verificación de personajes\n")
    
    if not run_validation('character_check.py', args.book_name, args.chapter):
        print("\n⚠️  La verificación de personajes no se completó")
        return False
    
    print("\n✅ Verificación de personajes completada")
    print("\nSiguiente paso:")
    print("Esperar revisión del capítulo por parte del usuario")
    print("Si está satisfecho → Pasar al siguiente capítulo")
    print("Si necesita modificaciones → Reescribir")
    return True

def main():
    parser = argparse.ArgumentParser(description='Control de flujo de trabajo de novel-writer')
    parser.add_argument('command', choices=[
        'create-outline', 'confirm-outline', 'write', 
        'after-write', 'character-check'
    ], help='Comando del flujo de trabajo')
    parser.add_argument('book_name', help='Nombre del libro')
    parser.add_argument('chapter', help='Número de capítulo (ej. 1_09)')
    
    args = parser.parse_args()
    
    commands = {
        'create-outline': cmd_create_outline,
        'confirm-outline': cmd_confirm_outline,
        'write': cmd_write,
        'after-write': cmd_after_write,
        'character-check': cmd_character_check,
    }
    
    result = commands[args.command](args)
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
