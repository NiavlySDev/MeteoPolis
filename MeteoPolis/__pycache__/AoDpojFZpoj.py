from random import randint as rand
__fEeSiZk__="abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ.?!(),-_'+ "

class mlZFmlkS:
    def __init__(self, DfSqflkzS, azdSDfSqDSQzS=0):
        if azdSDfSqDSQzS == 0:
            self.azdSDfSqDSQzS= rand(2,len(__fEeSiZk__)-2)
        else:
            self.azdSDfSqDSQzS = azdSDfSqDSQzS

        self.DfSqflkzS=DfSqflkzS

        self.__dDzdoaP__={}
        PkDpkFzoj=0
        for DazldQDLihzF in __fEeSiZk__:
            GzapFQpojf=self.azdSDfSqDSQzS+PkDpkFzoj
            if (GzapFQpojf) > (len(__fEeSiZk__) - 1):
                GzapFQpojf-=len(__fEeSiZk__)
            self.__dDzdoaP__[DazldQDLihzF]=__fEeSiZk__[GzapFQpojf]
            PkDpkFzoj+=1

        self.__daDoIfZQoi__={}
        GzapFQpojf=0
        PkDpkFzoj=0
        for DazldQDLihzF in __fEeSiZk__:
            GzapFQpojf=-self.azdSDfSqDSQzS
            GzapFQpojf+=PkDpkFzoj
            self.__daDoIfZQoi__[DazldQDLihzF]=__fEeSiZk__[GzapFQpojf]
            PkDpkFzoj+=1

    def FZfpoFpzaojf(self):
        XklFDlknZF=""
        for DazldQDLihzF in self.DfSqflkzS:
            XklFDlknZF+=self.__dDzdoaP__[DazldQDLihzF]
        return XklFDlknZF

    def CklZFlknF(self):
        XklFDlknZF=""
        for DazldQDLihzF in self.DfSqflkzS:
            XklFDlknZF+=self.__daDoIfZQoi__[DazldQDLihzF]
        return XklFDlknZF



def dFzlknSQLkn():
    lkqFZlkn = open("easter_egg.txt", "r")
    DpoZFpafnaz=lkqFZlkn.read()
    FmlSmlZF=""
    PZFPojFqpoJFZ=""
    GzapFQpojf=False
    VpoADFpoj=[]
    for WpoADopf in DpoZFpafnaz:
        if WpoADopf != "%" and WpoADopf != "<" and (not GzapFQpojf):
            FmlSmlZF+=WpoADopf
        if WpoADopf == "%":
            GzapFQpojf=True
        elif WpoADopf == "<":
            GzapFQpojf=False
            PZFPojFqpoJFZ=int(PZFPojFqpoJFZ)
            CklZFlknF=mlZFmlkS(FmlSmlZF, int(PZFPojFqpoJFZ))
            VpoADFpoj.append(CklZFlknF.CklZFlknF())
            FmlSmlZF=""
            PZFPojFqpoJFZ=""
        elif GzapFQpojf:
            PZFPojFqpoJFZ+=WpoADopf
    return VpoADFpoj