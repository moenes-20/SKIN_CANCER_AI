---
title: Skin Cancer Ai
emoji: 🩺
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

<div align="center">

# 🩺 Skin Cancer AI

### Plateforme de détection intelligente des lésions cutanées par Deep Learning

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)

---

🔗 **[Accéder au Modèle (Google Drive)](https://drive.google.com/file/d/12XF6OPGURb9wIqkE9kgjsDeZzj8MDbwx/view?usp=sharing)** &nbsp;|&nbsp; 📸 **[Captures d'écran](#screenshots)** &nbsp;|&nbsp; 📊 **[Résultats d'Entraînement](#training)** &nbsp;|&nbsp; 🌐 **[Lancer le Site Web (Vercel)](https://skin-cancer-ai-beta.vercel.app/)**

</div>

---

## 📺 Démonstration Vidéo
*Lecteur interactif (Patientez quelques secondes pour le chargement) :*

<div align="center">
  <video src="https://github.com/moenes-20/SKIN_CANCER_AI/raw/main/Vedavatfinal.mp4" width="100%" controls muted autoplay loop>
    Votre navigateur ne supporte pas le lecteur vidéo. <a href="https://github.com/moenes-20/SKIN_CANCER_AI/blob/main/Vedavatfinal.mp4">Cliquez ici pour voir la vidéo</a>.
  </video>
</div>

---

## 📋 Description du Projet

**Skin Cancer AI** est une solution complète de diagnostic assisté par ordinateur. Elle intègre un modèle de Deep Learning de pointe (**VGG16**) dans une interface utilisateur moderne et fluide. Le système permet aux cliniciens d'analyser des images dermatoscopiques pour classer les lésions en deux catégories : **Bénin** ou **Malin**.

L'interface utilise des techniques avancées de rendu (**Canvas API**) pour des animations fluides et un design **Glassmorphism** premium, offrant une expérience utilisateur digne des standards de l'industrie.

---

<a name="screenshots"></a>
## 🖼️ Captures d'écran

### 1. Site de Présentation Immersion
![Presentation Hero](screenshots/00_presentation_hero.png)

### 2. Animation Scroll-Stop
![Presentation Scroll](screenshots/00_presentation_scroll.png)

### 3. Authentification Cinématique
![Login](screenshots/01_login.png)

### 4. Dashboard de Pilotage
![Dashboard](screenshots/02_dashboard.png)

### 5. Analyse Intelligente
![Analyse](03_predict_exemple.png)

### 6. Résultat de Diagnostic
![Résultat](03_predict_exemple_resultat.png)

---

<a name="training"></a>
## 🧠 Le Modèle & Résultats

### Architecture VGG16
Le modèle est basé sur l'architecture **VGG16**, optimisée par Transfer Learning.

### 📊 Performances Réelles
![Metrics](resultat/training_metrics.png)
![Confusion Matrix](resultat/confusion_matrix.png)

---

## 🏗️ Architecture du Projet

```mermaid
graph TD
    Root["📁 SKIN_CANCER_AI"]
    
    Root --> AppPy["📄 app.py"]
    Root --> DBSql["📄 database.sql"]
    Root --> Req["📄 requirements.txt"]
    Root --> Run["📄 LANCER_SKIN_CANCER_AI.bat"]
    
    Root --> Model["📁 model/"]
    Model --> VGG["📄 vgg16_skin_cancer.h5"]
    
    Root --> Pres["📁 presentation/"]
    Pres --> PIdx["📄 index.html"]
    Pres --> PFrames["📁 frames/"]
    
    Root --> Res["📁 resultat/"]
    Res --> RGraph["📊 Graphes & Metrics"]
    
    Root --> Static["📁 static/"]
    Static --> CSS["📁 css/style.css"]
    Static --> JS["📁 js/app.js"]
    Static --> Uploads["📁 uploads/"]
    
    Root --> Temp["📁 templates/"]
    Temp --> TBase["📄 base.html"]
    Temp --> TLogin["📄 login.html"]
    Temp --> TDash["📄 dashboard.html"]
    Temp --> TResult["📄 result.html"]
    
    style Root fill:#0a1628,stroke:#1378ff,stroke-width:2px,color:#fff
    style Pres fill:#1a0a28,stroke:#a78bfa,color:#fff
    style Res fill:#0a2800,stroke:#00c2ff,color:#fff
```

---

## 🛠️ Outils & Technologies
- **Backend** : Flask (Python)
- **ML/IA** : TensorFlow, Keras (VGG16)
- **Database** : MySQL
- **Deployment** : Hugging Face (Backend), Vercel (Frontend)

---

<div align="center">

**Skin Cancer AI · Diagnostic de Précision · 2026**

</div>
