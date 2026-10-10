def moyenne(releves):
    """Calcule la température moyenne à partir d'un dictionnaire de relevés.

    Args:
        releves: Dictionnaire {jour: température} (ex: {'lundi': 20.5}).

    Returns:
        float: Température moyenne en °C.

    Raises:
        ValueError: Si le dictionnaire est vide.
    """
    if not releves:
        raise ValueError("Le dictionnaire de relevés ne peut pas être vide.")
    return sum(releves.values()) / len(releves)

def maximale(releves):
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

def jours_au_dessus(releves, seuil):
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

def jour_le_plus_froid(releves):
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

releves = {
    "lundi": 12,
    "mardi": 15,
    "mercredi": 9,
    "jeudi": 11,
    "vendredi": 7,
    "samedi": 13,
    "dimanche": 12
}
m = moyenne(releves)
print(f"La moyenne est de {m:.1f}")
maxi, jour = maximale(releves)
print(f"Le jour le plus chaud est {jour} avec {maxi}°C")
nb = jours_au_dessus(releves, m)
print(f"Nombre de jours au-dessus de la moyenne : {nb}")
froid, jour_froid = jour_le_plus_froid(releves)
print(f"Le jour le plus froid est {jour_froid} avec {froid}°C")