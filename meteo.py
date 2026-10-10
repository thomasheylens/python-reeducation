def moyenne(valeurs):
    return sum(valeurs) / len(valeurs)

def maximale(valeurs, jours):
    maxi = valeurs[0]
    jour_max = jours[0]
    for i in range(len(valeurs)):
        if valeurs[i] > maxi:
            maxi = valeurs[i]
            jour_max = jours[i]
    return maxi, jour_max

def jours_au_dessus(valeurs, seuil):
    resultat = 0
    for i in range(len(valeurs)):
        if valeurs[i] > seuil:
            resultat += 1
    return resultat

temp = [12, 15, 9, 11, 7, 13, 12]
jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
m = moyenne(temp)
print(f"La moyenne est de {m:.1f}")
maxi, jour = maximale(temp, jours)
print(f"Le jour le plus chaud est {jour} avec {maxi}°C")
nb = jours_au_dessus(temp, m)
print(f"Nombre de jours au-dessus de la moyenne : {nb}")