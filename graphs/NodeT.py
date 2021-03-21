######################################################
# Diego Sevilla
# 17238
######################################################
# Node.py
######################################################
# Clase que representa a un nodo
######################################################

class NodeT:
    '''
    Clase para representar a un nodo tomando en cuenta el algoritmo de 
    thompson.

    Atributos:
     - relations = arreglo de relaciones tipo Relacion()
     - isInitial = es inicial
     - isAccepting = es final o de aceptacion
    '''
    def __init__(self,relations=[],isInitial=False,isAccepting=False):
        self.relations = relations
        self.isInitial = isInitial
        self.isAccepting = isAccepting

    #gets
    def getRelations(self):
        return self.relations

    def getSpecificRelation(self,i):
        if(len(self.relations) == 0):
            return None
        else:
            return self.relations[i]

    def getIsInitial(self):
        return self.isInitial

    def getIsAccepting(self):
        return self.isAccepting

    #sets
    def setRelation(self,relation):
        self.relations.append(relation)

    def setRelations(self,relations):
        self.relations = relations

    def setIsInitial(self,state):
        self.isInitial = state

    def setIsAccepting(self,state):
        self.isAccepting = state


    #others
    def resetRelations(self):
        self.relations = []

    def popRelation(self,i):
        return self.relations.pop(i)

    def modifyRelationDestiny(self,i,new_destiny_node): 
        relation = self.relations[i].setDestiny(new_destiny_node)

    def copyNodeAtributes(self):
        return self.relations,self.isInitial,self.isAccepting

    def pasteNodeAtributes(self,relations,isInitial,isAccepting):
        self.relations = relations
        self.isInitial = isInitial
        self.isAccepting = isAccepting

    def clearStates(self):
        self.isInitial = False
        self.isAccepting = False


