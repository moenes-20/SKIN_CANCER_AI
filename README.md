---
title: Skin Cancer Ai
emoji: 🩺
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# 🩺 Skin Cancer AI Platform - Clinical Intelligence

> **Une solution complète de diagnostic dermatologique assisté par IA, alliant la puissance du Deep Learning (VGG16) à une architecture Cloud moderne.**

[![Vercel Presentation](https://img.shields.io/badge/Live-Vercel_Site-blue?style=for-the-badge&logo=vercel)](https://skin-cancer-ai-beta.vercel.app/)
[![Hugging Face App](https://img.shields.io/badge/AI_Engine-Hugging_Face-orange?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/moenes123/skin-cancer-ai-v2)

---

## 📺 Démonstration Vidéo
Découvrez le parcours utilisateur complet, de la présentation à l'analyse clinique :

<div align="center">
  <video src="Vedavatfinal.mp4" width="100%" controls></video>
</div>

---

## 📸 Aperçu de la Plateforme

### 1. Site de Présentation (Vercel)
Une interface immersive avec animations "scroll-stop" pour présenter le projet.
![Vercel Presentation](screenshots/01_home_vercel.png)

### 2. Dashboard Clinique (Hugging Face)
Le centre de contrôle pour la gestion des patients et des analyses.
![Dashboard](screenshots/02_dashboard.png)

### 3. Processus d'Analyse IA
L'utilisateur dépose une image pour une prédiction instantanée.
![Analyse](03_predict_exemple.png)

### 4. Rapport de Diagnostic
Résultats détaillés générés par le modèle VGG16 fine-tuné.
![Résultat](03_predict_exemple_resultat.png)

---

## 🏗️ Architecture du Système

```mermaid
graph TD
    A[Vercel Site - Presentation] -->|Redirection| B[Hugging Face Space - App]
    B -->|Moteur Flask/Docker| C{IA Model VGG16}
    B -->|Persistance| D[Aiven Cloud - MySQL]
    C -->|Prediction| B
    B -->|Dashboard UI| E[Utilisateur Final]
```

### Stack Technique
- **Frontend Vitrine** : Vanilla JS, CSS3, Vercel
- **Application IA** : Flask, Python 3.10, Gunicorn (4 workers)
- **Modèle Deep Learning** : VGG16 (Transfer Learning)
- **Base de Données** : MySQL 8.0 sur Aiven Cloud
- **Déploiement** : Docker, Hugging Face Spaces

---

## 🧠 Le Modèle IA
Le cœur du système repose sur une architecture **VGG16** pré-entraînée sur ImageNet, puis fine-tunée sur un dataset médical de lésions cutanées.
- **Entrée** : Images 224x224 pixels.
- **Sortie** : Classification Binaire (Bénin / Malin) avec score de confiance.
- **Performance** : Optimisé pour la détection clinique assistée.

---

## 🚀 Installation & Déploiement

### Déploiement Cloud
- **Frontend** : Connecter le dossier `/presentation` à Vercel.
- **Backend** : Utiliser le script `upload_to_hf.py` pour envoyer le projet sur Hugging Face.

### Lancement Local
Exécuter le fichier `LANCER_SKIN_CANCER_AI.bat` pour démarrer le serveur Flask localement sur le port 5000.

---

© 2026 Plateforme Skin Cancer AI - Développé pour l'excellence médicale.
