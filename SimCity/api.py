import tkinter as tk
from PIL import Image, ImageTk
from Cases import Case

import time
import csv
import MeteoPolis

##### Paramètres (Modifiable) #####

taille_case=48
taille_carte = 10

###################################

##### Paramètres (Non-Modifiable) #####

def parametres_immuables():
    return {'NATURE' : "ressources/map/nature.png",
    'RESIDENCE' : "ressources/map/residence.png",
    'ENERGIE' : "ressources/map/energie.png",
    'EMPLOI' : "ressources/map/emploie.png",
    'DETRUIT' : "ressources/map/terrain_vague.png",
    'LOGO' : "ressources/fenetre/icone.ico",

    'rgb_nature' : (0, 255, 0),
    'rgb_residence' : (0, 0, 255),
    'rgb_emploi' : (255, 165, 0),
    'rgb_energie' : (255, 255, 0),
    'rgb_detruit' : (255, 0, 0),

    'title' : "MeteoPolis",
    'version' : "v0.5.5"}

######################################


# Ancien code ici, cf. (Archives -> II)

def lecture_fichier(nom_fichier : str) :
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


def conversion_ligne(liste):
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


def ecriture_fichier(carte : list, nom_fichier : str) :
    """Sauvegarder la carte dans un fichier csv"""
    with open(nom_fichier,'w',newline="",encoding='utf-8') as f :
        csv.writer(f, delimiter = ';').writerows(carte)


class Application:
    def __init__(self, saison_de_depart, nom_fichier):

        self.parametres = parametres_immuables()

        self.application = tk.Tk()
        self.application.title("MeteoPolis")

        self.meteopolis = MeteoPolis.Meteopolis()

        if nom_fichier != "":
            #Je charge la carte depuis le fichier
            carte = lecture_fichier(nom_fichier)
        else:
            carte=self.meteopolis.carte

        self.meteopolis.carte=carte

        # ville.set_saison(saison_depart)

        self.taille_cases = 48
        taille_carte = self.meteopolis.nb_lignes
        self.saison_de_depart = saison_de_depart
        self.nom_fichier = nom_fichier
        self.simulation = False

        """Crée tous les boutons des interfaces"""
        x2 = self.taille_cases + 3
        for ligne in self.meteopolis.carte:
            y2 = self.taille_cases + 3
            for case in ligne:
                if case.typecase == "Nature":
                    image_originale = Image.open(self.parametres['NATURE'])
                elif case.typecase == "Residence":
                    image_originale = Image.open(self.parametres['RESIDENCE'])
                elif case.typecase == "Emploi":
                    image_originale = Image.open(self.parametres['EMPLOI'])
                elif case.typecase == "Energie":
                    image_originale = Image.open(self.parametres['ENERGIE'])
                elif case.typecase == "Out":
                    image_originale = Image.open(self.parametres['DETRUIT'])
                else:
                    raise ValueError(f"Type inconnu: {case.typecase}")

                image_redimensionnee = image_originale.resize((taille_case, taille_case))
                image_tk = ImageTk.PhotoImage(image_redimensionnee)
                bouton = tk.Button(self.application, image=image_tk)
                bouton.image = image_tk
                bouton.pack()
                bouton.place(x=x2, y=y2)
                y2 += self.taille_cases + 3
            x2 += self.taille_cases + 3

        self.taille_fenetre = (taille_case+3) * 12
        self.application.maxsize(self.taille_fenetre, self.taille_fenetre)
        self.application.minsize(self.taille_fenetre, self.taille_fenetre)
        self.application.title("MeteoPolis"+" " + self.parametres['version'])
        self.centrer_fenetre()
        self.application.iconbitmap(self.parametres['LOGO'])

        self.Affichage()

        self.application.mainloop()


    def centrer_fenetre(self):
        """Permet de centrer la fenêtre au millieu de l'écran"""
        largeur_ecran = self.application.winfo_screenwidth()
        hauteur_ecran = self.application.winfo_screenheight()
        x = (largeur_ecran - self.taille_fenetre) // 2
        y = (hauteur_ecran - self.taille_fenetre) // 2
        self.application.geometry(f"{self.taille_fenetre}x{self.taille_fenetre}+{x}+{y}")

    def Affichage(self):
        """Affichage de la fenêtre normale"""
        for widget in self.application.winfo_children():
            widget.destroy()

        if not self.simulation:
            lancer = tk.Button(self.application, text='LANCER LA SIMULATION', command = lambda: self.meteopolis.simulation(self))
            lancer.pack(side='top')
            self.application.maxsize(self.taille_fenetre, self.taille_fenetre)
            self.application.minsize(self.taille_fenetre, self.taille_fenetre)
            self.application.title(parametres_immuables()["title"]+" "+parametres_immuables()["version"]+" [Accueil]")
        else:
            self.creer_texte(self.application, (self.taille_cases+3) * 4, 0, f"Saison: {self.meteopolis.saison}", 15)
            self.creer_texte(self.application, (self.taille_cases+3) * 1.5, 0, f"Jour: {str(self.meteopolis.jour)}", 15)
            self.creer_texte(self.application, (self.taille_cases+3) * 8, 0, f"Méteo: {self.meteopolis.temps}", 15)
            self.application.title(parametres_immuables()["title"]+" "+parametres_immuables()["version"]+" [Simulation]")

        x2 = self.taille_cases + 3
        for ligne in self.meteopolis.carte:
            y2 = self.taille_cases + 3
            for case in ligne:
                if case.typecase == "Nature":
                    image_originale = Image.open(self.parametres['NATURE'])
                elif case.typecase == "Residence":
                    image_originale = Image.open(self.parametres['RESIDENCE'])
                elif case.typecase == "Emploi":
                    image_originale = Image.open(self.parametres['EMPLOI'])
                elif case.typecase == "Energie":
                    image_originale = Image.open(self.parametres['ENERGIE'])
                elif case.typecase == "Out":
                    image_originale = Image.open(self.parametres['DETRUIT'])
                else:
                    raise ValueError(f"Type inconnu: {case.typecase}")

                image_redimensionnee = image_originale.resize((taille_case, taille_case))
                image_tk = ImageTk.PhotoImage(image_redimensionnee)
                bouton = tk.Button(self.application, image=image_tk)
                bouton.image = image_tk
                bouton.pack()
                bouton.place(x=x2, y=y2)
                y2 += self.taille_cases + 3
            x2 += self.taille_cases + 3

        if not self.simulation:
            modif = tk.Button(self.application, text='MODIFIER LA CARTE', command = lambda: self.Affichage_modifications())
            modif.pack(side='bottom')

    def Affichage_modifications(self):
        """Affichage de la page après modifications"""
        self.application.maxsize(self.taille_fenetre, self.taille_fenetre + 110)
        self.application.minsize(self.taille_fenetre, self.taille_fenetre + 110)
        self.application.title(parametres_immuables()["title"]+" "+parametres_immuables()["version"]+" [Editeur]")
        for widget in self.application.winfo_children():
            widget.destroy()

        self.creer_texte(self.application, (self.taille_cases+3) * 3.25, 0, 'MODIFICATION DE LA CARTE', 15)

        x2 = self.taille_cases + 3
        for i, ligne in enumerate(self.meteopolis.carte):
            y2 = self.taille_cases + 3
            for j, case in enumerate(ligne):
                if case.typecase == "Nature":
                    image_originale = Image.open(self.parametres['NATURE'])
                elif case.typecase == "Residence":
                    image_originale = Image.open(self.parametres['RESIDENCE'])
                elif case.typecase == "Emploi":
                    image_originale = Image.open(self.parametres['EMPLOI'])
                elif case.typecase == "Energie":
                    image_originale = Image.open(self.parametres['ENERGIE'])
                elif case.typecase == "Out":
                    image_originale = Image.open(self.parametres['DETRUIT'])
                else:
                    raise ValueError(f"Type inconnu: {case.typecase}")

                image_redimensionnee = image_originale.resize((self.taille_cases, self.taille_cases))
                image_tk = ImageTk.PhotoImage(image_redimensionnee)
                bouton = tk.Button(self.application, image=image_tk, command=lambda i=i, j=j: self.changer_nature_case((i, j)))
                bouton.image = image_tk
                bouton.pack()
                bouton.place(x=x2, y=y2)
                y2 += self.taille_cases + 3
            x2 += self.taille_cases + 3

        # Variable pour stocker la sélection
        self.var = tk.IntVar()

        self.Actions = tk.Frame(self.application)
        self.Sauvegarde = tk.Frame(self.application)

        # Création des radioboutons
        self.radio_choix1 = tk.Radiobutton(self.Actions, text="Nature", variable=self.var, value=1)
        self.radio_choix2 = tk.Radiobutton(self.Actions, text="Résidence", variable=self.var, value=2)
        self.radio_choix3 = tk.Radiobutton(self.Actions, text="Emploi", variable=self.var, value=3)
        self.radio_choix4 = tk.Radiobutton(self.Actions, text="Energie", variable=self.var, value=4)

        self.retour = tk.Button(self.Actions, text = 'RETOUR', command = lambda: self.Affichage())

        self.radio_choix1.pack(side=tk.TOP)
        self.radio_choix2.pack(side=tk.TOP)
        self.radio_choix3.pack(side=tk.TOP)
        self.radio_choix4.pack(side=tk.TOP)

        self.retour.pack(side=tk.TOP)

        self.Charger_Button = tk.Button(self.Sauvegarde, text="Sauvegarder la carte sous le nom de: ", command=lambda:self.save())
        self.Charger_Button.pack(side=tk.LEFT)

        self.Nom_De_Carte = tk.Entry(self.Sauvegarde)
        self.Nom_De_Carte.pack(side=tk.LEFT)

        self.Sauvegarde.pack(side='bottom')

        self.Actions.pack(side='bottom')


    def changer_nature_case(self, coo):
        """Changer le type d'une case"""
        self.type = self.var.get()
        if self.type == 1:
            self.meteopolis.carte[coo[0]][coo[1]].new_type('Nature')
        elif self.type == 2:
            self.meteopolis.carte[coo[0]][coo[1]].new_type('Residence')
        elif self.type == 3:
            self.meteopolis.carte[coo[0]][coo[1]].new_type('Emploi')
        elif self.type == 4:
            self.meteopolis.carte[coo[0]][coo[1]].new_type('Energie')
        self.Affichage_modifications()

    def save(self):
        """Sauvegarde de la carte"""
        self.nom_fichier = self.Nom_De_Carte.get()
        ecriture_fichier(self.meteopolis.carte, self.nom_fichier + '.csv')


    def creer_texte(self, fenetre, x2, y2, texte, taille):
        """Créé un texte (texte) de taille (taille) aux coordonnées (x2, y2) dans la fenêtre fenetre (fenetre)"""
        texte_label = tk.Label(fenetre, text=texte)
        texte_label.place(x=x2, y=y2)
        texte_label.config(font=("Helvetica", taille))

    def Simuler(self):
        """Supprime tous les boutons d'une page"""
        for widget in self.application.winfo_children():
            widget.destroy()

    def Simulation(self):
        """Lance la simulation"""
        self.simulation = True
        self.meteopolis.set_saison(self.saison_de_depart)
        self.nb_saison = 1

        return self.Simuler_une_annee()

    def Simuler_une_annee(self):
        """Lance la simulation complète"""
        if self.meteopolis.get_jour() == 31:
            self.meteopolis.jour = 0
            self.meteopolis.set_saison()
            self.nb_saison += 1

        if self.nb_saison == 5:
            return Graphe.calcul_score(self.meteopolis)

        self.Affichage()
        self.meteopolis.incremente_jour()
        #Graphe.ville_de_demain(self.meteopolis) # Calcul de la ville du lendemain

        return self.application.after(self.meteopolis.get_tempo() * 1000, self.Simuler_une_annee)


ok = Application('Ete', 'Carte.csv')