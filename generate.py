import os
import glob
import json
from jinja2 import Environment, FileSystemLoader

def scan_gallery_folder(folder_name):
    """
    Scans a folder for images and safely normalizes their web paths.
    """
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.JPG', '*.JPEG', '*.PNG', '*.WEBP')
    items = []
    
    if os.path.exists(folder_name):
        found_files = []
        for ext in extensions:
            found_files.extend(glob.glob(os.path.join(folder_name, ext)))
            
        # Sort files alphabetically to keep order predictable
        found_files.sort()
        
        for filepath in found_files:
            # 1. Standardize backslashes to forward slashes for the browser
            web_path = filepath.replace("\\", "/")
            
            # Fix: If your server requires paths starting with a leading slash, uncomment the line below:
            # if not web_path.startswith("/"): web_path = "/" + web_path
            
            # 2. Build clean text descriptions from file names
            filename_raw = os.path.splitext(os.path.basename(web_path))[0]
            clean_caption = filename_raw.replace("-", " ").replace("_", " ").title()
            
            items.append({
                "src": web_path,
                "description": clean_caption
            })
    else:
        os.makedirs(folder_name)
        print(f"--> Created empty missing directory: '{folder_name}/'")
        
    return items

def build_portfolio():
    print("--> Starting fixed portfolio build engine...")
    
    # Setup Jinja template environment
    env = Environment(loader=FileSystemLoader('.'))
    try:
        template = env.get_template('templates/index.html')
    except Exception:
        template = env.get_template('index.html')

    # 1. Grab Cover Image
    cover_assets = scan_gallery_folder("cover")
    if cover_assets:
        # Force exact resolution structure
        cover_image_path = cover_assets[0]["src"]
        print(f"--> Matched Cover Path: {cover_image_path}")
    else:
        # Luxury layout fallback path
        cover_image_path = "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?q=80&w=1600"
        print("--> Notice: 'cover/' is blank. Defaulting to Unsplash asset placeholder.")

    # 2. Index Categories
    categories = ["highlights", "cities", "architecture", "nature"]
    gallery_database = {}
    
    for cat in categories:
        gallery_database[cat] = scan_gallery_folder(cat)
        print(f"--> Category '{cat}' processed: {len(gallery_database[cat])} images synced.")

    # 3. Write out the dynamic data map file
    with open('gallery-data.json', 'w', encoding='utf-8') as json_file:
        json.dump(gallery_database, json_file, indent=2)
    print("--> Synced 'gallery-data.json' successfully.")

    # 4. Render and verify template output
    output_html = template.render(cover_image=cover_image_path)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(output_html)
    
    print("--> Build complete! Check 'index.html' locally.")

if __name__ == "__main__":
    build_portfolio()
