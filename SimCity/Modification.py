import tkinter as tk
from PIL import Image, ImageTk
import api
from Cases import Case

class Modification:
    def __init__(self, meteopolis):
        self.meteopolis=meteopolis
        self.carte = meteopolis.carte

        self.meteopolis.fenetre.title(api.title+" [Edition] "+api.version)

        self.coschangees=[]

    def maj(self):
        for widget in self.meteopolis.fenetre.winfo_children():
            widget.destroy()
        api.creer_texte(self.fenetre, (api.taille_case+3) * 3.7, 5, f"Modification de la Carte", 15)
        api.creer_texte(self.fenetre, 125, (((api.taille_case+3)*12)+12), f'Pour appliquer les changements, cliquez:', 15)
        modif = tk.Button(self.fenetre, text="Fermer", command=self.sauvegarder)
        modif.place(x=275, y=((api.taille_case+3)*13))
        api.creer_boutons(self.fenetre, self.meteopolis.carte, api.taille_case)

    def sauvegarder(self):
        for change in self.coschangees:
            self.meteopolis.carte[change["cos"][0]][change["cos"][1]]=Case(50,change["type"])
        for widget in self.fenetre.winfo_children():
            widget.destroy()
        self.meteopolis.maj()

    def affichage(self):
        self.fenetre.mainloop()

    def modif(self, event, bouton):
        x = (bouton.winfo_x()//api.taille_case)-1
        y = (bouton.winfo_y()//api.taille_case)-1
        x2=bouton.winfo_x()
        y2=bouton.winfo_y()
        self.supprimer_bouton(bouton.winfo_x(), bouton.winfo_y())

        self.coschangees.append({"cos":(x,y),"type":None})

        self.create_remplacement(api.NATURE, 3.3, x2, y2)
        self.create_remplacement(api.RESIDENCE, 4.3, x2, y2)
        self.create_remplacement(api.EMPLOI, 5.3, x2, y2)
        self.create_remplacement(api.ENERGIE, 6.3, x2, y2)
        self.create_remplacement(api.DETRUIT, 7.3, x2, y2)

    def create_remplacement(self, image, x, x2, y2):
        image_originale = Image.open(image)
        image_redimensionnee = image_originale.resize((50, 50))
        image_tk = ImageTk.PhotoImage(image_redimensionnee)

        modif = tk.Button(self.fenetre, image=image_tk)
        modif.bind("<Button-1>", lambda event, b=modif: self.remplacement_bouton(event, b, int((api.taille_case+3)*x), int(((api.taille_case+3)*11)), image, x2, y2))
        modif.image=image_tk
        modif.place(x=int((api.taille_case+3)*x), y=int(((api.taille_case+3)*11)))

    def supprimer_bouton(self, x, y):
        for widget in self.fenetre.winfo_children():
            if isinstance(widget, tk.Button) and widget.winfo_x() == x and widget.winfo_y() == y:
                widget.destroy()
                return

    def remplacement_bouton(self, event, b, x, y, image, x2, y2):
        image_originale = Image.open(image)
        image_redimensionnee = image_originale.resize((50, 50))
        image_tk = ImageTk.PhotoImage(image_redimensionnee)

        if image==api.NATURE:
            self.coschangees[len(self.coschangees)-1]["type"]="Nature"
        if image==api.EMPLOI:
            self.coschangees[len(self.coschangees)-1]["type"]="Emploi"
        if image==api.RESIDENCE:
            self.coschangees[len(self.coschangees)-1]["type"]="Residence"
        if image==api.ENERGIE:
            self.coschangees[len(self.coschangees)-1]["type"]="Energie"
        if image==api.DETRUIT:
            self.coschangees[len(self.coschangees)-1]["type"]="Out"

        modif = tk.Button(self.fenetre, image=image_tk)
        modif.image=image_tk
        modif.place(x=x2, y=y2)

        self.supprimer_bouton(int((api.taille_case+3)*3.3),((api.taille_case+3)*11))
        self.supprimer_bouton(int((api.taille_case+3)*4.3),((api.taille_case+3)*11))
        self.supprimer_bouton(int((api.taille_case+3)*5.3),((api.taille_case+3)*11))
        self.supprimer_bouton(int((api.taille_case+3)*6.3),((api.taille_case+3)*11))
        self.supprimer_bouton(int((api.taille_case+3)*7.3),((api.taille_case+3)*11))

    # types -> ["Nature","Residence","Emploi","Energie","Detruit"]
    def creer_boutons(self, fenetre, carte, taille_cases):
        x2=taille_cases+3
        for ligne in carte:
            y2=taille_cases+3
            for case in ligne:
                if case.typecase=="Nature":
                    image_originale = Image.open(api.NATURE)
                if case.typecase=="Residence":
                    image_originale = Image.open(api.RESIDENCE)
                if case.typecase=="Emploi":
                    image_originale = Image.open(api.EMPLOI)
                if case.typecase=="Energie":
                    image_originale = Image.open(api.ENERGIE)
                if case.typecase=="Out":
                    image_originale = Image.open(api.DETRUIT)
                image_redimensionnee = image_originale.resize((api.taille_case, api.taille_case))
                image_tk = ImageTk.PhotoImage(image_redimensionnee)
                bouton=tk.Button(fenetre, image=image_tk)
                bouton.bind("<Button-1>", lambda event, b=bouton: self.modif(event, b))
                bouton.image=image_tk
                bouton.pack()
                bouton.place(x=x2,y=y2)
                y2+=taille_cases+3
            x2+=taille_cases+3