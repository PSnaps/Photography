import os
import json

# Define directory mappings
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

valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.jpg', '.png')

for category, path in folders.items():
    if os.path.exists(path):
        # Sort files so they display in order
        files = sorted(os.listdir(path))
        for f in files:
            # Check for valid image types while ignoring system files like .DS_Store
            if f.lower().endswith(valid_extensions) and not f.startswith('.'):
                full_path = f"{path}/{f}"
                
                if category == 'featured':
                    # Split images evenly between hero collage and slider highlights
                    if 'hero' in f.lower():
                        manifest['hero'].append({'file': full_path})
                    else:
                        # Capitalize filename clean for image title text fallback
                        title_clean = os.path.splitext(f)[0].replace('_', ' ').replace('-', ' ').title()
                        manifest['highlights'].append({'file': full_path, 'title': title_clean})
                else:
                    label_clean = os.path.splitext(f)[0].replace('_', ' ').replace('-', ' ').title()
                    manifest[category].append({'file': full_path, 'label': label_clean})

# Save the structured file mapping right in your repository root
with open('gallery-data.json', 'w') as out_file:
    json.dump(manifest, out_file, indent=2)

print("✅ Success! gallery-data.json has been completely rebuilt based on your folder contents.")