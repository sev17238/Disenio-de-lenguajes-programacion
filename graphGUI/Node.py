######################################################
# Diego Sevilla
# 17238
######################################################
# Node.py
######################################################
# Python3 programa que repreenta 
# 1. RegEx: Expresion regular postfix.
######################################################

class Node:
    def __init__(self, inicial,aceptacion, relaciones):
        self.inicial = inicial
        self.aceptacion = aceptacion
        self.relaciones = relaciones

    def getInicial(self):
        return self.inicial

    def getAceptacion(self):
        return self.aceptacion

    def getRelaciones():
        return self.relaciones

    def setInicial(self,state):
        self.inicial = state
        return self.inicial

    def setAceptacion(self,state):
        self.aceptacion = state
        return self.aceptacion

    def getRelaciones(self):
        return self.relaciones

    def setRelacion(self):
        relacion

