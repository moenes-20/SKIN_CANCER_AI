import os
from huggingface_hub import HfApi
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# CONFIGURATION
REPO_ID = "moenes123/skin-cancer-ai-v2" 
TOKEN = os.getenv("HF_TOKEN") # Ne pas mettre le token ici pour GitHub !

api = HfApi()

print(f"DEBUG: Debut de l'upload vers {REPO_ID}...")

# Upload de tout le dossier actuel
api.upload_folder(
    folder_path=".",
    repo_id=REPO_ID,
    repo_type="space",
    token=TOKEN,
    ignore_patterns=[".venv/*", ".git/*", "*.mp4", "__pycache__/*", "upload_to_hf.py", ".env", "optimize_images.py"]
)

print("DEBUG: Termine ! Ton application est en cours de deploiement.")
