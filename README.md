# python-reeducation

Application météo complète en Python : une carte de France affiche en permanence les températures d'environ 90 villes sur un curseur de 14 jours, adossée à deux routes JSON et à des statistiques calculées côté serveur. Le projet a été réalisé en un mois dans le cadre d'un réapprentissage de Python : il rassemble une application Flask, une suite de 25 tests pytest et un linter Ruff. Il documente surtout une méthode de travail : le développement a été délégué à un agent IA de code, gouverné par une charte écrite et des revues avant fusion.

## Méthode

Le développement a été délégué à un agent IA de code (le CLI Vibe), gouverné par une charte écrite : [AGENTS.md](AGENTS.md). Cette charte fixe le mode de collaboration : trois questions de cadrage avant tout chantier, trois phrases d'explication ensuite, une branche par modification poussée sur le distant, suite de tests verte et linter sans écart avant chaque commit, commits atomiques dont le message tient en une phrase de dix mots maximum. La fusion vers la branche principale reste un geste manuel du porteur du projet (avec `--no-ff`). La première pull request du dépôt, la [pull request #1](https://github.com/thomasheylens/python-reeducation/pull/1), illustre ce mode de bout en bout : branche poussée, revue formelle déposée sur le diff, fusion depuis l'interface. Le journal d'apprentissage du projet, thème par thème, est consigné dans [PARCOURS.md](PARCOURS.md).

## Fonctionnalités

- Statistiques en ligne de commande (`python meteo.py`) : moyenne des relevés, températures la plus élevée et la plus basse avec leurs dates, nombre de jours au-dessus d'un seuil donné.
- Page web (Flask) : carte plein écran de France affichant en permanence les températures d'environ 90 villes, sur un curseur de 14 jours.
  <!-- capture : carte de France — image à venir : docs/captures/carte-france.png -->
- Route `/temperatures?ville=` : coordonnées de la ville et températures sous deux clés, `observations` (7 jours passés) et `previsions` (7 jours à venir), plus un bloc `mesures` (moyenne, extrêmes, jours au-dessus de la moyenne).
- Route `/temperatures-villes` : la même structure pour toutes les villes du fichier `villes.json`.
- La recherche d'une ville la met en évidence et ouvre un panneau de mesures (moyenne, extrêmes, jours au-dessus de la moyenne).
  <!-- capture : panneau de mesures — image à venir : docs/captures/panneau-mesures.png -->
- Échelle de couleurs du bleu au rouge (-10 à 40 °C), avec mode nuit.

## Installation

```
git clone https://github.com/thomasheylens/python-reeducation.git
cd python-reeducation
pip install -r requirements.txt
```

L'environnement de développement est déclaré dans le dépôt (`.devcontainer/devcontainer.json`) : un Codespace se reconstruit automatiquement, avec un `git pull --ff-only` au démarrage.

## Utilisation

- `python meteo.py` : statistiques en ligne de commande.
- `python app.py`, puis ouvrir http://localhost:8000 — dans un Codespace, le port 8000 est accessible via l'onglet Ports.

## Tests

La suite compte 25 tests et s'exécute avec `pytest`. Elle vérifie les calculs de moyenne, les extrêmes, le comptage des jours au-dessus d'un seuil, le géocodage, les routes du serveur (une ville avec mesures, toutes les villes, chargement parallèle et cache), la page (mode nuit, curseur de date, panneau de mesures) ainsi que la gestion des erreurs (données manquantes, ville introuvable, problèmes de connexion).

## Outils de développement

Le linter Ruff vérifie les conventions PEP 8, le tri des imports et les pièges classiques (règles E, W, F, I, B, UP) :

```
pip install -r requirements-dev.txt
python -m ruff check .
```

La correction automatique est disponible : `python -m ruff check . --fix`. Les dépendances de développement (Ruff, pytest) sont déclarées à part, dans `requirements-dev.txt`.

## Choix techniques

- Les températures sont séparées en deux dictionnaires distincts — `observations` pour les 7 jours passés, `previsions` pour les 7 jours à venir — pour que le vocabulaire de l'API suive la sémantique des données.
- L'API Open-Meteo fournit les données de Météo-France sans nécessiter de token ; le géocodage des villes utilise son API de recherche.
- Une erreur explicite est levée si les relevés sont vides, pour éviter les calculs incorrects.
- Flask sert la page et l'API ; le serveur écoute sur 0.0.0.0 pour que le port soit transférable depuis un Codespace.
- La liste des villes (90 villes de plus de 50 000 habitants) est fixée dans `villes.json` ; leur chargement est parallélisé sur 3 fils avec un timeout réseau de 15 secondes, et mis en cache 30 minutes côté serveur pour ménager l'API.
- Limites assumées : les températures sont des moyennes simplifiées (max+min)/2, pas des moyennes horaires ; le cache serveur de 30 minutes peut donc servir des relevés légèrement datés.
- Python 3.14 ; la charte du dépôt n'autorise aucune bibliothèque externe sans accord explicite — la seule dépendance de production est Flask.
- Les messages de commit sont limités à une phrase de dix mots.

<details>
<summary>Configuration du CLI Vibe (pour l'auteur du dépôt)</summary>

Le CLI Vibe s'installe automatiquement à la création du conteneur (voir `.devcontainer/devcontainer.json`).
Le token d'authentification se génère sur la page des extensions Vibe de Mistral Studio : https://chat.mistral.ai/code/extensions
Il ne doit jamais être commité dans le dépôt.

</details>
