import tkinter as tk
from PIL import Image, ImageTk
from Cases import Case

NATURE="ressources/map/terrain_vague.png"
RESIDENCE="ressources/map/residence.png"
EMPLOI="ressources/map/energie.png"
ENERGIE="ressources/map/emploie.png"
DETRUIT="ressources/map/detruit.png"

rgb_nature = (0, 255, 0)
rgb_residence = (0, 0, 255)
rgb_emploi = (255, 165, 0)
rgb_energie = (255, 255, 0)
rgb_detruit = (255, 0, 0)

taille_case=53
taille_carte = 10

def centrer_fenetre(fenetre, largeur, hauteur):
    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()
    x = (largeur_ecran - largeur) // 2
    y = (hauteur_ecran - hauteur) // 2
    fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")


#types -> ["Nature","Residence","Emploi","Energie","Detruit"]
# In api.py

def creer_boutons(fenetre, carte, taille_cases):
    x2 = taille_cases + 3
    for ligne in carte:
        y2 = taille_cases + 3
        for case in ligne:
            if case.typecase == "Nature":
                image_originale = Image.open(NATURE)
            elif case.typecase == "Residence":
                image_originale = Image.open(RESIDENCE)
            elif case.typecase == "Emploi":
                image_originale = Image.open(EMPLOI)
            elif case.typecase == "Energie":
                image_originale = Image.open(ENERGIE)
            elif case.typecase == "Out":
                image_originale = Image.open(DETRUIT)
            else:
                raise ValueError(f"Unknown case type: {case.typecase}")

            image_redimensionnee = image_originale.resize((50, 50))
            image_tk = ImageTk.PhotoImage(image_redimensionnee)
            bouton = tk.Button(fenetre, image=image_tk)
            bouton.image = image_tk
            bouton.pack()
            bouton.place(x=x2, y=y2)
            y2 += taille_cases + 3
        x2 += taille_cases + 3


def creer_texte(fenetre, x2, y2, texte):
    texte_label = tk.Label(fenetre, text=texte)
    texte_label.place(x=x2, y=y2)
    texte_label.config(font=("Helvetica", 15))

def exporter_carte(self, carte):
    """
    1 - Vert: Nature
    2 - Bleu: Résidence
    3 - Orange: Emploi
    4 - Jaune: Energie
    5 - Rouge: Détruit
    """

    image = Image.new("RGB", (10, 10), color="white")

    x=0
    for ligne in carte:
        y=0
        for case in ligne:
            if case.typecase == "Nature": # 1 - Vert: Nature
                image.putpixel((x, y), (0, 255, 0))
            if case.typecase == "Residence": # 2 - Bleu: Ville
                image.putpixel((x, y), (0, 0, 255))
            if case.typecase == "Emploi": # 3 - Orange: Emploi
                image.putpixel((x, y), (255, 165, 0))
            if case.typecase == "Energie": # 4 - Jaune: Energie
                image.putpixel((x, y), (255, 255, 0))
            if case.typecase == "Out": # 5 - Rouge: Détruit
                image.putpixel((x, y), (255, 0, 0))
            y+=1
        x+=1

    image.save("carte.png")

#types -> ["Nature","Residence","Emploi","Energie","Detruit"]
def importer_carte(path):
    image = Image.open(path)
    hauteur, largeur = image.size
    carte = [[None for _ in range(hauteur)] for _ in range(largeur)]
    for x in range(hauteur):
        for y in range(largeur):
            pixel = image.getpixel((x, y))
            if pixel == rgb_nature:
                carte[x][y] = Case(100, "Nature")
            elif pixel == rgb_residence:
                carte[x][y] = Case(100, "Residence")
            elif pixel == rgb_emploi:
                carte[x][y] = Case(100, "Emploi")
            elif pixel == rgb_energie:
                carte[x][y] = Case(100, "Energie")
            elif pixel == rgb_detruit:
                carte[x][y] = Case(100, "Out")
            else:
                raise ValueError(f"Unknown pixel color at position ({x}, {y})")
    return carte