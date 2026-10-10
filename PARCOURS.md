# PARCOURS.md

Journal de bord du projet `python-reeducation` : réapprentissage de Python, accompagné par un agent IA (Vibe), dans le cadre d'une reconversion vers un poste d'ingénieur / chef de projet. Chaque ligne consigne un thème d'apprentissage et ce qu'il a produit.

## Journal d'apprentissage

**Prise en main de l'outillage** — Mise en place de l'environnement complet : Codespace dans le navigateur sur iPad, installation du CLI Vibe, création et synchronisation du dépôt GitHub. Premier commit, premier README. L'agent IA est opérationnel, piloté en lecture comme en écriture.

**Diagnostic d'incidents** — Plantage de l'hôte d'extensions : analyse par couches (appareil, réseau, Codespace, extension), identification de la cause probable (extension sur un environnement à ressources limitées), arbitrage local/distant. Compréhension que le CLI et l'extension sont deux surfaces du même agent, et que le CLI est le plan de repli robuste.

**Collaboration développeur-agent** — Premiers cycles de délégation encadrée : lecture de l'historique Git par l'agent, écriture déléguée du README, relecture des diffs et des messages de commit. Découverte que le comportement d'un agent se spécifie et ne se suppose pas : la qualité du livrable dépend de la précision de la consigne.

**Gouvernance d'agent** — Rédaction d'un fichier `AGENTS.md` : charte de collaboration dérivée des incidents vécus (présentation du diff avant exécution, exécution de vérification avant commit, messages de commit d'intention, périmètre strict). Vocabulaire professionnel acquis : charte, règles de contribution, Markdown. La charte est itérée à mesure du comportement observé de l'agent.

**Dictionnaires Python** — Refactoring des listes parallèles vers un dictionnaire unique de relevés : lecture du code refactoré par l'agent, puis écriture par moi-même de la fonction minimum (initialisation à `float('inf')`, mise à jour en couple des variables). Première revue de code croisée : l'agent relit ma fonction, je dois arbitrer ses critiques (docstring acceptée, renommage pesé, cas vide tranché) au lieu de les subir.

**Contrat d'erreur et cas limites** — Arbitrage du comportement sur dictionnaire vide : lancement d'une `ValueError` explicite avec message plutôt qu'une `ZeroDivisionError` accidentelle ou un `None`. Principe retenu : le test n'invente pas le comportement, il enregistre un arbitrage pris d'abord par le développeur.

**Intégration d'une API** — Branchement du programme sur des données réelles : comparaison de l'API officielle Météo-France (token, inscription) et d'Open-Meteo (diffusion des modèles AROME/ARPEGE de Météo-France, sans clé), choix de la seconde. La fonction de chargement est isolée : les fonctions de calcul traversent le changement de source sans modification — preuve expérimentale d'un bon découpage.

**Tests automatisés** — Mise en place de `pytest` : suite de tests déléguée puis relue, écriture de mes propres tests (`pytest.raises`, cas de moyenne vide), interprétation des cas limites (convention d'égalité au maximum : la première date gagne). Notion de dépendance externe et de mock : un test idéal ne dépend que du code testé, pas du monde extérieur. Extension de la suite aux cas non testés, sur ma propre initiative.

**Hygiène du dépôt** — Ajout d'un `.gitignore` sur proposition de l'agent, avant tout incident : le dépôt sait ce qu'il versionne et ce qu'il ignore. Historique de commits propres, atomiques, à l'intention lisible.

**Documentation pour un lecteur externe** — Réécriture complète du README selon un plan que j'ai conçu : présentation en trois phrases, fonctionnalités sans aucun nom de fonction (compréhensibles par un non-initié), installation avec commandes copiables, tests décrits en langage clair, choix techniques argumentés. Relecture avec trois critères : exactitude factuelle, test du non-initié, cohérence avec les tests réels.

## Lecture d'ensemble

La trajectoire se lit en quatre mouvements : outillage, méthode de collaboration, technique (dictionnaires, API, tests), puis communication (documentation). Le fil conducteur est constant : déléguer l'exécution, conserver la décision — l'arbitrage technique et la vérification finale restent les miens à chaque étape. C'est la position du chef de projet technique que je vise.
