# Utiliser Python 3.10
FROM python:3.10-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Créer le dossier de l'app
WORKDIR /app

# Copier les requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du projet
COPY . .

# Créer le dossier uploads s'il n'existe pas
RUN mkdir -p static/uploads && chmod 777 static/uploads

# Exposer le port par défaut de Hugging Face
EXPOSE 7860

# Lancer l'application avec Gunicorn (Mode Performance : 4 workers)
CMD ["gunicorn", "--workers", "4", "--threads", "2", "--timeout", "120", "--bind", "0.0.0.0:7860", "app:app"]
