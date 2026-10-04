import os
import json
import urllib.parse

# Define the root photos directory and category folder mapping
BASE_DIR = "photos"

# Map category keys to their actual folder names on disk
CATEGORIES = {
    "cities_architecture": "Cities & Architecture",
    "cover": "Cover",
    "highlights": "Highlights",
    "nature_escapes": "Nature & Escapes"
}

# Allowed image extensions
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def format_description(filename: str) -> str:
    """Generates a title-case description from a filename without extension."""
    name, _ = os.path.splitext(filename)
    # Replace hyphens/underscores with spaces and convert to Title Case
    clean_name = name.replace("-", " ").replace("_", " ")
    return clean_name.title()


def build_gallery_json(base_dir: str, categories: dict) -> dict:
    gallery_data = {}

    for category_key, folder_name in categories.items():
        category_path = os.path.join(base_dir, folder_name)
        gallery_data[category_key] = []

        if not os.path.exists(category_path):
            print(f"Warning: Directory '{category_path}' not found. Skipping.")
            continue

        # Sort files to ensure deterministic output
        for filename in sorted(os.listdir(category_path)):
            ext = os.path.splitext(filename)[1].lower()
            if ext in VALID_EXTENSIONS:
                # Relative path as used on web server
                raw_path = f"{base_dir}/{folder_name}/{filename}"

                # URL-encode path while keeping forward slashes intact
                encoded_path = urllib.parse.quote(raw_path, safe="/")

                description = format_description(filename)

                gallery_data[category_key].append({
                    "src": encoded_path,
                    "description": description
                })

    return gallery_data


def main():
    data = build_gallery_json(BASE_DIR, CATEGORIES)

    output_filename = "gallery-data.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated '{output_filename}'!")


if __name__ == "__main__":
    main()