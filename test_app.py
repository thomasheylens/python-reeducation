from unittest.mock import patch

import app as serveur

client_test = serveur.app.test_client()

def test_page_accueil():
    response = client_test.get("/")
    assert response.status_code == 200
    assert b"Toulon" in response.data

def test_page_accueil_mode_nuit():
    # Le bouton de bascule et le fond de carte nocturne sont présents dans la page
    response = client_test.get("/")
    assert response.status_code == 200
    assert b'id="mode-nuit"' in response.data
    assert b"Mode nuit" in response.data
    assert b"World_Dark_Gray_Base" in response.data

def test_page_curseur_date_et_texte_carte():
    # Le curseur remplace l'ancienne liste déroulante et l'info-bulle disparaît
    response = client_test.get("/")
    assert response.status_code == 200
    assert b'id="curseur-date"' in response.data
    assert b'type="range"' in response.data
    assert b'<select id="date">' not in response.data
    assert b"temperature-carte" in response.data
    assert b"bindPopup" not in response.data

def test_page_colonne_mesures():
    # La colonne des mesures est présente dans la page, masquée par défaut
    response = client_test.get("/")
    assert response.status_code == 200
    assert b'id="mesures"' in response.data
    assert b'id="mesure-moyenne"' in response.data
    assert b'id="mesure-max"' in response.data
    assert b'id="mesure-min"' in response.data
    assert b'id="mesure-jours"' in response.data
    assert b"#mesures.visible" in response.data

def test_temperatures_villes():
    # La route renvoie les relevés de chaque ville du fichier villes.json
    villes = [{"nom": "Toulon", "latitude": 43.12, "longitude": 5.93}]
    donnees = [{"nom": "Toulon", "latitude": 43.12, "longitude": 5.93,
                "releves": {"2024-01-01": 10.0}}]
    with patch("app.VILLES", villes), \
         patch("app.charger_releves_villes", return_value=donnees) as mock:
        serveur._cache_villes = None  # Vide le cache entre les tests
        response = client_test.get("/temperatures-villes")
    assert response.status_code == 200
    assert response.get_json() == donnees
    mock.assert_called_once_with(villes)

def test_temperatures_villes_cache():
    # Un deuxième appel dans les 30 minutes ne recharge pas les données
    villes = [{"nom": "Toulon", "latitude": 43.12, "longitude": 5.93}]
    donnees = [{"nom": "Toulon", "latitude": 43.12, "longitude": 5.93,
                "releves": {"2024-01-01": 10.0}}]
    with patch("app.VILLES", villes), \
         patch("app.charger_releves_villes", return_value=donnees) as mock:
        serveur._cache_villes = None
        client_test.get("/temperatures-villes")
        response = client_test.get("/temperatures-villes")
    mock.assert_called_once()
    assert response.get_json() == donnees

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
        "releves": releves,
        "mesures": {
            "moyenne": 11.25,
            "max": {"temperature": 12.5, "jour": "2024-01-02"},
            "min": {"temperature": 10.0, "jour": "2024-01-01"},
            "jours_au_dessus_moyenne": 1
        }
    }

def test_temperatures_ville_defaut():
    releves = {"2024-01-01": 10.0, "2024-01-02": 12.5}
    with patch("app.localiser", return_value=(43.12, 5.93)), \
         patch("app.charger_releves", return_value=releves) as mock_chargement:
        response = client_test.get("/temperatures")
    mock_chargement.assert_called_once_with("Toulon", coordonnees=(43.12, 5.93))
    assert response.status_code == 200
    assert response.get_json() == {
        "ville": "Toulon",
        "latitude": 43.12,
        "longitude": 5.93,
        "releves": releves,
        "mesures": {
            "moyenne": 11.25,
            "max": {"temperature": 12.5, "jour": "2024-01-02"},
            "min": {"temperature": 10.0, "jour": "2024-01-01"},
            "jours_au_dessus_moyenne": 1
        }
    }

def test_ville_introuvable():
    # Quand la ville est introuvable, localiser lève ValueError
    # et charger_releves ne doit jamais être appelé
    with patch("app.localiser", side_effect=ValueError("Ville introuvable : Yxzkjh")), \
         patch("app.charger_releves") as mock_chargement:
        response = client_test.get("/temperatures?ville=Yzzkjh")
    assert response.status_code == 404
    assert "Yzzkjh" in response.get_json()["erreur"]
    mock_chargement.assert_not_called()

def test_ville_vide():
    # Une chaîne vide n'est pas la valeur par défaut : la ville est introuvable
    with patch("app.localiser", side_effect=ValueError("Ville introuvable : ")), \
         patch("app.charger_releves") as mock_chargement:
        response = client_test.get("/temperatures?ville=")
    assert response.status_code == 404
    assert response.get_json()["erreur"] == "Ville introuvable : "
    mock_chargement.assert_not_called()

def test_erreur_reseau():
    # Erreur réseau lors du chargement des relevés (géocodage réussi)
    with patch("app.localiser", return_value=(43.12, 5.93)), \
         patch("app.charger_releves", side_effect=RuntimeError("Échec de connexion")):
        response = client_test.get("/temperatures")
    assert response.status_code == 502
    assert "erreur" in response.get_json()
