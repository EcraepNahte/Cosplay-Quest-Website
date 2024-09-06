
from collections import defaultdict


def organize_characters(characters):
    # Sort characters by pack, genre, and source_media
    sorted_characters = sorted(characters, key=lambda x: (x.pack_id, x.genre, x.source_media))
    
    # Group characters hierarchically
    organized = defaultdict(lambda: defaultdict(list))
    
    for char in sorted_characters:
        organized[char.pack_id][char.genre].append(char.to_dict())
    
    return organized