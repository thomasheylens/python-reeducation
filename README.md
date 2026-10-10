# python-reeducation
Projet d'apprentissage Python. Réapprentissage accompagné par un agent IA. Consomme des données météo réelles via une API publique.

## Fonctionnalités
Calcule des statistiques sur des relevés de température pour une ville donnée.
Identifie les températures les plus élevées et les plus basses avec leurs dates.
Compte le nombre de jours où la température dépasse un seuil donné.
Sert une page web (Flask) qui affiche les températures des 14 jours (7 passés, 7 à venir), avec recherche par ville.

## Installation
git clone https://github.com/thomasheylens/python-reeducation.git
cd python-reeducation
pip install -r requirements.txt

## Utilisation
Exécuter `python meteo.py` pour les statistiques en ligne de commande.
Exécuter `python app.py` puis ouvrir http://localhost:8000 — dans un Codespace, le port 8000 est accessible via l'onglet Ports.

## Limites
Les températures sont des moyennes (max+min)/2, pas des moyennes horaires.

## Tests
Les tests vérifient les calculs de moyenne, les extrêmes, le comptage des jours au-dessus d'un seuil, le géocodage, ainsi que la gestion des erreurs (données manquantes, ville introuvable, problèmes de connexion). La suite s'exécute avec `pytest`.

## Configuration du CLI Vibe
Le CLI Vibe s'installe automatiquement à la création du conteneur (voir `.devcontainer/devcontainer.json`).
Le token d'authentification se génère sur la page des extensions Vibe de Mistral Studio : https://chat.mistral.ai/code/extensions
Il ne doit jamais être commité dans le dépôt.

## Choix techniques
Les relevés sont stockés dans un dictionnaire unique pour centraliser les données.
L'API Open-Meteo fournit des données Météo-France sans nécessiter de token ; le géocodage des villes utilise son API de recherche.
Une erreur explicite est levée si les relevés sont vides pour éviter les calculs incorrects.
Flask sert la page et l'API ; le serveur écoute sur 0.0.0.0 pour que le port soit transférable depuis un Codespace.
