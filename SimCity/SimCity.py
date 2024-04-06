import tkinter as tk
from PIL import Image, ImageTk
import api
from Cases import Case

class Case:
    def __init__(self, vie, voisins1, voisins2, voisins3, type1,coordonnees):
        self.vie = vie
        self.voisins1 = voisins1
        self.voisins2 = voisins2
        self.voisins3 = voisins3
        self.type = type1
        self.coordonnees = coordonnees

class SimCity:
    def __init__(self):
        self.title = "SimCity"
        self.version = 1.0
        self.taille_carte = 10
        self.fenetre = tk.Tk()
        self.taille_fenetre = 53 * 12
        self.fenetre.maxsize(53 * 12, 53 * 12)
        self.fenetre.minsize(53 * 12, 53 * 12)
        self.saison = "Printemps"
        self.jour = 1
        self.meteo = "Ensoleillé"

        self.carte = []  # Maintenant une liste d'objets Case
        for x in range(self.taille_carte):
            ligne = []
            for y in range(self.taille_carte):
                case = Case(100, [], [], [], 0, (x,y))
                ligne.append(case)
            self.carte.append(ligne)

        self.rgb_nature = (0, 255, 0)
        self.rgb_residence = (0, 0, 255)
        self.rgb_emploi = (255, 165, 0)
        self.rgb_energie = (255, 255, 0)
        self.rgb_detruit = (255, 0, 0)

        api.creer_texte(self.fenetre, 53 * 1.5, 0, f"Jour: {str(self.jour)}")
        api.creer_texte(self.fenetre, 53 * 4, 0, f"Saison: {self.saison}")
        api.creer_texte(self.fenetre, 53 * 8, 0, f"Météo: {self.meteo}")

        self.fenetre.title(self.title)
        api.centrer_fenetre(self.fenetre, self.taille_fenetre, self.taille_fenetre)
        self.fenetre.iconbitmap("ressources/fenetre/icone.ico")

    def exporter_carte(self, carte):
        """
        1 - Vert: Nature
        2 - Bleu: Résidence
        3 - Orange: Emploi
        4 - Jaune: Energie
        5 - Rouge: Détruit
        """

        image = Image.new("RGB", (10, 10), color="white")

        x=0
        for ligne in carte:
            y=0
            for case in ligne:
                if case == 1: # 1 - Vert: Nature
                    image.putpixel((x, y), (0, 255, 0))
                if case == 2: # 2 - Bleu: Ville
                    image.putpixel((x, y), (0, 0, 255))
                if case == 3: # 3 - Orange: Emploi
                    image.putpixel((x, y), (255, 165, 0))
                if case == 4: # 4 - Jaune: Energie
                    image.putpixel((x, y), (255, 255, 0))
                if case == 5: # 5 - Rouge: Détruit
                    image.putpixel((x, y), (255, 0, 0))
                y+=1
            x+=1

        image.save("carte.png")

    def importer_carte(self, path):
        self.carte=[[0 for _ in range(self.taille_carte)] for _ in range(self.taille_carte)]
        image = Image.open(path)
        hauteur, largeur = image.size
        for x in range(hauteur):
            for y in range(largeur):
                pixel = image.getpixel((x, y))
                if pixel == self.rgb_nature:
                    self.carte[x][y]=1
                if pixel == self.rgb_residence:
                    self.carte[x][y]=2
                if pixel == self.rgb_emploi:
                    self.carte[x][y]=3
                if pixel == self.rgb_energie:
                    self.carte[x][y]=4
                if pixel == self.rgb_detruit:
                    self.carte[x][y]=5

        api.creer_boutons(self.fenetre, self.carte)

    def affichage(self):
        self.fenetre.mainloop()

sim=SimCity()
sim.importer_carte("carte.png")
sim.affichage()