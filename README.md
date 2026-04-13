# SoftDesk API

API REST sécurisée développée avec Django Rest Framework dans le cadre du projet SoftDesk.

---

## 🚀 Description

Cette API permet de gérer :

- les utilisateurs
- les projets
- les contributeurs
- les issues
- les commentaires

Elle respecte des exigences de :
- sécurité (JWT, permissions)
- protection des données (RGPD)
- optimisation (green code, pagination)

---

## 📁 Structure du projet
softdesk/
├── users/
├── projects/
├── softdesk/
├── manage.py


## ⚙️ Installation

### 1. Cloner le projet

```
bash
git clone https://github.com/TON_USERNAME/softdesk-api.git
cd softdesk-api
```

### 2. Créer un environnement virtuel

```
python -m venv .venv
source .venv/bin/activate  # Linux / Mac
.venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```
pip install -r requirements.txt
```

### 4. Appliquer les migrations

```
pip install -r requirements.txt
```

### 5. Lancer le serveur

```
python manage.py runserver
```
## 📦 Technologies
Python
Django
Django REST Framework
JWT (SimpleJWT)

## 🧪 Tests

Les endpoints ont été testés avec Postman :

authentification
CRUD complet
permissions par rôle :
non authentifié
utilisateur
contributeur
auteur

## 📌 Remarques
Les mots de passe sont hashés automatiquement
Le champ password n’est jamais renvoyé dans les réponses
Les données utilisateurs respectent les contraintes RGPD



