######################################################
# Diego Sevilla
# 17238
######################################################
# NodeD.py
######################################################

class NodeT:
    """
    Clase para representar a un nodo en el calculo del anulable, primerapos y ultimapos

    Atributos:
     - anulable: True o False
     - primerapos: arreglo con estados
     - ultimapos: arreglo con estados
    """
    def __init__(self,anulable,primerapos,ultimapos):
        self.anulable = anulable
        self.primerapos = primerapos
        self.ultimapos = ultimapos

    #gets_________________
    def getUltimaPos(self):
        u_pos = []
        for i in self.ultimapos:
            u_pos.append(i)
        return u_pos

    def getPrimeraPos(self):
        p_pos = []
        for i in self.ultimapos:
            p_pos.append(i)
        return p_pos

    def getAnulable(self):
        anulable = self.anulable
        return anulable
