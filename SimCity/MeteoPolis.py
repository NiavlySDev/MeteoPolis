import tkinter as tk
from PIL import Image, ImageTk
from Cases import Case
from Modification import Modification
# import Graphe
import time
import api

class Meteopolis:
    #selon la doc
    def __init__(self, nb_lignes = 10, nb_colonnes = 10, type = "Nature", tempo = 5) -> None:
        self.carte = []
        self.jour = 1
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

        self.fenetre = tk.Tk()
        self.taille_fenetre = (api.taille_case+3) * 12
        self.fenetre.maxsize(self.taille_fenetre, self.taille_fenetre)
        self.fenetre.minsize(self.taille_fenetre, self.taille_fenetre)

        self.fenetre.title(api.title+" "+api.version)

        api.centrer_fenetre(self.fenetre, self.taille_fenetre, self.taille_fenetre)

        self.fenetre.iconbitmap(api.LOGO)

        self.maj()

        self.editeur=Modification(self)

    def __str__(self) -> str:
        resultat = ''
        for i in self.carte:
            ligne = ''
            for j in i:
                ligne += j.typecase + ' '
            resultat += ligne + '\n'
        return resultat

    def maj(self):
        for widget in self.fenetre.winfo_children():
            widget.destroy()
        api.creer_texte(self.fenetre, (api.taille_case+3) * 4, 0, f"Saison: {self.saison}", 15)
        api.creer_texte(self.fenetre, (api.taille_case+3) * 1.5, 0, f"Jour: {str(self.jour)}", 15)
        api.creer_texte(self.fenetre, (api.taille_case+3) * 8, 0, f"Méteo: {self.temps}", 15)

        bouton = tk.Button(self.fenetre, text="Modifier", command=self.editeur)
        bouton.place(x=(api.taille_case*5.8), y=(api.taille_case*12))

        api.creer_boutons(self.fenetre, self.carte, api.taille_case)

    def editeur(self) -> None:
        self.editeur.maj()

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

    def simulation(saison_depart, nom_fichier = "") -> int:
        #Je créé une instance de Meteopolis()
        ville = Meteopolis()

        if nom_fichier != "":
            #Je charge la carte depuis le fichier
            carte = api.lecture_fichier(nom_fichier)
        else:
            carte=ville.carte

        ville.carte=carte

        ville.maj()

        # ville.set_saison(saison_depart)

        ville.fenetre.mainloop()

        """
        # Je passe les 4 saisons
        for i in range(4):
            #Je passe les 30 jours
            for j in range(30):
                # Methode d'affichage à implémenter
                ville.incremente_jour()
                Graphe.ville_de_demain(ville) # Calcul de la ville du lendemain
                time.sleep(ville.tempo) # Pause de tempo secondes
            ville.set_saison() # J'incrémente la saison
        return Graphe.calcul_score(ville)
        """

Meteopolis.simulation("Ete", "carte.csv")