#----- I -----#

'''
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
'''

#----- # -----#

#----- II -----#

'''
def centrer_fenetre(fenetre, largeur, hauteur):
    """Permet de centrer la fenêtre au millieu de l'écran"""
    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()
    x = (largeur_ecran - largeur) // 2
    y = (hauteur_ecran - hauteur) // 2
    fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")

def creer_boutons(fenetre, carte, taille_cases):
    """Crée tous les boutons des interfaces"""
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
                raise ValueError(f"Type inconnu: {case.typecase}")

            image_redimensionnee = image_originale.resize((taille_case, taille_case))
            image_tk = ImageTk.PhotoImage(image_redimensionnee)
            bouton = tk.Button(fenetre, image=image_tk)
            bouton.image = image_tk
            bouton.pack()
            bouton.place(x=x2, y=y2)
            y2 += taille_cases + 3
        x2 += taille_cases + 3

def creer_texte(fenetre, x2, y2, texte, taille):
    """Créé un texte (texte) de taille (taille) aux coordonnées (x2, y2) dans la fenêtre fenetre (fenetre)"""
    texte_label = tk.Label(fenetre, text=texte)
    texte_label.place(x=x2, y=y2)
    texte_label.config(font=("Helvetica", taille))
'''
#----- ## -----#