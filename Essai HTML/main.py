from pyscript import document as doc
from time import sleep

meteo="Soleil"
saison="Printemps"
jour=0
nom="Sim City 2.0"

matrice_de_base = [
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1]
]

#//Code des cases:
#//0: Détruite
#//1: Nature
#//2: Résidence
#//3: Energie
#//4: Emploie
doc.querySelector("#infos").innerText = "Saison: "+saison+" | Meteo: "+meteo+" | Jour: "+str(jour)
doc.querySelector("#nom").innerText = nom
doc.querySelector("#bas").innerText = "Lancement de l'année..."

def animation_haut():
    base="Création de la ville"
    point="."
    a=0
    for i in range(10):
        a+=1
        base+=point*a
        if a==3:
            a=0
            base="Création de la ville"
        doc.querySelector("#haut").innerText = base


        



def affichage(matrice): #Retourne une liste de liste (map de la journée)
    doc.querySelector("#haut").innerText = matrice






'''
def initialisation():
    #Initialisation:
    
    L'initialisation se déroule comme suit:
    - On lance la fenêtre, affichage:
        - En haut, "Création de ville"
        - En bas, "Lancement de l'année"
        - Au milieu, La grille de 10*10
        - A droite, la sélection de la case à mettre au niveau des clics de souris sur la grille
    

def boucle_principale(carte):
    #Simulation
    
    On attend la doc
    - Calculer la nouvelle carte
    - Afficher
    

def enregistrer(carte):
    #Conclusion
    
    Enregistrer la carte en png
    

def simulation():
    map = initialisation()
    map = boucle_principale(map)
    enregistrer(map)
'''