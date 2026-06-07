import os
import glob
import json
from jinja2 import Environment, FileSystemLoader

def scan_gallery_folder(folder_path):
    """
    Scans a folder path under photos/ for image files and returns a list 
    of dictionaries structured for the portfolio frontend.
    """
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.JPG', '*.JPEG', '*.PNG', '*.WEBP')
    items = []
    
    if os.path.exists(folder_path):
        found_files = []
        for ext in extensions:
            found_files.extend(glob.glob(os.path.join(folder_path, ext)))
            
        # Sort files alphabetically to keep order predictable
        found_files.sort()
        
        for filepath in found_files:
            # Normalize to web-standard forward slashes
            web_path = filepath.replace("\\", "/")
            
            # Auto-generate a clean caption from the filename
            filename_raw = os.path.splitext(os.path.basename(web_path))[0]
            clean_caption = filename_raw.replace("-", " ").replace("_", " ").title()
            
            items.append({
                "src": web_path,
                "description": clean_caption
            })
    else:
        # Automatically create the folder structure if it got misplaced
        os.makedirs(folder_path)
        print(f"--> Created missing directory path: '{folder_path}/'")
        
    return items

def build_portfolio():
    print("--> Starting portfolio build engine with updated photos/ structure...")
    
    # Initialize Jinja2 environment templates
    env = Environment(loader=FileSystemLoader('.'))
    try:
        template = env.get_template('templates/index.html')
    except Exception:
        template = env.get_template('index.html')

    # 1. Grab the hero cover image dynamically from photos/cover
    cover_assets = scan_gallery_folder("photos/cover")
    if cover_assets:
        cover_image_path = cover_assets[0]["src"]
        print(f"--> Linked Hero Cover: {cover_image_path}")
    else:
        # Luxury fallback canvas link if your folder is empty
        cover_image_path = "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?q=80&w=1600"
        print("--> Notice: 'photos/cover/' is empty. Using high-res fallback.")

    # 2. Automatically index all image gallery directories under photos/
    categories = ["highlights", "cities", "architecture", "nature"]
    gallery_database = {}
    
    for cat in categories:
        # Scan path is now photos/category_name
        target_folder = f"photos/{cat}"
        gallery_database[cat] = scan_gallery_folder(target_folder)
        print(f"--> Indexed category '{cat}': found {len(gallery_database[cat])} images.")

    # 3. Write out the dynamic data map to gallery-data.json
    with open('gallery-data.json', 'w', encoding='utf-8') as json_file:
        json.dump(gallery_database, json_file, indent=2)
    print("--> Rebuilt and synced 'gallery-data.json' successfully.")

    # 4. Inject variables and assemble your flat index.html
    output_html = template.render(cover_image=cover_image_path)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(output_html)
    
    print("--> Complete build pipeline finalized safely!")

if __name__ == "__main__":
    build_portfolio()
