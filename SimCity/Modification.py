import tkinter as tk
from PIL import Image, ImageTk
import api
from Cases import Case

class Modification:
    def __init__(self):
        self.title = "SimCity [Modification]"
        self.version = 1.1
        self.taille_carte = 10
        self.fenetre = tk.Tk()
        self.taille_case=50
        self.taille_fenetre = (self.taille_case+3) * 12
        self.fenetre.maxsize((self.taille_case+3) * 12, ((self.taille_case+3) * 12)+100)
        self.fenetre.minsize((self.taille_case+3) * 12, ((self.taille_case+3) * 12)+100)

        self.carte = []

        self.fenetre.title(self.title+" v"+str(self.version))
        api.centrer_fenetre(self.fenetre, self.taille_fenetre, self.taille_fenetre)
        self.fenetre.iconbitmap("ressources/fenetre/icone.ico")
        api.creer_texte(self.fenetre, (api.taille_case+3) * 3.7, 5, f"Modification de la Carte")
        api.creer_texte(self.fenetre, (api.taille_case+3)*1.8, ((api.taille_case+3)*10)+25, f'Pour appliquer les changements, cliquez:')
        modif = tk.Button(self.fenetre, text="Fermer", command=self.sauvegarder)
        modif.place(x=((api.taille_case+3)*8)+17, y=((api.taille_case+3)*10)+28)

        self.coschangees=[]

    def sauvegarder(self):
        image = Image.open("carte.png")
        for change in self.coschangees:
            image.putpixel(change["cos"], change["type"])
        image.save("carte.png")
        self.fenetre.destroy()

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
            self.coschangees[len(self.coschangees)-1]["type"]=(0,255,0)
        if image==api.EMPLOI:
            self.coschangees[len(self.coschangees)-1]["type"]=(255, 165, 0)
        if image==api.RESIDENCE:
            self.coschangees[len(self.coschangees)-1]["type"]=(0,0,255)
        if image==api.ENERGIE:
            self.coschangees[len(self.coschangees)-1]["type"]=(255,255,0)
        if image==api.DETRUIT:
            self.coschangees[len(self.coschangees)-1]["type"]=(255,0,0)

        modif = tk.Button(self.fenetre, image=image_tk)
        modif.image=image_tk
        modif.place(x=x2, y=y2)

        self.supprimer_bouton(int((api.taille_case+3)*3.3),((api.taille_case+3)*11))
        self.supprimer_bouton(int((api.taille_case+3)*4.3),((api.taille_case+3)*11))
        self.supprimer_bouton(int((api.taille_case+3)*5.3),((api.taille_case+3)*11))
        self.supprimer_bouton(int((api.taille_case+3)*6.3),((api.taille_case+3)*11))
        self.supprimer_bouton(int((api.taille_case+3)*7.3),((api.taille_case+3)*11))

    def creer_boutons(self, fenetre, carte, taille_cases):
        x2=taille_cases+3
        for ligne in carte:
            y2=taille_cases+3
            for case in ligne:
                if case.typecase==1:
                    image_originale = Image.open(api.NATURE)
                if case.typecase==2:
                    image_originale = Image.open(api.RESIDENCE)
                if case.typecase==3:
                    image_originale = Image.open(api.EMPLOI)
                if case.typecase==4:
                    image_originale = Image.open(api.ENERGIE)
                if case.typecase==5:
                    image_originale = Image.open(api.DETRUIT)
                image_redimensionnee = image_originale.resize((50, 50))
                image_tk = ImageTk.PhotoImage(image_redimensionnee)
                bouton=tk.Button(fenetre, image=image_tk)
                bouton.bind("<Button-1>", lambda event, b=bouton: self.modif(event, b))
                bouton.image=image_tk
                bouton.pack()
                bouton.place(x=x2,y=y2)
                y2+=taille_cases+3
            x2+=taille_cases+3