import os
from PIL import Image

def optimize_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"DEBUG: Dossier non trouve : {folder_path}")
        return

    print(f"DEBUG: Optimisation des images dans : {folder_path}")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                new_path = os.path.splitext(file_path)[0] + ".webp"
                
                try:
                    with Image.open(file_path) as img:
                        img.save(new_path, "WEBP", quality=80)
                        print(f"OK: Converti : {file} -> {os.path.basename(new_path)}")
                except Exception as e:
                    print(f"ERROR: Erreur sur {file}: {e}")

# CETTE FOIS ON VISE LE BON DOSSIER
optimize_folder("presentation/frames")
optimize_folder("static/img")

print("\nOptimisation terminee !")
