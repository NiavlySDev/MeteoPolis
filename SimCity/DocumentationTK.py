import tkinter as tk
from PIL import Image, ImageTk

# Fonction appelée lors du clic sur le bouton
def clic_sur_bouton():
    print("Vous avez cliqué sur le bouton!")

# Créer une fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Bouton avec image")

# Charger l'image avec PIL
image_originale = Image.open("chemin/vers/votre/image.jpg")  # Mettez le chemin de votre image ici

# Redimensionner l'image à la taille désirée
largeur = 100  # Modifier la largeur souhaitée
hauteur = 100  # Modifier la hauteur souhaitée
image_redimensionnee = image_originale.resize((largeur, hauteur))

# Convertir l'image redimensionnée en un format compatible avec Tkinter
image_tk = ImageTk.PhotoImage(image_redimensionnee)

# Créer un bouton avec l'image redimensionnée
bouton_image = tk.Button(fenetre, image=image_tk, command=clic_sur_bouton)
bouton_image.place(x=50, y=50)  # Modifier les coordonnées x et y selon votre choix

# Créer un widget Label pour afficher le texte
texte_label = tk.Label(fenetre, text="Bonjour, monde!")
texte_label.pack()  # Cette méthode permet d'ajuster automatiquement la taille du widget en fonction du texte

# Changer la taille de la fenêtre (largeur x hauteur)
fenetre.geometry("400x300")  # Changer les dimensions selon vos besoins

# Démarrer la boucle principale de Tkinter
fenetre.mainloop()
