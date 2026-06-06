{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import json\
\
# Define directory mappings\
folders = \{\
    'architecture': 'photos/architecture',\
    'nature': 'photos/nature',\
    'cities': 'photos/cities',\
    'featured': 'photos/featured'\
\}\
\
manifest = \{\
    'hero': [],\
    'highlights': [],\
    'cities': [],\
    'architecture': [],\
    'nature': []\
\}\
\
valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.jpg', '.png')\
\
for category, path in folders.items():\
    if os.path.exists(path):\
        # Sort files so they display in order\
        files = sorted(os.listdir(path))\
        for f in files:\
            # Check for valid image types while ignoring system files like .DS_Store\
            if f.lower().endswith(valid_extensions) and not f.startswith('.'):\
                full_path = f"\{path\}/\{f\}"\
                \
                if category == 'featured':\
                    # Split images evenly between hero collage and slider highlights\
                    if 'hero' in f.lower():\
                        manifest['hero'].append(\{'file': full_path\})\
                    else:\
                        # Capitalize filename clean for image title text fallback\
                        title_clean = os.path.splitext(f)[0].replace('_', ' ').replace('-', ' ').title()\
                        manifest['highlights'].append(\{'file': full_path, 'title': title_clean\})\
                else:\
                    label_clean = os.path.splitext(f)[0].replace('_', ' ').replace('-', ' ').title()\
                    manifest[category].append(\{'file': full_path, 'label': label_clean\})\
\
# Save the structured file mapping right in your repository root\
with open('gallery-data.json', 'w') as out_file:\
    json.dump(manifest, out_file, indent=2)\
\
print("\uc0\u9989  Success! gallery-data.json has been completely rebuilt based on your folder contents.")}