import os
import json

def generate_portfolio_manifest():
    photos_dir = "photos"
    manifest_file = "gallery-data.json"
    
    # Target portfolio structure
    manifest = {
        "highlights": [],
        "cities": [],
        "architecture": [],
        "nature": []
    }
    
    if not os.path.exists(photos_dir):
        print(f"Error: '{photos_dir}' directory not found in the current root.")
        return

    # Map subfolders cleanly to target JSON structures
    category_mapping = {
        "highlights": "highlights",
        "cities": "cities",
        "arch": "architecture",
        "architecture": "architecture",
        "nature": "nature"
    }

    print("Analyzing asset trees dynamically...")

    # Traverse directory tree
    for root, dirs, files in os.walk(photos_dir):
        relative_path = os.path.relpath(root, photos_dir)
        if relative_path == ".":
            continue
            
        # Determine current category partition from folder name
        subfolder = relative_path.split(os.sep)[0]
        target_category = category_mapping.get(subfolder.lower())
        
        if not target_category:
            continue

        for file in sorted(files):
            # Strict verification of image asset types (ignoring system hidden files)
            if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                continue
                
            base_name = os.path.splitext(file)[0]
            # Construct web-safe absolute path strings inside standard layout wrapper
            img_path = f"{photos_dir}/{relative_path}/{file}".replace('\\', '/')
            txt_path = os.path.join(root, f"{base_name}.txt")
            
            # Default fallback description based cleanly on file naming structure
            description = base_name.replace('-', ' ').replace('_', ' ').title()
            
            # Bulletproof reading block for sidecar text files
            if os.path.exists(txt_path):
                # Try multiple common text encodings defensively to prevent decode crashes
                encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
                text_read_successfully = False
                
                for encoding in encodings_to_try:
                    try:
                        with open(txt_path, 'r', encoding=encoding) as f:
                            content = f.read().strip()
                            
                            # Defensive guard: If the file signature smells like a binary image file, reject it
                            if content.startswith(('\xff\xd8', '\x89PNG', 'GIF87a', 'GIF89a', 'RIFF')):
                                print(f"Warning: Raw binary data detected inside structural path '{txt_path}'. Bypassing file parse safely.")
                                break
                                
                            if content:
                                description = content
                            text_read_successfully = True
                            break
                    except (UnicodeDecodeError, PermissionError):
                        continue
                
                if not text_read_successfully:
                    print(f"Warning: Failed to extract descriptor safely from '{txt_path}'. Reverting to clean filename title framework.")

            # Append the structured data payload
            manifest[target_category].append({
                "src": img_path,
                "description": description
            })

    # Wrap inside an outer 'galleryData' namespace block to provide fallback mapping options inside index.html
    output_payload = {
        "galleryData": manifest
    }

    try:
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(output_payload, f, indent=2, ensure_ascii=False)
            
        print("\n=== SYSTEM INVENTORY COMPLETED ===")
        print(f"File configured: '{manifest_file}'")
        print(f" - Highlights Subspace:   {len(manifest['highlights'])} records")
        print(f" - Cities Subspace:       {len(manifest['cities'])} records")
        print(f" - Architecture Subspace: {len(manifest['architecture'])} records")
        print(f" - Nature Subspace:       {len(manifest['nature'])} records")
        print("===================================\n")
        
    except Exception as e:
        print(f"Fatal: Could not serialize configurations securely to disk: {e}")

if __name__ == "__main__":
    generate_portfolio_manifest()
