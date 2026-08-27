#!/usr/bin/env python3
"""
novel-writer: Script de revisión de personajes - Se ejecuta obligatoriamente al terminar cada capítulo.
Uso: python3 character_check.py <NombreDelLibro> <NumeroDeCapitulo>
Ejemplo: python3 character_check.py "El_Caballero_Audaz" 1_08
"""

import sys
import re
from pathlib import Path
from collections import Counter

def get_project_path(book_name):
    """Obtiene la ruta del proyecto"""
    paths = [
        Path.home() / ".openclaw" / "workspace" / "content-projects" / book_name,
        Path.home() / "Documents" / book_name,
        Path.cwd() / book_name, # Añadido: también busca en el directorio actual
    ]
    for path in paths:
        if path.exists():
            return path
    return None

def extract_characters_from_chapter(chapter_content):
    """Extrae posibles nombres de personajes del capítulo (Heurística adaptada para español)"""
    # Busca palabras que empiezan con mayúscula y tienen al menos 3 letras (incluye tildes y ñ)
    pattern = r'\b[A-Z][a-záéíóúñü]{2,}\b'
    matches = re.findall(pattern, chapter_content)
    
    # Filtro de palabras comunes en español que suelen estar capitalizadas pero NO son nombres propios
    non_names = {
        'El', 'La', 'Los', 'Las', 'Un', 'Una', 'Unos', 'Unas', 
        'Y', 'O', 'U', 'E', 'Ni', 'Que', 'Si', 'No', 'Se', 'Lo', 'Le', 
        'Del', 'Al', 'Por', 'Para', 'Con', 'Sin', 'Sobre', 'Tras', 
        'Hasta', 'Desde', 'Entre', 'Hacia', 'Este', 'Esta', 'Esto', 
        'Estos', 'Estas', 'Ese', 'Esa', 'Eso', 'Esos', 'Esas', 
        'Aquel', 'Aquella', 'Aquello', 'Aquellos', 'Aquellas', 
        'Muy', 'Mas', 'Bien', 'Mal', 'Ya', 'Aun', 'Aún', 'También', 
        'Tampoco', 'Solo', 'Sólo', 'Don', 'Doña', 'Señor', 'Señora', 
        'Capítulo', 'Volumen', 'Parte', 'Día', 'Días', 'Noche', 'Mañana',
        'Tarde', 'Hora', 'Minutos', 'Segundos', 'Casa', 'Calle', 'Ciudad',
        'Había', 'Era', 'Fue', 'Tiene', 'Tengo', 'Hace', 'Hizo', 'Puede',
        'Cuando', 'Como', 'Donde', 'Quien', 'Cual', 'Cuanto', 'Mientras',
        'Todo', 'Toda', 'Todos', 'Todas', 'Algo', 'Nada', 'Alguien', 'Nadie'
    }
    
    # Contamos frecuencias: los nombres propios suelen repetirse, las palabras al azar no tanto
    word_counts = Counter(matches)
    
    characters = set()
    for word, count in word_counts.items():
        if word not in non_names:
            characters.add(word)
    
    # Ordenamos por frecuencia (los más mencionados primero) y luego alfabéticamente
    sorted_chars = sorted(characters, key=lambda x: (-word_counts[x], x))
    return sorted_chars

def load_character_cards(project_path):
    """Carga las fichas de personajes existentes"""
    cards_file = project_path / "memory" / "character_cards.md"
    if not cards_file.exists():
        return {}
    
    content = cards_file.read_text(encoding='utf-8')
    cards = {}
    
    # Analizar fichas de personajes en formato YAML
    current_role = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- id:'):
            current_role = line.replace('- id:', '').strip()
            cards[current_role] = {}
        elif current_role and ':' in line:
            key, value = line.split(':', 1)
            cards[current_role][key.strip()] = value.strip()
    
    return cards

def check_character_importance(character, project_path, current_volume, current_chapter):
    """Verifica la importancia del personaje en capítulos posteriores"""
    outline_file = project_path / "config" / f"volume_{current_volume}_chapter_outline.md"
    if not outline_file.exists():
        outline_file = project_path / "config" / "volume_1_chapter_outline.md"
    
    if not outline_file.exists():
        return False, 0
    
    content = outline_file.read_text(encoding='utf-8')
    
    # Contar cuántas veces aparece el personaje en el esquema
    count = len(re.findall(re.escape(character), content, re.IGNORECASE))
    
    # Si aparece 2 o más veces, se considera un personaje importante
    is_important = count >= 2
    
    return is_important, count

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 character_check.py <NombreDelLibro> <NumeroDeCapitulo>")
        print("Ejemplo: python3 character_check.py El_Caballero_Audaz 1_08")
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
    chapter_file = project_path / "chapters" / f"vol{volume}_chapter_{chapter_num}.md"
    
    if not chapter_file.exists():
        print(f"❌ Error: El archivo del capítulo no existe: {chapter_file.name}")
        sys.exit(1)
    
    print(f"\n🔍 Revisión de personajes: '{book_name}' - Capítulo {chapter}\n")
    
    # Leer contenido del capítulo
    chapter_content = chapter_file.read_text(encoding='utf-8')
    
    # Extraer personajes
    characters = extract_characters_from_chapter(chapter_content)
    print(f"📖 Posibles personajes que aparecen en este capítulo ({len(characters)} detectados):")
    for char in characters[:20]:  # Mostrar solo los primeros 20 (los más frecuentes)
        print(f"  - {char}")
    if len(characters) > 20:
        print(f"  ... y {len(characters) - 20} más.")
    
    # Cargar fichas de personajes existentes
    existing_cards = load_character_cards(project_path)
    print(f"\n🎭 Fichas de personajes existentes en memoria ({len(existing_cards)}):")
    
    # Verificar qué personajes no tienen ficha
    new_characters = []
    for char in characters:
        char_id = char.lower().replace(' ', '_')
        # Ignorar títulos genéricos si no van acompañados de nombre
        if char_id not in existing_cards and char not in ['Señor', 'Señora', 'Don', 'Doña', 'Capitán', 'Rey', 'Reina']:
            new_characters.append(char)
    
    if new_characters:
        print(f"\n⚠️  Nuevos personajes detectados sin ficha ({len(new_characters)}):")
        for char in new_characters[:15]: # Limitar salida para no saturar
            # Verificar importancia en el esquema
            is_important, count = check_character_importance(char, project_path, volume, chapter_num)
            if is_important:
                print(f"  🔴 {char} (Personaje importante, aparece {count} veces en el esquema)")
            else:
                print(f"  🟡 {char} (Personaje secundario o de relleno, crear ficha es opcional)")
        if len(new_characters) > 15:
            print(f"  ... y {len(new_characters) - 15} más.")
    else:
        print("\n✅ ¡Excelente! Todos los personajes detectados ya tienen su ficha.")
    
    # Actualizar mapa de relaciones (si hay nuevos personajes)
    relationship_file = project_path / "memory" / "relationship_map.md"
    if relationship_file.exists():
        print(f"\n✓ Mapa de relaciones encontrado: {relationship_file.name}")
    else:
        print(f"\n⚠️  El mapa de relaciones no existe. Se recomienda crearlo.")
    
    print("\n📋 Acciones recomendadas para el Agente:")
    if new_characters:
        print("1. Crear fichas de personaje (YAML) para los marcados con 🔴 en `memory/character_cards.md`.")
        print("2. Actualizar el mapa de relaciones en `memory/relationship_map.md`.")
    else:
        print("No se requieren actualizaciones de personajes en este paso.")
    
    print("\n✅ Revisión de personajes completada.\n")

if __name__ == '__main__':
    main()
