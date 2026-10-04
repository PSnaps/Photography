import os
import glob
import json
import re
from jinja2 import Environment, FileSystemLoader

def clean_category_key(folder_name):
    """
    Converts folder names into clean, lower-snake_case JSON keys for JavaScript.
    E.g., "Cities & Architecture" -> "cities_architecture"
    """
    clean = folder_name.lower()
    clean = re.sub(r'[^a-z0-9]+', '_', clean)
    return clean.strip('_')

def scan_gallery_folder(folder_path):
    """
    Scans a folder path under photos/ for image files and returns a list 
    of dictionaries structured for the portfolio frontend.
    """
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.JPG', '*.JPEG', '*.PNG', '*.WEBP')
    items = []
    
    if os.path.exists(folder_path):
        found_files = set()
        for ext in extensions:
            for filepath in glob.glob(os.path.join(folder_path, ext)):
                # Use absolute paths in set to deduplicate case-insensitive Windows matches
                found_files.add(os.path.abspath(filepath))
            
        sorted_files = sorted(list(found_files))
        
        for filepath in sorted_files:
            # Convert back to relative path using web-standard forward slashes
            rel_path = os.path.relpath(filepath, start=os.getcwd()).replace("\\", "/")
            
            # Auto-generate a clean caption from the filename
            filename_raw = os.path.splitext(os.path.basename(rel_path))[0]
            clean_caption = filename_raw.replace("-", " ").replace("_", " ").title()
            
            items.append({
                "src": rel_path,
                "description": clean_caption
            })
    else:
        os.makedirs(folder_path, exist_ok=True)
        print(f"--> Created missing directory path: '{folder_path}/'")
        
    return items

def build_portfolio():
    print("--> Starting portfolio build engine with dynamic directory scanning...")
    
    photos_dir = "photos"
    gallery_database = {}

    # 1. Dynamically discover and index all subdirectories inside photos/
    if os.path.exists(photos_dir):
        subfolders = [
            d for d in os.listdir(photos_dir) 
            if os.path.isdir(os.path.join(photos_dir, d))
        ]
        
        for folder_name in sorted(subfolders):
            target_folder = os.path.join(photos_dir, folder_name)
            # Map folder name to a clean JS key (e.g. 'cities_architecture')
            js_key = clean_category_key(folder_name)
            
            scanned_items = scan_gallery_folder(target_folder)
            gallery_database[js_key] = scanned_items
            
            print(f"--> Indexed folder '{folder_name}' as key '{js_key}': found {len(scanned_items)} images.")
    else:
        os.makedirs(photos_dir, exist_ok=True)
        print(f"--> Notice: Created missing base '{photos_dir}/' folder.")

    # 2. Select Cover Image (look in 'cover' key or fallback)
    cover_assets = gallery_database.get("cover", [])
    if cover_assets:
        cover_image_path = cover_assets[0]["src"]
        print(f"--> Linked Hero Cover: {cover_image_path}")
    else:
        cover_image_path = "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?q=80&w=1600"
        print("--> Notice: 'photos/cover/' empty or missing. Using high-res fallback.")

    # 3. Write dynamic data map to gallery-data.json
    with open('gallery-data.json', 'w', encoding='utf-8') as json_file:
        json.dump(gallery_database, json_file, indent=2)
    print("--> Rebuilt and synced 'gallery-data.json' successfully.")

    # 4. Safely render Jinja2 template without self-overwriting source
    env = Environment(loader=FileSystemLoader('.'))
    template_path = 'templates/index.html' if os.path.exists('templates/index.html') else 'index.html'
    
    try:
        template = env.get_template(template_path)
        output_html = template.render(cover_image=cover_image_path)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(output_html)
        print("--> Complete build pipeline finalized safely!")
    except Exception as e:
        print(f"--> Warning during HTML rendering: {e}")

if __name__ == "__main__":
    build_portfolio()