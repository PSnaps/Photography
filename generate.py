import os
import json

folders = {
    'architecture': 'photos/architecture',
    'nature': 'photos/nature',
    'cities': 'photos/cities',
    'featured': 'photos/featured'
}

manifest = {
    'hero': [],
    'highlights': [],
    'cities': [],
    'architecture': [],
    'nature': []
}

valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

for category, path in folders.items():
    if os.path.exists(path):
        files = sorted(os.listdir(path))
        for f in files:
            if f.lower().endswith(valid_extensions) and not f.startswith('.'):
                full_path = f"{path}/{f}"
                base_name = os.path.splitext(f)[0]
                
                # Check for a matching story file (e.g., IMG_1024.txt)
                story_path = os.path.join(path, f"{base_name}.txt")
                story_text = ""
                
                if os.path.exists(story_path):
                    # Smart reading logic to handle encoding conflicts smoothly
                    try:
                        with open(story_path, 'r', encoding='utf-8') as sf:
                            story_text = sf.read().strip()
                    except UnicodeDecodeError:
                        try:
                            # Fallback to UTF-16 if TextEdit saved it with byte markers (0xff)
                            with open(story_path, 'r', encoding='utf-16') as sf:
                                story_text = sf.read().strip()
                        except Exception:
                            try:
                                # Safe system fallback for standard legacy text
                                with open(story_path, 'r', encoding='latin-1') as sf:
                                    story_text = sf.read().strip()
                            except Exception as e:
                                print(f"⚠️ Could not parse story for {f}: {e}")
                                story_text = ""
                
                # Clean up title fallbacks from file name
                title_clean = base_name.replace('_', ' ').replace('-', ' ').title()
                
                if category == 'featured':
                    if 'hero' in f.lower():
                        manifest['hero'].append({'file': full_path})
                    else:
                        manifest['highlights'].append({
                            'file': full_path, 
                            'title': title_clean,
                            'story': story_text
                        })
                else:
                    manifest[category].append({
                        'file': full_path, 
                        'label': title_clean,
                        'story': story_text
                    })

with open('gallery-data.json', 'w', encoding='utf-8') as out_file:
    json.dump(manifest, out_file, indent=2, ensure_ascii=False)

print("✅ Success! gallery-data.json has been completely rebuilt.")
