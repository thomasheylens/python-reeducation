from flask import Flask, jsonify, render_template, request

from meteo import charger_releves, localiser

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/temperatures")
def temperatures():
    ville = request.args.get("ville", "Toulon")
    try:
        # Géocodage de la ville pour obtenir ses coordonnées
        latitude, longitude = localiser(ville)
        # Chargement des relevés de température
        releves = charger_releves(ville)
    except ValueError:
        return jsonify({"erreur": f"Ville introuvable : {ville}"}), 404
    except RuntimeError as e:
        return jsonify({"erreur": f"Problème de connexion à l'API : {e}"}), 502
    return jsonify({
        "ville": ville,
        "latitude": latitude,
        "longitude": longitude,
        "releves": releves
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
