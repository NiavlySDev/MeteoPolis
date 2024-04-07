import tkinter as tk
from PIL import Image, ImageTk
from Cases import Case
from Modification import Modification
import api

class MeteoPolis:
    def __init__(self):
        self.title = "MeteoPolis"
        self.version = 1.2
        self.fenetre = tk.Tk()
        self.taille_fenetre = (api.taille_case+3) * 12
        self.fenetre.maxsize((api.taille_case+3) * 12, (api.taille_case+3) * 12)
        self.fenetre.minsize((api.taille_case+3) * 12, (api.taille_case+3) * 12)
        self.saison = "Printemps"
        self.jour = 1
        self.meteo = "Ensoleillé"

        self.carte = []

        self.rgb_nature = (0, 255, 0)
        self.rgb_residence = (0, 0, 255)
        self.rgb_emploi = (255, 165, 0)
        self.rgb_energie = (255, 255, 0)
        self.rgb_detruit = (255, 0, 0)

        api.creer_texte(self.fenetre, (api.taille_case+3) * 1.5, 0, f"Jour: {str(self.jour)}")
        api.creer_texte(self.fenetre, (api.taille_case+3) * 4, 0, f"Saison: {self.saison}")
        api.creer_texte(self.fenetre, (api.taille_case+3) * 8, 0, f"Météo: {self.meteo}")

        self.fenetre.title(self.title+" v"+str(self.version))
        api.centrer_fenetre(self.fenetre, self.taille_fenetre, self.taille_fenetre)
        self.fenetre.iconbitmap("ressources/fenetre/icone.ico")
        bouton = tk.Button(self.fenetre, text="Modifier", command=self.modifier)
        bouton.place(x=(api.taille_case*5.8), y=(api.taille_case*12))

        self.carte = []  # Initialisation de la liste de cartes
        for i in range(api.taille_carte):
            ligne = []  # Initialisation de la ligne courante
            for j in range(api.taille_carte):
                case = Case(100, "Nature")  # Création d'une nouvelle case avec vie=100 et typecase="Nature"
                ligne.append(case)  # Ajout de la case à la ligne courante
            self.carte.append(ligne)  # Ajout de la ligne à la liste de cartes
        api.creer_boutons(self.fenetre, self.carte, api.taille_case)

    def __str__(self):
        s = ""
        for ligne in self.carte:
            s += "["
            for case in ligne:
                s += str(case)  # Utilisation de la méthode __str__ de la classe Case
            s += "]\n"
        return s

    def modifier(self):
        self.fenetre.destroy()
        mod=Modification()
        mod.creer_boutons(mod.fenetre, api.importer_carte("carte.png"), mod.taille_case)
        mod.affichage()

    def affichage(self):
        self.fenetre.mainloop()

sim=MeteoPolis()
api.creer_boutons(sim.fenetre, api.importer_carte("carte.png"), api.taille_case)
sim.affichage()