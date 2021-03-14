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

    def getSpecificRelation(self,i):
        return self.relations[i]

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

    def popRelation(self,i):
        return self.relations.pop(i)

    def modifyDestinyRelation(self,i,new_destinty_node): #'A,a,B'
        relation = self.relations[i]
        relation = relation[0:1]+new_destinty_node
        #temp = list(relation)
        #temp[4] = new_destinty_node
        #relation = "".join(temp)
        print(relation)
        self.relations[i] = relation

    #def modifyOriginRelation(self,i,new_origin_node): #'A,a,B'
    #    relation = self.relations[i]
    #    relation = new_origin_node+relation[1:4]
    #    print(relation)
    #    self.relations[i] = relation

