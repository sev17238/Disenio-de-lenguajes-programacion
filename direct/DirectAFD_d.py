######################################################
# Diego Sevilla
# 17238
######################################################
# Direct_d.py
######################################################
# Archivo deprecated con fallas de implementacion
######################################################

# imports _________________________
import time
import collections
import sys
sys.path.append(".")
from functions import *
from graphs.NodeD_d import *
from graphs.Relation import *
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

        self.AFDArray = []
        self.AFDResult = {}

        # para todos los nodos en general
        self.globalCounter = 0
        # para los nodos sin hijos
        self.globalCounterStates = 0

    def posfixParse(self):
        """
        Funcion para recorrer la cadena postfix e interpretar
        cada uno de los tokens y operandos
        """
        kleenesCounter = 0
        continiousOpsCounter = 0
        expresion_hash = self.postfix_regex + ['#','.']
        for token in expresion_hash:
            # Se aumenta el contador de estados cada vez que se encuentra un caracter del alfabeto.
            # Este nos servira para los valores de los nodos sin hijos
            if(token in "".join(self.alphabet) or token == "#"):
                self.globalCounterStates += 1
                continiousOpsCounter = 0
            else:
                continiousOpsCounter += 1
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
                    if(c1.getToken() in ".|*" and c2.getToken() in ".|*" and continiousOpsCounter <= 2):
                        counter = self.globalCounterStates
                        self.createChildlessNode(token,counter)
                    elif(c1.getToken() in ".|*" and c2.getToken() in ".|*" and continiousOpsCounter > 2):
                        c22 = self.firstLastPos[counter]
                        c11 = self.firstLastPos[counter-continiousOpsCounter-1]
                        self.createNodeWithChildren(token,c11,c22,counter)
                        continiousOpsCounter = 0
                    elif(c1.getToken() in ".|*" or c2.getToken() in ".|*"):
                        if(token in "".join(self.alphabet) or token == "#"):
                            counter = self.globalCounterStates
                            self.createChildlessNode(token,counter)
                        else:
                            self.createNodeWithChildren(token,c1,c2,counter)
                    else:
                        self.createNodeWithChildren(token,c1,c2,counter)

        #print(self.firstLastPos)

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
                        statesInNextPos = self.nextPos[state] + c2.getFirstPos()
                         # Eliminacion de duplicados
                        statesInNextPos = list(dict.fromkeys(statesInNextPos))
                        # Los estados se ordenan de forma ascendente
                        statesInNextPos.sort()

                        self.nextPos[state] = statesInNextPos

                    else:
                        self.nextPos[state] = c2.getFirstPos()

            elif(node.getToken() == '*'):
                for state in node.getLastPos():
                    if(state in self.nextPos):
                        statesInNextPos = self.nextPos[state] + node.getFirstPos()
                         # Eliminacion de duplicados
                        statesInNextPos = list(dict.fromkeys(statesInNextPos))
                        # Los estados se ordenan de forma ascendente
                        statesInNextPos.sort()
                        self.nextPos[state] = statesInNextPos
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
        #print(self.nextPos)


    def nextPosToAFD(self):
        #se actualiza el contador global para que el diccionario AFDResult empiece a partir de 1
        self.globalCounter = 0
        counter = self.globalCounter

        #el firstPos de la raiz del arbol sera el estado inicial
        initial_state = self.firstLastPos[len(self.firstLastPos)].getFirstPos()
        init_node = NodeDD(initial_state,isInitial=True)
        self.AFDResult[counter] = init_node
        self.globalCounter += 1

        tempNextPos = []

        self.checkNextPosState(init_node)

        local_counter = 0
        stop = False
        #stop sera verdadero cuando ya no se generen mas estados a partir del nodo en cuestion
        while(stop != True):
            #se obtiene el siguiente nodo
            node = self.AFDResult[local_counter+1]
            #se chequea diccionario en nextPost. Pueden agregarse nodos o no
            stop = self.checkNextPosState(node)

            local_counter += 1

        #print(self.AFDResult)


    def checkNextPosState(self,current_node):
        tempEqualStates = {}
        #iteramos en los estados del nodo en cuestion y almacenamos los valores de nextPos que apliquen
        for state in current_node.getStates():
            for node_num, token_nextpos in self.nextPos.items():
                if(node_num == state):
                    tempEqualStates[node_num] = token_nextpos

        wasAtLeastANodeAdded = 0
        #ahora iteramos en los esatodos de nextPos que aplican y buscar si hay tokens repetidos
        for token in self.alphabet:
            tempEqualTokens = {}
            for node_state, token_nextpos in tempEqualStates.items():
                if(token_nextpos[0] == token):
                    tempEqualTokens[node_state] = token_nextpos

            newPosibleStateset = []
            # suma de nextPoses 
            for node_state, token_nextpos in tempEqualTokens.items():
                newPosibleStateset = newPosibleStateset + token_nextpos[1]
            # Eliminacion de duplicados
            newPosibleStateset = list(dict.fromkeys(newPosibleStateset))
            # Los estados se ordenan de forma ascendente
            newPosibleStateset.sort()
            
            counter = self.globalCounter
            #si el set de estados no existe entonces se agrega el nuevo nodo
            if(not(self.checkStatesetExistenceInAFD(newPosibleStateset))):
                #se crea el nuevo nodo
                if(len(self.nextPos) in newPosibleStateset):
                    newNode = NodeDD(newPosibleStateset,isAccepting=True)
                else:
                    newNode = NodeDD(newPosibleStateset)
                #se crea relacion del nodo anterior al nodo que se esta creando
                #rel = Relation(counter,token,newNode.getStates())
                rel = Relation(counter-1,token,counter)
                prevNode = self.AFDResult[counter-1]
                prevNode.addRelation(rel)

                self.AFDResult[counter] = newNode
                self.globalCounter += 1
                wasAtLeastANodeAdded += 1
            else:
                if(current_node.getStates() == newPosibleStateset):
                    for id, node_l in self.AFDResult.items():
                        if(node_l.getStates() == newPosibleStateset):
                            rel = Relation(id,token,id)
                            #rel = Relation(counter-1,token,counter-1)
                            nodeToAddRelation = self.AFDResult[id]
                            nodeToAddRelation.addRelation(rel)
                            #current_node.addRelation(rel)
                            break
                else:
                    for id, node_l in self.AFDResult.items():
                        if(node_l.getStates() == newPosibleStateset):
                            rel = Relation(counter-1,token,id)
                            #nodeToAddRelation = self.AFDResult[id]
                            current_node.addRelation(rel)
                            break
        
        if(wasAtLeastANodeAdded == 0):
            return True
        else:
            return False


    def checkStatesetExistenceInAFD(self,newPosibleStateset):
        """Funcion para revisar si el set de estados ya existe en el afd que se esta construyendo

        Args:
            newPosibleStateset (list): el set de estados en cuestion

        Returns:
            bool: respuesta de existencia
        """
        for id,node in self.AFDResult.items():
            if(newPosibleStateset == node.getStates()):
                return True
        return False


    def getAFDAcceptingStates(self):
        '''
        Se verifica si el estado de aceptacion del AFN se encuentra en alguno de los
        sets de estados generados y asi saber que estado del AFD es de aceptacion.

        - Ej. acceptingStatesAFN = 10 --> (a|b)*abb
        '''
        #Los Estados de aceptacion el AFN generado por thompson
        afdAcceptingStates = {}
        for id,node in self.AFDResult.items():
            if(node.getIsAccepting()):
                afdAcceptingStates[id] = node
        return afdAcceptingStates


    def move(self,statesSet,transition):
        '''
        Funcion mover() que retorna los estados (del conjunto de estados proporcionado), que pasan 
        por la transicion especificada. Ej. move(A,a) --> (a|b)*abb

        Params:
        - AFD: diccionario que representacion del AFD en question
        - statesSet: Un conjunto de estados de un AFN Ej. A = [0,1,2,4,7]
        - transition: transicion por la que pueden pasar algunos de los estados en A.
        - return - [3,8]
        '''
        resultSetArray = []

        AFDResult = self.AFDResult

        for id, current_node in AFDResult.items():
            if(statesSet[0] == id):
                for rel in current_node.getRelations():
                    if(rel.getToken() == transition):
                        return [rel.getDestiny()]
        return None

        '''for stateFromSet in statesSet:
            for state, current_node in self.resultAFD.items():
                for tran, s_set in current_node.items():
                    if(state == stateFromSet and tran == transition):
                        for id, state_val in resultAFD.items():
                            if(s_set == state_val):
                                resultSetArray.append(id)'''

        return resultSetArray


    def simDirectAFD(self):
        '''
        Funcion para simular un AFD 
        '''

        print('\n Simulando AFD con la cadena a evaluar... ')

        start_time = time.perf_counter()
        F = self.getAFDAcceptingStates()
        s = [0]
        for token in self.chain:
            if(s == None):
                break
            else:
                s = self.move(s,token)

        accepted = False
        for accepting_state in F.keys():
            if(s[0] == accepting_state):
                accepted = True
                break
            else:
                accepted = False

        if(accepted):
            print('-------------------------------------------------')
            print('La cadena '+self.chain+' fue aceptada por el AFD.')
            end_time = time.perf_counter() 
            total_time = end_time-start_time
            print('Tiempo transcurrido: '+str(total_time))
            print('-------------------------------------------------')
        else:
            print('-------------------------------------------------')
            print('La cadena '+self.chain+' NO fue aceptada por el AFD.')
            end_time = time.perf_counter()
            total_time = end_time-start_time
            print('Tiempo transcurrido: '+str(total_time))
            print('-------------------------------------------------')
        return 0


    def getAFDRelations(self):
        '''
        Funcion que retorna las relaciones de un afn
        '''
        rels = []
        for id, node in self.AFDResult.items():
            node_rels = node.getRelations()
            if(len(node_rels) > 0):
                rels.append(node_rels)
        return rels


    def drawDirectAFD(self, filename='direct-afd'):
        print('Dibujando representacion del AFD Directo... \n')
        file_name = 'graphs-direct/'+filename
        dot = Digraph(comment=filename, format='png')
        dot.attr(rankdir='LR', size='8,8')
        dot.attr('node', style='filled',color='plum2') #,color='lightgrey'

        acceptingStates = self.getAFDAcceptingStates()
        dot.attr('node', shape='doublecircle')
        for id,node in acceptingStates.items():
            dot.node(str(id))

        dot.attr('node', shape='circle')
        afdRelations = self.getAFDRelations()

        for rels in afdRelations:
            if(len(rels) > 0):
                if(len(rels) > 1):
                    for rel in rels:
                        dot.edge(str(rel.getOrigin()), str(rel.getDestiny()), label=str(rel.getToken()))
                else:
                    rel = rels.pop()
                    dot.edge(str(rel.getOrigin()), str(rel.getDestiny()), label=str(rel.getToken()))

        dot.attr(label=r'\n'+filename, fontsize='20')
        dot.render(filename=file_name, view=True)
        #dot.view()

    def generateDirectAFD(self):
        """Funcion centralizadora de las funciones necesarias para la generacion de un AFD a partir de una
        expresion regular.
        """
        #se parsea el postfix para calcular anulable, firstpos y lastpos
        self.posfixParse()
        #se construye nextpos a partir de los calculos anteriores
        self.buildNextPos()
        #se construye el afd a partir de nextpos
        self.nextPosToAFD()
        #se simula el afd con la cadena ingresada
        self.simDirectAFD()
        #se dibuja el afd
        self.drawDirectAFD()
        