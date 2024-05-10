def simplex(objective, contraintes, solutions):
    nbr_contraintes = len(contraintes)
    nbr_var = len(objective)

    #creation des indices dans la base
    var_dans_base = [i for i in range(nbr_var - nbr_contraintes + 1, nbr_var + 1)]

    """
    donne l'indice [ligne, colonne] du pivot actuel
    @return []
    """
    def choix_pivot():
        nonlocal nbr_contraintes

        #Choix variable entrante
        #recherche maximum positive
        valeur_maximum = max(objective)
        if valeur_maximum <= 0:
            return None
        colonne_pivot = objective.index(valeur_maximum)

        #choix variable sortante
        #recherche minimum ratio
        minimum = float('inf')
        ligne_pivot = -1
        for i in range(0, nbr_contraintes):
            if contraintes[i][colonne_pivot] == 0 :
                continue
            rapport = solutions[i] / contraintes[i][colonne_pivot]
            if  rapport > 0 and rapport < minimum:
                ligne_pivot = i 
                minimum = rapport 
        #La solution est deja optimale
        if ligne_pivot == -1:
            return None
    
        return [ligne_pivot, colonne_pivot]
    
    pivot = choix_pivot()
    while pivot != None:

        ligne_pivot,colonne_pivot = pivot
        valeur_pivot = contraintes[ligne_pivot][colonne_pivot]

        #rendre la valeur du pivot a 1
        contraintes[ligne_pivot] = [x/valeur_pivot for x in contraintes[ligne_pivot]]
        solutions[ligne_pivot] = solutions[ligne_pivot] / valeur_pivot

        #Annuler les pseudo-pivots dans les contraintes et les solutions des variables dans base
        #pseudo-pivot les valeurs qui ont la meme colonne que le pivot
        for i in range(0, len(contraintes)):
            if i == ligne_pivot :
                continue
            #valeur du chiffre sur la meme colonne que le pivot
            valeur_pseudo_pivot = contraintes[i][colonne_pivot]
            contraintes[i] = [x - valeur_pseudo_pivot * y for  x,y in zip(contraintes[i], contraintes[ligne_pivot]) ]
            solutions[i] = solutions[i] - valeur_pseudo_pivot * solutions[ligne_pivot]

        #Annuler les pseudo-pivots dans l'objective et la solution de l'objective
        valeur_pseudo_pivot = objective[colonne_pivot]
        objective = [x - valeur_pseudo_pivot * y  for x,y in zip(objective, contraintes[ligne_pivot])]
        solutions[-1] = solutions[-1] - valeur_pseudo_pivot * solutions[ligne_pivot]
        var_dans_base [ligne_pivot] = colonne_pivot + 1

        #pivotage
        pivot = choix_pivot()

    return (var_dans_base, solutions, objective)

objective = [3, 2, 0, 0]
contraintes = [
    [2, 1, 1, 0],
    [1, 1, 0, 1]
]
solutions = [100, 80, 0]

# objective = [30, 50, 0, 0, 0]
# contraintes = [
#     [3, 2, 1, 0, 0],
#     [1, 0, 0, 1, 0],
#     [0, 1, 0, 0, 1]
# ]
# solutions = [1800, 400, 600, 0]

print(simplex(objective, contraintes, solutions))

    
        


    




