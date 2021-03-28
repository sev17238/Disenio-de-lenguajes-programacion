######################################################
# Diego Sevilla
# 17238
######################################################
# NodeD.py
######################################################

class NodeD:
    """
    Clase para representar a un nodo en el calculo del annullable, firstpos y lastpos

    Atributos:
     - annullable: True o False
     - firstpos: arreglo con estados
     - lastpos: arreglo con estados
    """
    def __init__(self,annullable,firstpos,lastpos,token):
        self.annullable = annullable
        self.firstpos = firstpos
        self.lastpos = lastpos
        self.token = token

    #gets_________________
    def getLastPos(self):
        u_pos = []
        for i in self.lastpos:
            u_pos.append(i)
        return u_pos

    def getFirstPos(self):
        p_pos = []
        for i in self.firstpos:
            p_pos.append(i)
        return p_pos

    def getAnnullable(self):
        annullable = self.annullable
        return annullable

    def getToken(self):
        token = self.token
        return token

    #sets_________________
    def setFirstPos(self,firstpos):
        self.firstpos = firstpos

    def setLastPos(self,lastpos):
        self.lastpos = lastpos
