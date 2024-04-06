class Case:
    def __init__(self, vie, voisins1, voisins2, voisins3, type, x, y):
        self.vie = vie
        self.voisins1 = voisins1
        self.voisins2 = voisins2
        self.voisins3 = voisins3
        self.type = type
        self.coordonnees = (x,y)

class SimCity:
    def __init__(self):
        # Autres initialisations restent inchangées

        self.carte = []  # Maintenant une liste d'objets Case
        for x in range(self.taille_carte):
            ligne = []
            for y in range(self.taille_carte):
                # Initialisation de chaque case avec des valeurs par défaut
                case = Case(vie=100, voisins1=[], voisins2=[], voisins3=[], type_=0, coordonnees=(x, y))
                ligne.append(case)
            self.carte.append(ligne)

