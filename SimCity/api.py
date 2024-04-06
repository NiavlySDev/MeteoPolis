import tkinter as tk
from PIL import Image, ImageTk

def centrer_fenetre(fenetre, largeur, hauteur):
    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()
    x = (largeur_ecran - largeur) // 2
    y = (hauteur_ecran - hauteur) // 2
    fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")

def creer_boutons(fenetre, carte):
    x2=53
    for ligne in carte:
        y2=53
        for case in ligne:
            if case==1:
                image_originale = Image.open("ressources/map/nature.png")
            if case==2:
                image_originale = Image.open("ressources/map/ville.png")
            if case==3:
                image_originale = Image.open("ressources/map/emploie.png")
            if case==4:
                image_originale = Image.open("ressources/map/energie.png")
            if case==5:
                image_originale = Image.open("ressources/map/detruit.png")
            image_redimensionnee = image_originale.resize((50, 50))
            image_tk = ImageTk.PhotoImage(image_redimensionnee)
            bouton=tk.Button(fenetre, image=image_tk)
            bouton.image = image_tk
            bouton.pack()
            bouton.place(x=x2,y=y2)
            y2+=53
        x2+=53

def creer_texte(fenetre, x2, y2, texte):
    texte_label = tk.Label(fenetre, text=texte)
    texte_label.place(x=x2, y=y2)
    texte_label.config(font=("Helvetica", 15))