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

        api.creer_texte(self.fenetre, (api.taille_case+3) * 4, 0, f"{self.saison}")
        api.creer_texte(self.fenetre, (api.taille_case+3) * 1.5, 0, f"Jour {str(self.jour)}")
        api.creer_texte(self.fenetre, (api.taille_case+3) * 8, 0, f"{self.meteo}")

        self.fenetre.title(self.title+" v"+str(self.version))
        api.centrer_fenetre(self.fenetre, self.taille_fenetre, self.taille_fenetre)
        self.fenetre.iconbitmap("ressources/fenetre/icone.ico")
        bouton = tk.Button(self.fenetre, text="Modifier", command=self.modifier)
        bouton.place(x=(api.taille_case*5.8), y=(api.taille_case*12))

        self.carte = []  # Initialisation de la liste de cartes
        for i in range(api.taille_carte):
            ligne = []  # Initialisation de la ligne courante
            for j in range(api.taille_carte):
                case = Case()  # Création d'une nouvelle case avec vie=100 et typecase="Nature"
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




class Meteopolis:
    #selon la doc
    def __init__(self, nb_lignes = 10, nb_colonnes = 10, type = "Nature", tempo = 5):
        self.carte = []
        self.jour = 10
        self.saison = ""
        self.chaos = 0
        self.temps = ""
        self.tempo = tempo
        for i in range(nb_lignes):
            self.carte.append([])
            for j in range(nb_colonnes):
                self.carte[i].append(Case(50, type))

    def __str__(self):
        resultat = ''
        for i in self.carte:
            ligne = ''
            for j in i:
                ligne += j.typecase + ' '
            resultat += ligne + '\n'
        return resultat

    def get_carte(self):
        return self.carte

    def get_jour(self):
        return self.jour

    def get_saison(self):
        return self.saison

    def get_chaos(self):
        return self.chaos

    def get_temps(self):
        return self.temps

    def get_tempo(self):
        return self.tempo

    def set_carte(self, carte_demain):
        ok = 5

    def set_temps(self, new_temps):
        ok = 5

    def set_saison(self, new_saison = ""):
        ok = 5

    def incremente_jour(self):
        ok = 5

    def incremente_chaos(self):
        ok = 5

    def proches_voisins(self, ligne, colonne):
        ok = 5

    def voisins(self, ligne, colonne):
        ok = 5

    def banlieue(self, ligne, colonne):
        ok = 5

    def voisinage(self, ligne, colonne):
        ok = 5

    def simulation(saison_depart, nom_fichier):
        ok = 5

