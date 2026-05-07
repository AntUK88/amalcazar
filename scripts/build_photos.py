#!/usr/bin/env python3
import json
from pathlib import Path

PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
PHOTOS_DIR = Path('photos')
CAPTIONS_FILE = Path('captions.json')
OUTPUT_FILE = Path('photos.json')

captions = {}
if CAPTIONS_FILE.exists():
    data = json.loads(CAPTIONS_FILE.read_text(encoding='utf-8'))
    for entry in data.get('photos', []):
        captions[entry['file']] = entry

photo_files = sorted([
    f.name for f in PHOTOS_DIR.iterdir()
    if f.is_file() and f.suffix.lower() in PHOTO_EXTENSIONS
    and not f.name.startswith('.')
])

output = []
for filename in photo_files:
    entry = captions.get(filename, {})
    output.append({
        'file': filename,
        'description': entry.get('description', ''),
        'notes': entry.get('notes', '')
    })

OUTPUT_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"Built photos.json with {len(output)} photos")
