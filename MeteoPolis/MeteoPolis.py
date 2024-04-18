import tkinter as tk
from PIL import Image, ImageTk
from Cases import Case
#from graphe_projet3 import Graphe

class Meteopolis:
    def __init__(self, nb_lignes = 10, nb_colonnes = 10, type = "Nature", tempo = 5) -> None:
        self.carte = []
        self.jour = 0
        self.saison = ""
        self.chaos = 0
        self.est_chaos = True
        self.temps = ""
        self.tempo = tempo
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.carte = []

        for i in range(nb_lignes): # Chargement de la carte de Base
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

    # Ancien Code Ici, cf. (Archives -> I)

    def get_carte(self) -> list:
        """Récupérer la carte"""
        return self.carte

    def get_jour(self) -> int:
        """Récupérer le jour actuel"""
        return self.jour

    def get_saison(self) -> str:
        """Récupérer la saison actuelle"""
        return self.saison

    def get_chaos(self) -> int:
        """Récupérer le n° du jour de chaos actuel"""
        return self.chaos

    def get_temps(self) -> str:
        """Récupérer la Météo"""
        return self.temps

    def get_tempo(self) -> int:
        """Récupérer la fréquence de rafraichissement de la carte"""
        return self.tempo

    def get_coo(self, ligne, colonne, direction = "", nombre_de_pas = 0) -> list:
        """Récupérer les coordonnées des cases à un pas de (nombre_de_pas)"""
        if direction == "" or nombre_de_pas == 0:
            return [ligne, colonne]
        if direction == "Horizontal":
            colonne += nombre_de_pas
        elif direction == "Vertical":
            ligne += nombre_de_pas
        if colonne < 0:
            colonne = self.nb_colonnes + colonne
        elif colonne >= self.nb_colonnes:
            colonne = colonne - self.nb_colonnes
        elif ligne < 0:
            ligne  = self.nb_lignes + ligne
        elif ligne >= self.nb_lignes:
            ligne = ligne - self.nb_lignes
        return [ligne, colonne]


    def set_carte(self, carte_demain) -> None:
        """Changer la carte"""
        self.carte = carte_demain

    def set_temps(self, new_temps) -> None:
        """Changer la météo"""
        self.temps = new_temps

    def set_saison(self, new_saison = "") -> None:
        """Changer la saison pour (new_saison) ou pour passer à la saison d'après si (new_saison) est vide"""
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
        """Ajouter un jour"""
        self.jour += 1

    def incremente_chaos(self) -> None:
        """Ajouter un jour de chaos"""
        self.chaos += 1

    def proches_voisins(self, ligne, colonne) -> list:
        """Récupérer les 4 voisins NSEO"""
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
        """Récupérer les voisins au premier cercle (zone de 3x3)"""
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
        """Récupérer les voisins au deuxième cercle (zone de 5x5)"""
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
        else :
            return []

    def simulation(self, application, nom_fichier = ''):
        """Lancer la simulation (directement dans l'interface)"""
        application.lancer_simulation()