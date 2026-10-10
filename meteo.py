def moyenne(releves):
    return sum(releves.values()) / len(releves)

def maximale(releves):
    maxi = -float('inf')
    jour_max = None
    for jour, temp in releves.items():
        if temp > maxi:
            maxi = temp
            jour_max = jour
    return maxi, jour_max

def jours_au_dessus(releves, seuil):
    resultat = 0
    for temp in releves.values():
        if temp > seuil:
            resultat += 1
    return resultat

def jour_le_plus_froid(releves):
    mini = float('inf')
    jour_min = None
    for jour, temp in releves.items():
        if temp < mini:
            mini = temp
            jour_min = jour
    return mini, jour_min

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