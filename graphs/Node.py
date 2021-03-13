######################################################
# Diego Sevilla
# 17238
######################################################
# Node.py
######################################################
# Clase que representa a un nodo
######################################################

class Node:
    '''
    Clase para representar a un nodo.

    Atributos:
     - value = el valor del nodo
     - relations = arreglo de relaciones Ej. ['A,a,B','A,b,C','A,ε,D'] en el caso donde value = 'A'
     - isInitial = es inicial
     - isAccepting = es final o de aceptacion

    '''
    def __init__(self,value,relations=[],isInitial=False,isAccepting=False):
        self.value = value
        self.relations = relations
        self.isInitial = isInitial
        self.isAccepting = isAccepting

    #gets
    def getValue(self):
        return self.value

    def getRelations(self):
        return self.relations

    def getIsInitial(self):
        return self.isInitial

    def getIsAccepting(self):
        return self.isAccepting

    #sets
    def setValue(self,value):
        self.value = value

    def setRelation(self,relation):
        self.relations.append(relation)

    def setIsInitial(self,state):
        self.isInitial = state

    def setIsAccepting(self,state):
        self.isAccepting = state


    #others
    def resetRelations(self):
        self.relations = []

