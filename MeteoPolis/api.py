import tkinter as tk
from PIL import Image, ImageTk
from Cases import Case

import csv
import MeteoPolis

##### Paramètres (Modifiable) #####

def parametre_modifiable() -> int:
    return 48 #"zoom" de la fenêtre

###################################

##### Paramètres (Non-Modifiable) #####

def parametres_immuables() -> dict:
    dico = {
        'LOGO' : "ressources/fenetre/icone.ico",

        'rgb_nature' : (0, 255, 0),
        'rgb_residence' : (0, 0, 255),
        'rgb_emploi' : (255, 165, 0),
        'rgb_energie' : (255, 255, 0),
        'rgb_detruit' : (255, 0, 0),

        'title' : "MeteoPolis",
        'version' : "v0.9.3",
        'tempo': 5
    }
    saisons = ["printemps", "ete", "automne", "hiver", "chaos"]
    cases = ["nature", "residence", "energie", "emploi", "detruit"]

    #Chargement des textures dans les fichiers
    for saison in saisons:
        for case in cases:
            dico[f"{case}_{saison}"]=Image.open(f"ressources/map/{case}/{case}_{saison}.png")

    return dico

#######################################


 #Changez la rapidité de défilement des jours en bas du code de ce fichier, vous trouverez:
""" return self.application.after(self.meteopolis.get_tempo() * [nb_ms], self.simuler_une_annee)
 changez le nombre nb_ms, remplacez le par le nombre de millisecondes par jour * 5.  """


##### Gérer les fichiers de la carte #####
# /!\ ne pas toucher à ces méthodes! /!\ #

def lecture_fichier(nom_fichier : str) -> list :
    """Lire et Appliquer un fichier csv sur une carte"""
    with open(nom_fichier, newline= "", encoding= 'utf-8') as f :
        fichier = csv.reader(f, delimiter = ';')
        carte = []
        for ligne in fichier :
            ligne=conversion_ligne(ligne)
            ligne2=[]
            for item in ligne:
                item=Case(item[0], item[1])
                ligne2.append(item)
            carte.append(ligne2)
        return carte

# /!\ ne pas toucher à ces méthodes! /!\ #

def conversion_ligne(liste : str) -> list:
    """Fonction permettant de bien charger le fichier csv"""
    liste2=[]

    for case in liste:
        temp,tempnb="",""
        for lettre in case:
            if lettre in "1234567890":
                tempnb+=lettre
            if lettre in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                temp+=lettre
            if lettre == ")":
                liste2.append((int(tempnb),temp))
                tempnb=""
                temp=""
    return liste2

# /!\ ne pas toucher à ces méthodes! /!\ #

def ecriture_fichier(carte : list, nom_fichier : str) -> None :
    """Sauvegarder la carte dans un fichier csv"""
    with open(nom_fichier,'w',newline="",encoding='utf-8') as f :
        csv.writer(f, delimiter = ';').writerows(carte)

# /!\ ne pas toucher à ces méthodes! /!\ #
##########################################

#Qu'on soit d'accord, vous n'avez aucune raison de modifier le code!
#Néanmoins, si vous le modifiez et que cela ne fonctionne plus:
#Sauvegardez vos cartes autre part (que dans le dossier) et retéléchargez la bonne version

##### Classe Application, gérant tout l'affichage #####

class Application:

    ## Fonction d'initialisation de la classe ##
    def __init__(self, saison_de_depart : str = 'Printemps', nom_fichier : str = '') -> None:
        #Je récupère les liens de toutes les images, les couleurs, le titre et la version du programme
        self.parametres = parametres_immuables()

        #J'initialise la fenêtre et la stocke en attribut de la classe
        self.application = tk.Tk()
        self.application.title(self.parametres['title'])

        #Je créé la ville et la stocke en attribut de la classe
        self.meteopolis = MeteoPolis.Meteopolis()

        #Je charge la carte depuis le fichier si nom_fichier n'est pas vide
        if nom_fichier != "":
            carte = lecture_fichier(nom_fichier)
            #Je remplace la carte par défaut par la carte chargée
            self.meteopolis.carte=carte

        #Je récupère la taille de cases souhaitée
        self.taille_cases = parametre_modifiable()

        #Je stocke directement, en attribut de la classe, les dimensions de la carte (toujours un carré)
        taille_carte = self.meteopolis.nb_lignes

        #Je stocke la saison de départ, et le nom du fichier au cas où
        self.saison_de_depart = saison_de_depart
        self.nom_fichier = nom_fichier

        #Booléen stipulant si la simulation est lancée ou non
        self.simulation = False

        #Booléen stipulant si l'on doit afficher les stats des cases
        self.stats = False

        #Je stocke la taille de la fenêtre en fonction de la taille des cases
        self.taille_fenetre = (self.taille_cases+3) * 12

        #Je change la fenêtre, en stipulant sa taille (min et max), son titre et son logo
        self.application.maxsize(self.taille_fenetre, self.taille_fenetre)
        self.application.minsize(self.taille_fenetre, self.taille_fenetre)
        self.application.title("MeteoPolis"+" " + self.parametres['version'])
        self.application.iconbitmap(self.parametres['LOGO'])

        #Je centre la fenêtre
        self.centrer_fenetre()

        #J'affiche le contenu de la fenêtre
        self.affichage()

        #Je lance la fenêtre
        self.application.mainloop()


    ## Fonction permettant de centrer la fenêtre au milieu de l'écran ##
    def centrer_fenetre(self) -> None:
        #Je récupère la largeur de l'écran
        largeur_ecran = self.application.winfo_screenwidth()

        #Je récupère la hauteur de l'écran
        hauteur_ecran = self.application.winfo_screenheight()

        #Je calcul où doit se trouver le coin en haut à gauche de la fenêtre sur l'écran. (coo 0, 0 de la fenêtre)
        x = (largeur_ecran - self.taille_fenetre) // 2
        y = (hauteur_ecran - self.taille_fenetre) // 2

        #Je position la fenêtre au milieu de l'écran
        self.application.geometry(f"{self.taille_fenetre}x{self.taille_fenetre}+{x}+{y}")


    ## Fonction gérant l'affichage de base et l'affichage de la simulation ##
    def affichage(self) -> None:
        #Je vide la fenêtre
        self.reset_affichage()

        #Affichage de base
        if not self.simulation:
            #Création du bouton qui appelle la fonction simulation de la classe Meteopolis
            lancer = tk.Button(self.application, text='LANCER LA SIMULATION', command = lambda: self.meteopolis.simulation(self))
            #Afficher le bouton pour lancer la simulation
            lancer.pack(side='top')

            #Changement de la taille de la fenêtre
            self.application.maxsize(self.taille_fenetre, self.taille_fenetre)
            self.application.minsize(self.taille_fenetre, self.taille_fenetre)

            #Changement du titre
            self.application.title(parametres_immuables()["title"]+" "+parametres_immuables()["version"]+" [Accueil]")

        #Affichage en simulation
        else:
            self.creer_texte(self.application, (self.taille_cases+3) * 1.5, 0, f"Jour: {str(self.meteopolis.jour)}", 15)

            #Affichage de la saison
            self.creer_texte(self.application, (self.taille_cases+3) * 4, 0, f"Saison: {self.meteopolis.saison}", 15)

            #Affichage de la météo
            self.creer_texte(self.application, (self.taille_cases+3) * 8, 0, f"Méteo: {self.meteopolis.temps}", 15)

            #Changement du titre
            self.application.title(parametres_immuables()["title"]+" "+parametres_immuables()["version"]+" [Simulation]")

            #Création d'un bouton pour définir si l'on doit afficher les stats ou non
            afficher_stats = tk.Button(self.application, text='STATS', command = lambda : self.changer_stats())
            afficher_stats.pack(side='bottom')

            #Création d'un texte pour expliquer le fonctionnement du bouton stats
            self.creer_texte(self.application, self.taille_fenetre//2 - 155, self.taille_fenetre-45, "ce bouton change l'affichage à partir du prochain jour", 10)

        #Si l'on affiche pas les statistiques
        if not self.stats:
            ## Affichage de la carte avec textures ##
            #Définition de la position horizontale des cases
            x2 = self.taille_cases + 3

            #Parcours des lignes de la carte
            for ligne in self.meteopolis.carte:

                #Définition de la position verticale des cases
                y2 = self.taille_cases + 3

                #Parcours des cases de la ligne
                for case in ligne:
                    #Définition des textures de chaque boutons
                    if self.meteopolis.saison != "":
                        image_originale = self.parametres[f"{case.typecase.lower()}_{self.meteopolis.saison.lower()}"]
                    else:
                        image_originale = self.parametres[f"{case.typecase.lower()}_{self.saison_de_depart.lower()}"]

                    #Changer la taille des textures pour s'adapter à la taille voulue des cases
                    image_redimensionnee = image_originale.resize((self.taille_cases, self.taille_cases))
                    image_tk = ImageTk.PhotoImage(image_redimensionnee)

                    #Créer une case avec la texture
                    bouton = tk.Button(self.application, image=image_tk)
                    bouton.image = image_tk

                    #Afficher la case
                    bouton.pack()
                    bouton.place(x=x2, y=y2)

                    #J'incrémente la position verticale de la prochaine case
                    y2 += self.taille_cases + 3
                #J'incrémente la position horizontale de la prochaine case
                x2 += self.taille_cases + 3
        #Si l'on affiche les statistiques
        else:
            ## Affichage de la carte avec stats ##
            #Définition de la position horizontale des cases
            x2 = self.taille_cases + 3

            #Parcours des lignes de la carte
            for ligne in self.meteopolis.carte:

                #Définition de la position verticale des cases
                y2 = self.taille_cases + 3

                #Parcours des cases de la ligne
                for case in ligne:
                    #Définition des textures de chaque boutons
                    if case.typecase == "Nature":
                        image_originale = self.parametres['rgb_nature']
                    elif case.typecase == "Residence":
                        image_originale = self.parametres['rgb_residence']
                    elif case.typecase == "Emploi":
                        image_originale = self.parametres['rgb_emploi']
                    elif case.typecase == "Energie":
                        image_originale = self.parametres['rgb_energie']
                    elif case.typecase == "Out":
                        image_originale = self.parametres['rgb_detruit']
                    else:
                        raise ValueError(f"Type inconnu: {case.typecase}")

                    #Charger la texture avec les bonnes dimensions
                    image_redimensionnee = Image.new("RGB", (self.taille_cases, self.taille_cases), image_originale)
                    image_tk = ImageTk.PhotoImage(image_redimensionnee)

                    #Créer une case avec la texture
                    bouton = tk.Button(self.application, image=image_tk, text=str(case.vie) + '\n' + case.typecase, font=("Arial", 7), compound=tk.CENTER)
                    bouton.image = image_tk

                    #Afficher la case
                    bouton.pack()
                    bouton.place(x=x2, y=y2)

                    #J'incrémente la position verticale de la prochaine case
                    y2 += self.taille_cases + 3
                #J'incrémente la position horizontale de la prochaine case
                x2 += self.taille_cases + 3

        #Si la simulation n'est pas lancée
        if not self.simulation:
            #Je créé le bouton pour entrer dans l'interface de modification de l'app
            modif = tk.Button(self.application, text='MODIFIER LA CARTE', command = lambda: self.affichage_modifications())
            #J'affiche le bouton
            modif.pack(side='bottom')

    def __EST__(self):
        from random import choice
        from __pycache__ import AoDpojFZpoj
        return choice(AoDpojFZpoj.dFzlknSQLkn())

    ## Méthode d'affichage du menu de modifications ##
    def affichage_modifications(self) -> None:
        #Changement de la taille de la fenêtre
        self.application.maxsize(self.taille_fenetre, self.taille_fenetre + 110)
        self.application.minsize(self.taille_fenetre-100, self.taille_fenetre + 10)

        #Changement du titre de la fenêtre
        self.application.title(parametres_immuables()["title"]+" "+parametres_immuables()["version"]+" [Editeur]")

        #Nettoyer la fenêtre
        self.reset_affichage()

        #Titre du menu au-dessus de la carte
        self.creer_texte(self.application, (self.taille_cases+3) * 4.25, 25, 'MODIFICATION DE LA CARTE', 10)

        ## Affichage de la carte, même méthode que la précédente méthode d'affichage, sauf la ligne commentée ##
        x2 = self.taille_cases + 3
        for i, ligne in enumerate(self.meteopolis.carte):
            y2 = self.taille_cases + 3
            for j, case in enumerate(ligne):
                #Définition des textures de chaque boutons
                if self.meteopolis.saison != "":
                    image_originale = self.parametres[f"{case.typecase.lower()}_{self.meteopolis.saison.lower()}"]
                else:
                    image_originale = self.parametres[f"{case.typecase.lower()}_{self.saison_de_depart.lower()}"]

                image_redimensionnee = image_originale.resize((self.taille_cases, self.taille_cases))
                image_tk = ImageTk.PhotoImage(image_redimensionnee)
                #Je créé un bouton, avec pour propriété d'appeler la fonction qui permet à la case de changer son types (changer_nature_case(coo))
                #Le i=i et j=j permet de faire en sorte que le bouton garde sa position en mémoire,
                #et qu'il puisse directement appeler la modification sur sa position
                bouton = tk.Button(self.application, image=image_tk, command=lambda i=i, j=j: self.changer_nature_case((i, j)))
                bouton.image = image_tk
                bouton.pack()
                bouton.place(x=x2, y=y2)
                y2 += self.taille_cases + 3
            x2 += self.taille_cases + 3

        # Variable pour stocker la sélection des radioboutons
        self.var = tk.IntVar()

        #Création d'un panneau pour contenir l'interface d'intéraction, et d'un panneau pour l'interface de sauvegarde
        self.Actions = tk.Frame(self.application)
        self.Sauvegarde = tk.Frame(self.application)

        # Création des radioboutons dans le panneau Actions, permettant de choisir entre chaque case
        self.radio_choix1 = tk.Radiobutton(self.Actions, text="Nature", variable=self.var, value=1)
        self.radio_choix2 = tk.Radiobutton(self.Actions, text="Résidence", variable=self.var, value=2)
        self.radio_choix3 = tk.Radiobutton(self.Actions, text="Emploi", variable=self.var, value=3)
        self.radio_choix4 = tk.Radiobutton(self.Actions, text="Energie", variable=self.var, value=4)

        #Affichage des radioboutons
        self.radio_choix1.pack(side='left')
        self.radio_choix2.pack(side='left')
        self.radio_choix3.pack(side='left')
        self.radio_choix4.pack(side='left')

        #Bouton dans le panneau Actions permettant de sortir de l'interface de modification
        self.retour = tk.Button(self.Actions, text = 'RETOUR', command = lambda: self.affichage())

        #Affichage du bouton de retour
        self.retour.pack(side=tk.TOP)

        #Création du bouton de sauvegarde, appelant la méthode save()
        self.Bouton_de_sauvegarde = tk.Button(self.Sauvegarde, text="Sauvegarder la carte sous le nom de: ", command=lambda:self.save())
        #Affichage du bouton de sauvegarde
        self.Bouton_de_sauvegarde.pack(side=tk.LEFT)

        #Création de l'espace d'entrée texte pour le nom de la carte à enregistrer
        self.Nom_De_Carte = tk.Entry(self.Sauvegarde)
        #Affichage de l'espace d'entrée texte
        self.Nom_De_Carte.pack(side=tk.LEFT)

        #Affichage du panneau de sauvegarde
        self.Sauvegarde.pack(side='bottom')

        #Affichage du panneau d'Actions
        self.Actions.pack(side='bottom')


    ## Méthode pour changer la nature de la case dont les coo sont en argument ##
    def changer_nature_case(self, coo : tuple) -> None:
        #Je récupère la sélection des radioboutons
        self.type = self.var.get()

        #J'appelle la fonction de la classe Case sur la case aux coordonnées indiquées en argument
        if self.type == 1:
            self.meteopolis.carte[coo[0]][coo[1]].new_type('Nature')
        elif self.type == 2:
            self.meteopolis.carte[coo[0]][coo[1]].new_type('Residence')
        elif self.type == 3:
            self.meteopolis.carte[coo[0]][coo[1]].new_type('Emploi')
        elif self.type == 4:
            self.meteopolis.carte[coo[0]][coo[1]].new_type('Energie')

        #Une fois la carte modifiée, j'actualise l'affichage
        self.affichage_modifications()


    ## Méthode qui sauvegarde la carte ##
    def save(self) -> None:
        #Je récupère le nom de carte rentré dans l'espace texte
        self.nom_fichier = self.Nom_De_Carte.get()

        #Si le nom entré n'est pas vide, j'appel la méthode de sauvegarde avec la carte et nom_fichier en argument
        if self.nom_fichier != '':
            ecriture_fichier(self.meteopolis.carte, self.nom_fichier + '.csv')


    ## Créé un texte (texte) de taille (taille) aux coordonnées (x2, y2) dans la fenêtre fenetre (fenetre) ##
    def creer_texte(self, fenetre, x2 : int, y2 : int, texte : str, taille : int) -> None:
        #Je créé un texte tkinter
        texte_label = tk.Label(fenetre, text=texte)

        #Je défini la police et la taille du texte
        texte_label.config(font=("Helvetica", taille))

        #Je défini la position du texte et l'affiche
        texte_label.place(x=x2, y=y2)


    ## Switch la variable stats ##
    def changer_stats(self):
        if self.stats:
            self.stats = False
        else:
            self.stats = True


    ## Méthode supprimant l'ensemble des objets dans la fenêtre ##
    def reset_affichage(self) -> None:
        #Je parcours l'ensemble des éléments de la fenêtre
        for widget in self.application.winfo_children():
            #Je détruit l'élément
            widget.destroy()


    ## Méthode lançant la simulation ##
    def lancer_simulation(self):
        #Je passe à True le booléen stipulant que la simulation est lancée
        self.simulation = True

        #Je définis la saison de départ de la simulation
        self.meteopolis.set_saison(self.saison_de_depart)

        #J'initialise le compteur de saisons à 1
        self.nb_saison = 1

        #Je simule une année
        return self.simuler_une_annee()


    ## Méthode lançant une simulation d'un an ##
    def simuler_une_annee(self):
        #Code provisoire, c'est la classe Graphe qui incrémentera les jours
        if self.meteopolis.get_jour() == 31:
            self.meteopolis.jour = 0
            self.meteopolis.set_saison()
            self.nb_saison += 1

        #Condition d'arrêt, quand la saison 4 est dépassée, on retourne le score de la simulation
        if self.nb_saison == 5:
            return Graphe.calcul_score(self.meteopolis)

        #J'affiche la carte
        self.affichage()

        #J'incrémente le numéro de la journée
        self.meteopolis.incremente_jour()

        #Je calcule la ville de demain
        #Graphe.ville_de_demain(self.meteopolis) # Calcul de la ville du lendemain

        #Appel récursif au bout de (self.meteopolis.get_tempo() * 1000) millisecondes
        return self.application.after(self.meteopolis.get_tempo() * 1000, self.simuler_une_annee)

#######################################################

#Liste des saisons de départ possible
saisons = ["Automne", "Hiver", "Printemps", "Ete"]
#temps = ["Ensoleillé","Nuageux","Pluvieux","Vent","Tempête","Neigeux","Brouillard"]
ok = Application('Printemps', 'Carte.csv')