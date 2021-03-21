######################################################
# Diego Sevilla
# 17238
######################################################
# RelationT.py
######################################################
# Clase que representa una relacion entre 2 nodos
######################################################

class RelationT:
    '''
    Clase para representar a un nodo.

    Atributos:
     - origin = the origin node type(str)
     - token = the token type(str)
     - destiny = the destiny node type(str)
    ''' 
    def __init__(self,origin,token,destiny):
        self.origin = origin
        self.token = token
        self.destiny = destiny

    #gets
    def getOrigin(self):
        return self.origin

    def getToken(self):
        return self.token

    def getDestiny(self):
        return self.destiny

    #sets
    def setOrigin(self,origin):
        self.origin = origin

    def setToken(self,token):
        self.token = token

    def setDestiny(self,destiny):
        self.destiny = destiny
