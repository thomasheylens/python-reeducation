from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request

def moyenne(releves: dict[str, float]) -> float:
    """Calcule la température moyenne à partir d'un dictionnaire de relevés.
    Args:
        releves: Dictionnaire {date ISO: température} (ex: {'2024-01-01': 20.5}).
    Returns:
        float: Température moyenne en °C.
    Raises:
        ValueError: Si le dictionnaire est vide.
    """
    if not releves:
        raise ValueError("Le dictionnaire de relevés ne peut pas être vide.")
    return sum(releves.values()) / len(releves)

def jour_le_plus_chaud(releves: dict[str, float]) -> tuple[float, str]:
    """Trouve la température maximale et le jour correspondant.
    Args:
        releves: Dictionnaire {jour: température}.
    Returns:
        tuple: (température_max, jour) où température_max est la plus haute température.
    Raises:
        ValueError: Si le dictionnaire est vide.
    """
    if not releves:
        raise ValueError("Le dictionnaire de relevés ne peut pas être vide.")
    maxi = -float('inf')
    jour_max = None
    for jour, temp in releves.items():
        if temp > maxi:
            maxi = temp
            jour_max = jour
    return maxi, jour_max

def jours_au_dessus(releves: dict[str, float], seuil: float) -> int:
    """Compte les jours où la température dépasse le seuil.
    Args:
        releves: Dictionnaire {jour: température}.
        seuil: Température seuil en °C (float).
    Returns:
        int: Nombre de jours strictement au-dessus du seuil.
    """
    resultat = 0
    for temp in releves.values():
        if temp > seuil:
            resultat += 1
    return resultat

def jour_le_plus_froid(releves: dict[str, float]) -> tuple[float, str]:
    """Trouve la température minimale et le jour correspondant.
    Args:
        releves: Dictionnaire {jour: température}.
    Returns:
        tuple: (température_min, jour) où température_min est la plus basse température.
    Raises:
        ValueError: Si le dictionnaire est vide.
    """
    if not releves:
        raise ValueError("Le dictionnaire de relevés ne peut pas être vide.")
    temp_mini = float('inf')
    jour_min = None
    for jour, temp in releves.items():
        if temp < temp_mini:
            temp_mini = temp
            jour_min = jour
    return temp_mini, jour_min

def localiser(ville: str) -> tuple[float, float]:
    """Retrouve les coordonnées d'une ville via l'API de géocodage Open-Meteo.
    Args:
        ville: Nom de la ville (str), ex: "Toulon".
    Returns:
        tuple: (latitude, longitude) du premier résultat.
    Raises:
        ValueError: Si la ville est introuvable.
        RuntimeError: Si l'appel au service de géocodage échoue.
    """
    url = (
        "https://geocoding-api.open-meteo.com/v1/search?name="
        + urllib.parse.quote(ville) + "&count=1&language=fr&format=json"
    )
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        raise RuntimeError(f"Échec du géocodage : {e}") from e
    resultats = data.get('results')
    if not resultats:
        raise ValueError(f"Ville introuvable : {ville}")
    return resultats[0]['latitude'], resultats[0]['longitude']

def charger_releves(
    ville: str = "Toulon",
    coordonnees: tuple[float, float] | None = None,
) -> dict[str, float]:
    """Charge les relevés de température pour une ville via Open-Meteo.
    Args:
        ville: Nom de la ville (str). Toulon par défaut.
        coordonnees: Couple (latitude, longitude) optionnel. Quand il est fourni,
                     localiser n'est pas appelé (évite un double géocodage).
    Returns:
        dict: Dictionnaire {date ISO: température} pour les 14 jours :
              les 7 premiers jours sont des relevés passés (observations),
              les 7 derniers des prévisions à venir.
              La température est la moyenne de la temp max et min de chaque jour.
    Raises:
        ValueError: Si la ville est introuvable.
        RuntimeError: Si l'appel API échoue.
    """
    if coordonnees is None:
        latitude, longitude = localiser(ville)
    else:
        latitude, longitude = coordonnees
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&timezone=Europe/Paris"
        "&daily=temperature_2m_max,temperature_2m_min&past_days=7&forecast_days=7"
    )

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        raise RuntimeError(f"Échec de la récupération des données météo : {e}") from e

    dates = data['daily']['time']
    temp_max = data['daily']['temperature_2m_max']
    temp_min = data['daily']['temperature_2m_min']

    releves = {}
    for i in range(len(dates)):
        moyenne_temp = (temp_max[i] + temp_min[i]) / 2
        releves[dates[i]] = round(moyenne_temp, 1)
    return releves

if __name__ == "__main__":
    try:
        releves = charger_releves()
        m = moyenne(releves)
        maxi, jour = jour_le_plus_chaud(releves)
        nb = jours_au_dessus(releves, m)
        froid, jour_froid = jour_le_plus_froid(releves)
        print(f"La moyenne est de {m:.1f}")
        print(f"Le jour le plus chaud est {jour} avec {maxi}°C")
        print(f"Nombre de jours au-dessus de la moyenne : {nb}")
        print(f"Le jour le plus froid est {jour_froid} avec {froid}°C")
    except (ValueError, RuntimeError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
