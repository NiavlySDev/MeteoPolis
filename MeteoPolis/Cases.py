import random
liste_types = ["Nature","Residence","Emploi","Energie"]

class Case:
    def __init__(self, vie=50, typecase = "Out"):
        self.vie = vie
        self.typecase = typecase
        self.magnifique = False

    def __str__(self):
        return f"({self.vie}, {self.typecase})"

    def get_vie(self):
        """Récupérer la vie d'une case"""
        return self.vie

    def get_type(self):
        """Récupérer le type de la case"""
        return self.typecase

    def get_magnifique(self):
        """Récupérer le niveau de magnifitude de la case"""
        return self.magnifique == True

    def modif_vie(self, modificateur):
        """Modifie (ajout ou retrait) la vie d'une case"""
        nouvelle_vie = self.vie + modificateur
        if nouvelle_vie > 100 and self.magnifique == False:
            self.set_vie(100)
        elif nouvelle_vie > 200 and self.magnifique == True:
            self.set_vie(200)
        elif nouvelle_vie < 0:
            self.set_vie(0)
        else:
            self.set_vie(nouvelle_vie)

    def new_type(self, new_type):
        """Changer le type d'une case"""
        self.typecase = new_type

    def set_vie(self, new_vie):
        """Changer la vie d'une case"""
        self.vie = new_vie

    def set_magnifique(self, new_magn=bool):
        """Mettre la case en magnifique ou en normal"""
        self.magnifique = new_magn

    def verif_case(self):
        """Mise a jour de la case"""
        if self.vie <= 0:
            self.set_vie(0)
            self.new_type("Out")
            self.set_magnifique(False)

        elif self.typecase == "Out" and self.vie == 100:

            indice_type = random.randint(0,3)
            self.new_type(liste_types[indice_type])
            self.set_vie(50)

        elif self.vie == 100 and self.magnifique == False:
            self.set_magnifique(True)

        elif self.magnifique == True and self.vie < 100:
            self.set_magnifique(False)