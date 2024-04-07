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
        self.vie += modificateur

    def new_type(self, new_type):
        self.typecase = new_type

    def set_vie(self, new_vie):
        self.vie = new_vie

    def set_magnifique(self, new_magn=bool):
        self.magnifique = new_magn

    def verif_case(self): #à faire quand on aura de quoi la faire
        oui = 15





