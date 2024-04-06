import tkinter as tk
from PIL import Image, ImageTk

NATURE="ressources/map/nature.png"
RESIDENCE="ressources/map/residence.png"
EMPLOI="ressources/map/emploie.png"
ENERGIE="ressources/map/energie.png"
DETRUIT="ressources/map/detruit.png"

def centrer_fenetre(fenetre, largeur, hauteur):
    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()
    x = (largeur_ecran - largeur) // 2
    y = (hauteur_ecran - hauteur) // 2
    fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")

def creer_boutons(fenetre, carte, taille_cases):
    x2=taille_cases+3
    for ligne in carte:
        y2=taille_cases+3
        for case in ligne:
            if case==1:
                image_originale = Image.open(NATURE)
            if case==2:
                image_originale = Image.open(RESIDENCE)
            if case==3:
                image_originale = Image.open(EMPLOI)
            if case==4:
                image_originale = Image.open(ENERGIE)
            if case==5:
                image_originale = Image.open(DETRUIT)
            image_redimensionnee = image_originale.resize((taille_cases, taille_cases))
            image_tk = ImageTk.PhotoImage(image_redimensionnee)
            bouton=tk.Button(fenetre, image=image_tk)
            bouton.image = image_tk
            bouton.pack()
            bouton.place(x=x2,y=y2)
            y2+=taille_cases+3
        x2+=taille_cases+3

def creer_texte(fenetre, x2, y2, texte):
    texte_label = tk.Label(fenetre, text=texte)
    texte_label.place(x=x2, y=y2)
    texte_label.config(font=("Helvetica", 15))