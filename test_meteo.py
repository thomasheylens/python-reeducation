import pytest
from unittest.mock import patch
import urllib.error
from meteo import moyenne, maximale, jours_au_dessus, jour_le_plus_froid, charger_releves

def test_moyenne():
    releves = {"2024-01-01": 10.0, "2024-01-02": 20.0, "2024-01-03": 30.0}
    assert moyenne(releves) == 20.0

def test_maximum():
    releves_simple = {"2024-01-01": 10.0, "2024-01-02": 20.0, "2024-01-03": 15.0}
    max_temp, max_jour = maximale(releves_simple)
    assert max_temp == 20.0
    assert max_jour == "2024-01-02"

    releves_egalite = {"2024-01-01": 20.0, "2024-01-02": 20.0, "2024-01-03": 15.0}
    max_temp, max_jour = maximale(releves_egalite)
    assert max_temp == 20.0
    assert max_jour == "2024-01-01"

def test_jour_le_plus_froid():
    releves = {"2024-01-01": 10.0, "2024-01-02": 20.0, "2024-01-03": 5.0}
    min_temp, min_jour = jour_le_plus_froid(releves)
    assert min_temp == 5.0
    assert min_jour == "2024-01-03"

    with pytest.raises(ValueError):
        jour_le_plus_froid({})

def test_charger_releves():
    releves = charger_releves()
    assert isinstance(releves, dict)
    assert len(releves) > 0

def test_dictionnaire_vide():
    with pytest.raises(ValueError):
        moyenne({})
    with pytest.raises(ValueError):
        maximale({})
    assert jours_au_dessus({}, 10.0) == 0
    with pytest.raises(ValueError):
        jour_le_plus_froid({})

def test_moyenne_cas_varies():
    assert moyenne({"2024-01-01": 15.0}) == 15.0
    assert moyenne({"2024-01-01": -5.0, "2024-01-02": 5.0}) == 0.0

def test_maximale_une_entree():
    max_temp, max_jour = maximale({"2024-01-01": 15.0})
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

def test_charger_releves_erreur():
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError("Échec de connexion")
        with pytest.raises(SystemExit):
            charger_releves()
