from __future__ import annotations

import json
import os
import time

from flask import Flask, Response, jsonify, render_template, request

from meteo import (
    charger_releves,
    charger_releves_villes,
    jour_le_plus_chaud,
    jour_le_plus_froid,
    jours_au_dessus,
    localiser,
    moyenne,
)

app = Flask(__name__)

def charger_villes() -> list[dict]:
    """Lit le fichier villes.json : les villes de plus de 50 000 habitants.
    Returns:
        list: Dictionnaires {"nom": str, "latitude": float, "longitude": float}.
    """
    chemin = os.path.join(os.path.dirname(__file__), "villes.json")
    with open(chemin, encoding="utf-8") as fichier:
        return json.load(fichier)

VILLES = charger_villes()

# Cache en mémoire des relevés de toutes les villes : {"date", "donnees"}
_cache_villes: dict | None = None
DUREE_CACHE_VILLES = 1800  # 30 minutes, en secondes

@app.route("/")
def index() -> str:
    return render_template("index.html")

@app.route("/temperatures")
def temperatures() -> Response | tuple[Response, int]:
    ville = request.args.get("ville", "Toulon")
    try:
        # Géocodage de la ville pour obtenir ses coordonnées
        latitude, longitude = localiser(ville)
        # Chargement des relevés de température
        releves = charger_releves(ville, coordonnees=(latitude, longitude))
    except ValueError:
        return jsonify({"erreur": f"Ville introuvable : {ville}"}), 404
    except RuntimeError as e:
        return jsonify({"erreur": f"Problème de connexion à l'API : {e}"}), 502
    # Mesures calculées avec les fonctions de meteo.py (affichées dans la colonne de droite)
    temp_moyenne = moyenne(releves)
    temp_max, jour_max = jour_le_plus_chaud(releves)
    temp_min, jour_min = jour_le_plus_froid(releves)
    return jsonify({
        "ville": ville,
        "latitude": latitude,
        "longitude": longitude,
        "releves": releves,
        "mesures": {
            "moyenne": temp_moyenne,
            "max": {"temperature": temp_max, "jour": jour_max},
            "min": {"temperature": temp_min, "jour": jour_min},
            "jours_au_dessus_moyenne": jours_au_dessus(releves, temp_moyenne)
        }
    })

@app.route("/temperatures-villes")
def temperatures_villes() -> Response:
    """Renvoie les relevés des 14 jours pour chaque ville du fichier villes.json.
    Les relevés sont gardés 30 minutes en mémoire pour ne pas solliciter
    l'API météo à chaque chargement de la page.
    """
    global _cache_villes
    if _cache_villes is not None and time.time() - _cache_villes["date"] < DUREE_CACHE_VILLES:
        return jsonify(_cache_villes["donnees"])
    releves = charger_releves_villes(VILLES)
    _cache_villes = {"date": time.time(), "donnees": releves}
    return jsonify(releves)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
