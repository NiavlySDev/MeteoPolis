import tkinter as tk
from PIL import Image, ImageTk
from Cases import Case
from Modification import Modification
#import Graphe
import time
import api

import csv

def lecture_fichier(nom_fichier) :
    with open(nom_fichier, newline= "", encoding= 'utf-8') as f :
        fichier = csv.reader(f, delimiter = ';')
        carte = []
        for ligne in fichier :
            carte.append(ligne)
        return carte

def ecriture_fichier(carte, nom_fichier) :
    with open(nom_fichier,'w',newline="",encoding='utf-8') as f :
        csv.writer(f, delimiter = ';').writerows(carte)

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
    def __init__(self, nb_lignes = 10, nb_colonnes = 10, type = "Nature", tempo = 5) -> None:
        self.carte = []
        self.jour = 10
        self.saison = ""
        self.chaos = 0
        self.temps = ""
        self.tempo = tempo
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        for i in range(nb_lignes):
            self.carte.append([])
            for j in range(nb_colonnes):
                self.carte[i].append(Case(50, type))

    def __str__(self) -> str:
        resultat = ''
        for i in self.carte:
            ligne = ''
            for j in i:
                ligne += j.typecase + ' '
            resultat += ligne + '\n'
        return resultat

    def get_carte(self) -> list:
        return self.carte

    def get_jour(self) -> int:
        return self.jour

    def get_saison(self) -> str:
        return self.saison

    def get_chaos(self) -> int:
        return self.chaos

    def get_temps(self) -> str:
        return self.temps

    def get_tempo(self) -> int:
        return self.tempo

    def get_coo(self, ligne, colonne, direction = "", nombre_de_pas = 0) -> list:
        if direction == "" or nombre_de_pas == 0:
            return [ligne, colonne]
        for i in range(nombre_de_pas):
            if direction == "Horizontal":
                colonne += nombre_de_pas
            elif direction == "Vertical":
                ligne += nombre_de_pas
            if colonne < 0:
                colonne = self.nb_colonnes + colonne
            elif colonne > self.nb_colonnes:
                colonne = colonne - self.nb_colonnes
            elif ligne < 0:
                ligne  = self.nb_lignes + ligne
            elif ligne > self.nb_lignes:
                ligne = ligne - self.nb_lignes
            return [ligne, colonne]


    def set_carte(self, carte_demain) -> None:
        self.carte = carte_demain

    def set_temps(self, new_temps) -> None:
        self.temps = new_temps

    def set_saison(self, new_saison = "") -> None:
        if new_saison != "":
            self.saison = new_saison
        elif self.saison == "Automne":
            self.saison = "Hiver"
        elif self.saison == "Hiver":
            self.saison = "Printemps"
        elif self.saison == "Printemps":
            self.saison = 'Ete'
        elif self.saison == "Ete":
            self.saison = "Automne"

    def incremente_jour(self) -> None:
        self.jour += 1

    def incremente_chaos(self) -> None:
        self.chaos += 1

    def proches_voisins(self, ligne, colonne) -> list:
        liste = []
        coo = self.get_coo(ligne, colonne, 'Horizontal', 1)
        liste.append(self.carte[coo[0]][coo[1]])
        coo = self.get_coo(ligne, colonne, 'Horizontal', -1)
        liste.append(self.carte[coo[0]][coo[1]])
        coo = self.get_coo(ligne, colonne, 'Vertical', 1)
        liste.append(self.carte[coo[0]][coo[1]])
        coo = self.get_coo(ligne, colonne, 'Vertical', -1)
        liste.append(self.carte[coo[0]][coo[1]])
        return liste


    def voisins(self, ligne, colonne) -> list:
        # On ajoute les 4 cases les plus proches
        proches = self.proches_voisins(ligne, colonne)
        liste = []
        for i in proches:
            liste.append(i)

        # On ajoute les cases accessibles en lignes droites, N, S, E, O
        coo = self.get_coo(ligne, colonne, 'Horizontal', 2)
        liste.append(self.carte[coo[0]][coo[1]])
        coo = self.get_coo(ligne, colonne, 'Horizontal', -2)
        liste.append(self.carte[coo[0]][coo[1]])
        coo = self.get_coo(ligne, colonne, 'Vertical', 2)
        liste.append(self.carte[coo[0]][coo[1]])
        coo = self.get_coo(ligne, colonne, 'Vertical', -2)
        liste.append(self.carte[coo[0]][coo[1]])

        # On ajoute les cases accessibles en diagonale, NE, NO, SE, SO
        coo = self.get_coo(ligne, colonne, 'Vertical', 1)
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', 1)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', -1)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo = self.get_coo(ligne, colonne, 'Vertical', -1)
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', 1)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', -1)
        liste.append(self.carte[coo1[0]][coo1[1]])

        return liste


    def banlieue(self, ligne, colonne) -> list:
        # On ajoute les 12 cases les plus proches
        proches = self.proches_voisins(ligne, colonne)
        liste = []
        for i in proches:
            liste.append(i)

        # On ajoute les cases les plus éloignées
        coo = self.get_coo(ligne, colonne, 'Vertical', 2)
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', 2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', -2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo = self.get_coo(ligne, colonne, 'Vertical', -2)
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', 2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', -2)
        liste.append(self.carte[coo1[0]][coo1[1]])

        # On ajoute les cases manquantes (en cavalier de jeu d'échec)
        coo = self.get_coo(ligne, colonne, 'Vertical', 1)
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', 2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', -2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo = self.get_coo(ligne, colonne, 'Vertical', -1)
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', 2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo1 = self.get_coo(coo[0], coo[1], 'Horizontal', -2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo = self.get_coo(ligne, colonne, 'Horizontal', 1)
        coo1 = self.get_coo(coo[0], coo[1], 'Vertical', 2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo1 = self.get_coo(coo[0], coo[1], 'Vertical', -2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo = self.get_coo(ligne, colonne, 'Horizontal', -1)
        coo1 = self.get_coo(coo[0], coo[1], 'Vertical', 2)
        liste.append(self.carte[coo1[0]][coo1[1]])
        coo1 = self.get_coo(coo[0], coo[1], 'Vertical', -2)
        liste.append(self.carte[coo1[0]][coo1[1]])

        return liste



    def voisinage(self, ligne, colonne) -> list:
        if self.carte[ligne][colonne].typecase == "Residence":
            return self.banlieue(ligne, colonne)
        elif self.carte[ligne][colonne].typecase == "Emploi":
            return self.proches_voisins(ligne, colonne)
        elif self.carte[ligne][colonne].typecase == "Nature" or self.carte[ligne][colonne].typecase == "Energie":
            return self.voisins(ligne, colonne)

    def simulation(saison_depart, nom_fichier) -> int:
        '''
        Lance la simulation sur 1 an (120 jours).
Renvoie le score final.'''
        carte = lecture_fichier(nom_fichier)
        ville = Meteopolis()
        for i in range(len(ville.nb_lignes)):
            for j in range(len(ville.nb_colonnes)):
                ville.carte[i][j] = Case(50, carte[i][j])
        ville.set_saison(saison_depart)

        for i in range(4):
            for j in range(30):
                #Methode d'affichage
                ville.incremente_jour()
                Graphe.ville_de_demain(ville)
                time.sleep(5)
            ville.set_saison()
        return Graphe.calcul_score(ville)
