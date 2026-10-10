import json
import pytest
from unittest.mock import patch
import urllib.error
from meteo import (moyenne, jour_le_plus_chaud, jours_au_dessus, jour_le_plus_froid,
                   charger_releves, localiser)

def test_moyenne():
    releves = {"2024-01-01": 10.0, "2024-01-02": 20.0, "2024-01-03": 30.0}
    assert moyenne(releves) == 20.0

def test_jour_le_plus_chaud():
    releves_simple = {"2024-01-01": 10.0, "2024-01-02": 20.0, "2024-01-03": 15.0}
    max_temp, max_jour = jour_le_plus_chaud(releves_simple)
    assert max_temp == 20.0
    assert max_jour == "2024-01-02"

    releves_egalite = {"2024-01-01": 20.0, "2024-01-02": 20.0, "2024-01-03": 15.0}
    max_temp, max_jour = jour_le_plus_chaud(releves_egalite)
    assert max_temp == 20.0
    assert max_jour == "2024-01-01"

def test_jour_le_plus_froid():
    releves = {"2024-01-01": 10.0, "2024-01-02": 20.0, "2024-01-03": 5.0}
    min_temp, min_jour = jour_le_plus_froid(releves)
    assert min_temp == 5.0
    assert min_jour == "2024-01-03"

    with pytest.raises(ValueError):
        jour_le_plus_froid({})

def test_localiser():
    """Vérifie le déballage du géocodage avec une réponse figée : aucun appel réseau."""
    fausse_reponse = {"results": [{"latitude": 43.12, "longitude": 5.93}]}
    corps = json.dumps(fausse_reponse).encode("utf-8")
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value.read.return_value = corps
        latitude, longitude = localiser("Toulon")
    assert latitude == 43.12
    assert longitude == 5.93

def test_localiser_introuvable():
    fausse_reponse = {"results": []}
    corps = json.dumps(fausse_reponse).encode("utf-8")
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value.read.return_value = corps
        with pytest.raises(ValueError):
            localiser("Xyzkjh")

def test_charger_releves():
    """Vérifie le déballage du JSON avec une réponse figée : aucun appel réseau."""
    fausse_reponse = {
        "daily": {
            "time": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04",
                     "2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08",
                     "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12",
                     "2024-01-13", "2024-01-14"],
            "temperature_2m_max": [10, 12, 14, 16, 15, 13, 11, 10, 12, 14, 15, 16, 14, 12],
            "temperature_2m_min": [2, 3, 5, 7, 6, 4, 3, 2, 4, 6, 7, 8, 6, 4],
        }
    }
    corps = json.dumps(fausse_reponse).encode("utf-8")
    with patch("meteo.localiser", return_value=(43.12, 5.93)), \
         patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value.read.return_value = corps
        releves = charger_releves("Toulon")
    assert len(releves) == 14
    assert releves["2024-01-04"] == 11.5  # (16 + 7) / 2

def test_charger_releves_erreur():
    with patch("meteo.localiser", return_value=(43.12, 5.93)), \
         patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError("Échec de connexion")
        with pytest.raises(RuntimeError):
            charger_releves()

def test_dictionnaire_vide():
    with pytest.raises(ValueError):
        moyenne({})
    with pytest.raises(ValueError):
        jour_le_plus_chaud({})
    assert jours_au_dessus({}, 10.0) == 0
    with pytest.raises(ValueError):
        jour_le_plus_froid({})

def test_moyenne_cas_varies():
    assert moyenne({"2024-01-01": 15.0}) == 15.0
    assert moyenne({"2024-01-01": -5.0, "2024-01-02": 5.0}) == 0.0

def test_jour_le_plus_chaud_une_entree():
    max_temp, max_jour = jour_le_plus_chaud({"2024-01-01": 15.0})
    assert max_temp == 15.0
    assert max_jour == "2024-01-01"

def test_jours_au_dessus():
    releves = {"2024-01-01": 10.0, "2024-01-02": 20.0, "2024-01-03": 15.0}
    assert jours_au_dessus(releves, 12.0) == 2
    assert jours_au_dessus(releves, 5.0) == 3
    assert jours_au_dessus(releves, 25.0) == 0
    assert jours_au_dessus(releves, 20.0) == 0

def test_jour_le_plus_froid_egalite():
    min_temp, min_jour = jour_le_plus_froid({"2024-01-01": 5.0, "2024-01-02": 5.0, "2024-01-03": 10.0})
    assert min_temp == 5.0
    assert min_jour == "2024-01-01"
