#!/usr/bin/env python3
"""
Verifica si el esquema del capítulo ha sido confirmado.
Uso: python3 validate_outline_confirmation.py <NombreDelLibro> <NumeroDeCapitulo>
Ejemplo: python3 validate_outline_confirmation.py "El_Caballero_Audaz" 1_08
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
    for path in paths:
        if path.exists():
            return path
    return None

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 validate_outline_confirmation.py <NombreDelLibro> <NumeroDeCapitulo>")
        print("Ejemplo: python3 validate_outline_confirmation.py El_Caballero_Audaz 1_08")
        sys.exit(1)
    
    book_name = sys.argv[1]
    chapter = sys.argv[2]
    
    project_path = get_project_path(book_name)
    if not project_path:
        print(f"❌ Error: No se encontró el proyecto '{book_name}'")
        print(f"   Asegúrate de que exista en ~/Documents/{book_name} o en el directorio actual.")
        sys.exit(1)
    
    status_file = project_path / "status.md"
    if not status_file.exists():
        print(f"❌ Error: El archivo status.md no existe")
        sys.exit(1)
    
    content = status_file.read_text(encoding='utf-8')
    
    # Analizar el número de capítulo
    chapter_parts = chapter.split('_')
    if len(chapter_parts) == 2:
        volume, chapter_num = chapter_parts
        # Intentar coincidir con múltiples formatos en español
        patterns = [
            rf"Volumen\s*{volume}.*Capítulo\s*{int(chapter_num)}.*esquema\s*(?:confirmado|aprobado|validado)",
            rf"Vol\.?\s*{volume}.*Cap\.?\s*{int(chapter_num)}.*(?:confirmado|aprobado|validado)",
            rf"vol{volume}_chapter_{chapter_num}.*confirmed",  # Mantener formato técnico
            rf"Volumen\s*{int(volume)}.*esquema\s*(?:confirmado|aprobado)",
            rf"Capítulo\s*{int(chapter_num)}.*esquema\s*(?:confirmado|aprobado)",
        ]
    else:
        patterns = [rf"Capítulo\s*{chapter}.*esquema\s*(?:confirmado|aprobado)"]
    
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"✅ Esquema confirmado: Capítulo {chapter}")
            sys.exit(0)
    
    print(f"❌ Esquema NO confirmado: Capítulo {chapter}")
    print(f"   Por favor, añade una marca de confirmación en status.md, por ejemplo:")
    print(f"   - 'Volumen 1, Capítulo 8 - Esquema confirmado, listo para escribir'")
    print(f"   - 'Vol. 1 Cap. 8 - Esquema aprobado ✓'")
    print(f"   - 'vol1_chapter_08 - confirmed'")
    sys.exit(1)

if __name__ == '__main__':
    main()
