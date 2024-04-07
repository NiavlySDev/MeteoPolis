class Case:
    def __init__(self,vie,typecase):
        self.vie = vie
        self.typecase = typecase

    def __str__(self):
        return f"({self.vie}, {self.typecase})"