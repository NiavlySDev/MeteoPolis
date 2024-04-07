import random
liste_types = ["Nature","Residence","Emploi","Energie"]

class Case:
    def __init__(self,vie=50,typecase = "Out"):
        self.vie = vie
        self.typecase = typecase
        self.magnifique = False

    def __str__(self):
        return f"({self.vie}, {self.typecase})"

    def get_vie(self):
        return self.vie

    def get_type(self):
        return self.typecase

    def get_magnifique(self):
        return self.magnifique == True

    def modif_vie(self, modificateur):
        nouvelle_vie = self.vie + modificateur
        if nouvelle_vie > 100 and self.magnifique == False:
            self.vie = 100
        elif nouvelle_vie > 200 and self.magnifique == True:
            self.vie = 200
        elif nouvelle_vie < 0:
            self.vie = 0
        else:
            self.vie = nouvelle_vie

    def new_type(self, new_type):
        self.typecase = new_type

    def set_vie(self, new_vie):
        self.vie = new_vie

    def set_magnifique(self, new_magn=bool):
        self.magnifique = new_magn

    def verif_case(self):
        if self.vie <= 0:
            self.vie = 0
            self.typecase = "Out"
            self.magnifique = False
        elif self.typecase == "Out" and self.vie == 100:
            indice_type = random.randint(0,3)
            self.typecase = liste_types[indice_type]
        elif self.vie == 100 and self.magnifique == False:
            self.magnifique == True
        elif self.magnifique == True and vie < 100:
            self.magnifique = False






