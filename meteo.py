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
