#!/usr/bin/env python3
"""
Valida que el esquema del capítulo cumpla con el formato requerido.
Uso: python3 validate_chapter_outline.py <NombreDelLibro> <NumeroDeCapitulo>
Ejemplo: python3 validate_chapter_outline.py "El_Caballero_Audaz" 1_09
"""

import sys
import re
from pathlib import Path

def get_project_path(book_name):
    """Obtiene la ruta del proyecto"""
    paths = [
        Path.home() / ".openclaw" / "workspace" / "content-projects" / book_name,
        Path.home() / "Documents" / book_name,
        Path.cwd() / book_name,  # Añadido: también busca en el directorio actual
    ]
    for path in path:
        if path.exists():
            return path
    return None

def validate_outline(outline_content):
    """Valida el contenido del esquema del capítulo"""
    errors = []
    warnings = []
    
    # Verificar campos requeridos (adaptados al español)
    required_fields = {
        'Momento': r'(?:Momento|Tiempo|Cuándo)[：:]',
        'Importancia': r'(?:Importancia|Peso|Relevancia)[：:]',
        'Fuente del Conflicto': r'(?:Fuente del Conflicto|Origen del Conflicto|Causa del Conflicto)[：:]',
        'Conflicto Central': r'(?:Conflicto Central|Conflicto Principal|Conflicto Clave)[：:]',
        'Decisión del Protagonista': r'(?:Decisión del Protagonista|Elección del Protagonista|Decisión Principal)[：:]',
        'Presagio/Semilla': r'(?:Presagio|Semilla|Planta|Siembra|Foreshadowing)[：:]',
        'Siguiente Capítulo': r'(?:Siguiente Capítulo|Continúa en|Conecta con)[：:]',
    }
    
    for field_name, pattern in required_fields.items():
        if not re.search(pattern, outline_content, re.IGNORECASE):
            errors.append(f"Falta el campo requerido: {field_name}")
    
    # Verificar longitud del esquema
    if len(outline_content) < 300:
        errors.append(f"El esquema es muy corto ({len(outline_content)} caracteres < 300)")
    elif len(outline_content) < 500:
        warnings.append(f"El esquema es algo corto ({len(outline_content)} caracteres < 500)")
    
    # Verificar si hay diseño de escena
    if not re.search(r'(?:Escena|Lugar|Ubicación|Ambiente|Escenario)', outline_content, re.IGNORECASE):
        warnings.append("Se recomienda añadir diseño de escena (lugar, ambiente)")
    
    # Verificar marcadores de importancia
    weight_pattern = r'[⭐★]|[1-5] estrellas?|[1-5]/5|alta|media|baja'
    if not re.search(weight_pattern, outline_content, re.IGNORECASE):
        warnings.append("Se recomienda añadir marcador de importancia (⭐-⭐⭐⭐⭐⭐ o alta/media/baja)")
    
    # Verificar si hay descripción de personajes involucrados
    if not re.search(r'(?:Personajes|Protagonista|Secundarios|Involucrados)', outline_content, re.IGNORECASE):
        warnings.append("Se recomienda listar personajes involucrados en la escena")
    
    # Verificar si hay descripción emocional o de tono
    if not re.search(r'(?:Tono|Emoción|Ambiente|Sentimiento|Clima emocional)', outline_content, re.IGNORECASE):
        warnings.append("Se recomienda describir el tono o clima emocional de la escena")
    
    return errors, warnings

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 validate_chapter_outline.py <NombreDelLibro> <NumeroDeCapitulo>")
        print("Ejemplo: python3 validate_chapter_outline.py El_Caballero_Audaz 1_09")
        sys.exit(1)
    
    book_name = sys.argv[1]
    chapter = sys.argv[2]
    
    project_path = get_project_path(book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el proyecto '{book_name}'")
        print(f"   Asegúrate de que exista en ~/Documents/{book_name} o en el directorio actual.")
        sys.exit(1)
    
    # Analizar el número de capítulo
    chapter_parts = chapter.split('_')
    if len(chapter_parts) != 2:
        print(f"❌ Error: El formato del número de capítulo debe ser 'X_Y' (ej. 1_01)")
        sys.exit(1)
    
    volume, chapter_num = chapter_parts
    outline_file = project_path / "memory" / f"chapter_{volume}_{chapter_num}_outline.md"
    
    if not outline_file.exists():
        print(f"❌ Error: El archivo del esquema no existe: {outline_file.name}")
        sys.exit(1)
    
    print(f"\n🔍 Validando esquema: '{book_name}' - Capítulo {chapter}\n")
    
    outline_content = outline_file.read_text(encoding='utf-8')
    errors, warnings = validate_outline(outline_content)
    
    if errors:
        print("❌ ERRORES (deben corregirse):")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("\n⚠️  ADVERTENCIAS (recomendaciones):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("✅ ¡Excelente! El esquema cumple con todos los requisitos")
        sys.exit(0)
    elif not errors:
        print("\n✅ El esquema es válido (tiene advertencias pero puede continuar)")
        sys.exit(0)
    else:
        print("\n❌ Validación del esquema falló. Por favor, corrige los errores y vuelve a intentarlo.")
        print("\n💡 Formato recomendado para el esquema:")
        print("   Momento: [cuándo ocurre la escena]")
        print("   Importancia: [⭐-⭐⭐⭐⭐⭐ o alta/media/baja]")
        print("   Escena: [lugar y ambiente]")
        print("   Personajes: [quién participa]")
        print("   Fuente del Conflicto: [qué causa el problema]")
        print("   Conflicto Central: [cuál es el problema principal]")
        print("   Decisión del Protagonista: [qué decide hacer]")
        print("   Tono/Emoción: [clima emocional de la escena]")
        print("   Presagio/Semilla: [qué se planta para el futuro]")
        print("   Siguiente Capítulo: [cómo conecta con lo que viene]")
        sys.exit(1)

if __name__ == '__main__':
    main()
