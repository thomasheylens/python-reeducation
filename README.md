# python-reeducation
Projet d'apprentissage Python. Réapprentissage accompagné par un agent IA. Consomme des données météo réelles via une API publique.

## Fonctionnalités
Calcule des statistiques sur des relevés de température.
Identifie les températures les plus élevées et les plus basses avec leurs dates.
Compte le nombre de jours où la température dépasse un seuil donné.

## Installation
git clone https://github.com/<votre-compte>/python-reeducation.git
cd python-reeducation
pip install requests pytest

## Utilisation
Exécuter `python meteo.py`.

## Tests
Les tests vérifient les calculs de moyenne, les extrêmes, le comptage des jours au-dessus d'un seuil, ainsi que la gestion des erreurs (données manquantes, problèmes de connexion).

## Choix techniques
Les relevés sont stockés dans un dictionnaire unique pour centraliser les données.
L'API Open-Meteo fournit des données Météo-France sans nécessiter de token.
Une erreur explicite est levée si les relevés sont vides pour éviter les calculs incorrects.
