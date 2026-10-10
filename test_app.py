from unittest.mock import patch

import app as serveur

client_test = serveur.app.test_client()

def test_page_accueil():
    response = client_test.get("/")
    assert response.status_code == 200
    assert b"Toulon" in response.data

def test_temperatures_succes():
    releves = {"2024-01-01": 10.0, "2024-01-02": 12.5}
    with patch("app.localiser", return_value=(43.12, 5.93)) as mock_localiser, \
         patch("app.charger_releves", return_value=releves) as mock_chargement:
        response = client_test.get("/temperatures?ville=Toulon")
    mock_localiser.assert_called_once_with("Toulon")
    mock_chargement.assert_called_once_with("Toulon", coordonnees=(43.12, 5.93))
    assert response.status_code == 200
    assert response.get_json() == {
        "ville": "Toulon",
        "latitude": 43.12,
        "longitude": 5.93,
        "releves": releves
    }

def test_temperatures_ville_defaut():
    with patch("app.localiser", return_value=(43.12, 5.93)), \
         patch("app.charger_releves", return_value={}) as mock_chargement:
        response = client_test.get("/temperatures")
    mock_chargement.assert_called_once_with("Toulon", coordonnees=(43.12, 5.93))
    assert response.status_code == 200

def test_ville_introuvable():
    # Quand la ville est introuvable, localiser lève ValueError
    # et charger_releves ne doit jamais être appelé
    with patch("app.localiser", side_effect=ValueError("Ville introuvable : Yxzkjh")), \
         patch("app.charger_releves") as mock_chargement:
        response = client_test.get("/temperatures?ville=Yzzkjh")
    assert response.status_code == 404
    assert "Yzzkjh" in response.get_json()["erreur"]
    mock_chargement.assert_not_called()

def test_erreur_reseau():
    # Erreur réseau lors du chargement des relevés (géocodage réussi)
    with patch("app.localiser", return_value=(43.12, 5.93)), \
         patch("app.charger_releves", side_effect=RuntimeError("Échec de connexion")):
        response = client_test.get("/temperatures")
    assert response.status_code == 502
    assert "erreur" in response.get_json()
