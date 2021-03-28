######################################################
# Diego Sevilla
# 17238
######################################################
# Direct.py
######################################################

# imports _________________________
import time
import collections
import sys
sys.path.append(".")
from functions import *
from graphs.NodeD import *
from graphviz import Digraph

class DirectAFD:
    """Clase que comvierte una expresion regular en formato postfix a un automara finito determinista AFD.
    """

    def __init__(self, tokens, chain, postfix_regex):
        self.chain = chain
        self.alphabet = tokens
        self.postfix_regex = postfix_regex

        self.firstLastPos = {}
        self.nextPos = {}

        self.AFNArray = []
        self.AFNResult = {}

        # para todos los nodos en general
        self.globalCounter = 0
        # para los nodos sin hijos
        self.globalCounterStates = 0

    def posfixParse(self):
        """
        Funcion para recorrer la cadena postfix e interpretar
        cada uno de los tokens y operandos
        """

        expresion_hash = self.postfix_regex + ['#','.']
        for token in expresion_hash:
            # Se aumenta el contador de estados cada vez que se encuentra un caracter del alfabeto.
            # Este nos servira para los valores de los nodos sin hijos
            if(token in "".join(self.alphabet) or token == "#"):
                self.globalCounterStates += 1
            #sabemos que estos primeros 2 caracteres en la expresion postfix pertenceran al alfabeto
            if(len(self.firstLastPos) < 2):
                counter = self.globalCounterStates
                self.createChildlessNode(token,counter)
            #inmediatamente despues vendra uno o varios operadores y posteriormente mas tokens
            else:
                if(token == '*'):
                    counter = self.globalCounter
                    #nodos hijos del nodo que se creara
                    c1 = self.firstLastPos[counter]

                    # calculamos anulable segun la tabla magica
                    annullable = True
                    # calculamos firstpos segun la tabla magica
                    firstpos = c1.getFirstPos()
                    # calculamos firstpos segun la tabla magica
                    lastpos = c1.getLastPos()

                    node = NodeD(annullable,firstpos,lastpos,token)
                    #ingresamos el nodo creado al diccionario global
                    self.firstLastPos[counter+1] = node
                    self.globalCounter += 1
                else:
                    counter = self.globalCounter
                    #nodos hijos del nodo que se creara
                    #if(self.firstLastPos[counter].getToken() == '*'):
                    #    c1 = self.firstLastPos[counter]
                    #    c2 = self.firstLastPos[counter-1]
                    #else:
                    c2 = self.firstLastPos[counter]
                    c1 = self.firstLastPos[counter-1]

                    # si los dos son . o | entonces el nodo que se creara no tendra hijos
                    if(c1.getToken() in ".|*" and c2.getToken() in ".|*"):
                        counter = self.globalCounterStates
                        self.createChildlessNode(token,counter)
                    elif(c1.getToken() in ".|*" or c2.getToken() in ".|*"):
                        if(token in "".join(self.alphabet) or token == "#"):
                            counter = self.globalCounterStates
                            self.createChildlessNode(token,counter)
                        else:
                            self.createNodeWithChildren(token,c1,c2,counter)
                    else:
                        self.createNodeWithChildren(token,c1,c2,counter)

        print(self.firstLastPos)

    def createNodeWithChildren(self,token,c1,c2,counter):
        """Funcion que crea un nodo con hijos

        - Args:
            - token (str): el token en cuestion
            - c1 (NodeD): el nodo izquierdo
            - c2 (NodeD): el nodo derecho
            - counter (int): el contador global
        """
        annullable, firstpos, lastpos = self.checksForAnnullableFirstposAndLastpos(token,c1,c2,counter)

        node = NodeD(annullable,firstpos,lastpos,token)
        #ingresamos el nodo creado al diccionario global
        self.firstLastPos[counter+1] = node
        self.globalCounter += 1

    def createChildlessNode(self,token,counter):
        """Funcion para crear un nodo sin hijos

        - Args:
            - token (str): el token en cuestion
            - counter (int): el contador global de estados especifico para los tokens del alfabeto
        """
        annullable = False
        firstpos = [counter]
        lastpos = [counter]
        node = NodeD(annullable,firstpos,lastpos,token)
        self.firstLastPos[self.globalCounter+1] = node
        self.globalCounter += 1

    def checksForAnnullableFirstposAndLastpos(self, token, c1, c2,counter):
        """Tabla magica para los valores posibles de Annullable, firstpos y lastpos

        - Args:
            - token (str): el token en cuestion
            - c1 (NodeD): el nodo izquierdo en cuestion
            - c2 (NodeD): el nodo derecho en cuestion
            - counter (int): contador que sirve para saber el estado de los nodos
        - Returns:
            - arr: un arreglo con los valores para annullable, firstpos y lastpos
        """
        if(token in "".join(self.alphabet) or token == "#"):
            #return token
            return False, [counter+1], [counter+1]
        elif(not(token in "".join(self.alphabet))):
            if(token == 'ε'):
                return True,[],[]
            elif(token == '|'):
                pos_s = c1.getFirstPos() + c2.getFirstPos()
                if(c1.getAnnullable() == False and c2.getAnnullable() == False):
                    return False, pos_s, pos_s
                elif(c1.getAnnullable() == False and c2.getAnnullable() == True):
                    return True, pos_s, pos_s
                elif(c1.getAnnullable() == True and c2.getAnnullable() == False):
                    return True, pos_s, pos_s
                else: #(c1.getAnnullable() == True and c2.getAnnullable() == True):
                    return True, pos_s, pos_s
            elif(token == '.'):
                firstpos = None
                lastpos = None
                if(c1.getAnnullable()):
                    firstpos = c1.getFirstPos() + c2.getFirstPos()
                elif(c1.getAnnullable() == False):
                    firstpos = c1.getFirstPos()

                if(c2.getAnnullable()):
                    lastpos = c1.getFirstPos() + c2.getFirstPos()
                elif(c2.getAnnullable() == False):
                    lastpos = c2.getFirstPos()

                if(c1.getAnnullable() == False and c2.getAnnullable() == False):
                    return False, firstpos, lastpos
                elif(c1.getAnnullable() == False and c2.getAnnullable() == True):
                    return False, firstpos, lastpos
                elif(c1.getAnnullable() == True and c2.getAnnullable() == False):
                    return False, firstpos, lastpos
                else: #if(c1.getAnnullable() == True and c2.getAnnullable() == True):
                    return True, firstpos, lastpos

            '''else: #(token == '*'):
                return c1.getFirstPos()'''

    def buildNextPos(self):
        """Funcion para la construccion de nextpos a partir del arbol con los annullable, firstpos y lastpos
        """
        tree = self.firstLastPos
        localStateCounter = 0
        for id, node in tree.items():
            if(node.getToken() == '.'):
                c1 = tree[id-2]
                for state in c1.getLastPos():
                    c2 = tree[id-1]

                    #self.nextPos[node.getLastPos()] = c1.getFirstPos() + c2.getLastPos()
                    if(state in self.nextPos):
                        self.nextPos[state] = self.nextPos[state] + c2.getFirstPos()
                    else:
                        self.nextPos[state] = c2.getFirstPos()

            elif(node.getToken() == '*'):
                for state in node.getLastPos():
                    if(state in self.nextPos):
                        self.nextPos[state] = self.nextPos[state] + node.getLastPos()
                    else:
                        self.nextPos[state] = node.getLastPos()
                        localStateCounter += 1

        self.nextPos[len(self.nextPos)+1] = []

        tokensInPostfix = []
        for token in self.postfix_regex:
            if(token in "".join(self.alphabet)):
                tokensInPostfix.append(token)

        counter = 1
        for token in tokensInPostfix:
            self.nextPos[counter] = [token,self.nextPos[counter]]
            counter += 1
        self.nextPos[counter] = ['#',self.nextPos[counter]]
        print(self.nextPos)

        self.globalCounter = 0

    def nextPosToAFD(self):
        


        return  0

    def generateDirectAFD(self):
        """Funcion centralizadora de las funciones necesarias para la generacion de un AFD a partir de una
        expresion regular.
        """
        self.posfixParse()
        self.buildNextPos()
        self.nextPosToAFD()

