######################################################
# Diego Sevilla
# 17238
######################################################
# Subsets.py
######################################################

# imports _______
from graphviz import Digraph
import time
import collections
from functions import *
from graphs.NodeT import *
from graphs.RelationT import RelationT
import sys
sys.path.append(".")


class Subsets:
    '''
        Clase que comvierte un automara finito no determinista (AFN) a un automata finito
        determinista (AFD) por medio del algoritmo de subconjuntos.
    '''
    def __init__(self,tokens,chain,AFN):
        self.chain = chain
        self.alphabet = tokens
        self.alphabet.sort()

        self.TAFN = AFN
        self.TAFNArray = []
        self.TAFNStates = {}

        self.statesCounter = 0 

        self.AFDArray = []
        self.resultAFD = {}
        self.AFDStates = []


    def pop(self):
        if (self.pop == -1):
            return
        else:
            self.top -= 1
            return self.stack.pop()

    def push(self, i):
        self.top += 1
        self.stack.append(i)

    def move(self,AFN,statesSet,transition):
        '''
        Funcion mover() que retorna los estados (del conjunto de estados proporcionado), que pasan 
        por la transicion especificada. Ej. move(A,a) --> (a|b)*abb

        Params:
        - AFN: diccionario que representacion del AFN en question
        - statesSet: Un conjunto de estados de un AFN Ej. A = [0,1,2,4,7]
        - transition: transicion por la que pueden pasar algunos de los estados en A.
        - return - [3,8]
        '''
        resultSet = []
        for state in statesSet:
            for node in AFN.values():
                rels = node.getRelations()
                if(len(rels) > 0):
                    for rel in rels:
                        # Si el estado es igual al origen del nodo(relacion) en cuestion y el token es igual que la 
                        # transicion se agregara el destino a resultSet 
                        if(state == rel.getOrigin() and rel.getToken() == transition):
                            # Eliminacion de duplicados
                            resultSet = list(dict.fromkeys(resultSet))
                            # Los estados se ordenan de forma ascendente
                            resultSet.sort()
                            # Este sera el estado al que podemos llegar a travez de la 
                            # transicion especificada.
                            resultSet.append(rel.getDestiny())

        # Eliminacion de duplicados
        resultSet = list(dict.fromkeys(resultSet))
        resultSet.sort()
        return resultSet

    def e_clossure(self,AFN,move):
        '''
        Funcion de cerradura epsilon que retorna todos los estados a los que se 
        puede llegar en el AFN a travez de epsilon o un token cualquiera. 
        Ej. ε_closure(AFN,[3,8]) --> (a|b)*abb

        Params:
        - AFN: diccionario con el AFN en question
        - move: Resultado proporcionado por la funcion mover()
        - return - Dtran(A,a) = ε_closure(move(A,a)) = [1,2,3,4,6,7,8]
        '''
        resultStateSet = []
        resultStateSet += move
        for state in move:
            for node in AFN.values():
                rels = node.getRelations()
                if(len(rels) > 1):
                    for rel in rels:
                        if(state == rel.getOrigin() and rel.getToken() == 'ε'):
                            # Eliminacion de duplicados
                            resultStateSet = list(dict.fromkeys(resultStateSet))
                            # Ordenamiento en orden ascendente
                            resultStateSet.sort()
                            resultStateSet += self.e_clossure(AFN,[rel.getDestiny()])
                elif(len(rels) != 0):
                    if(state == rels[0].getOrigin() and rels[0].getToken() == 'ε'):
                        resultStateSet = list(dict.fromkeys(resultStateSet))
                        resultStateSet.sort()
                        resultStateSet += self.e_clossure(AFN,[rels[0].getDestiny()])

        # Eliminacion de duplicados
        resultStateSet = list(dict.fromkeys(resultStateSet))
        # Ordenamiento en orden ascendentes
        resultStateSet.sort()
        return resultStateSet

    def moveAFD(self,statesSet,transition):
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
        statesToTest = self.getTestingStates()

        for stateFromSet in statesSet:
            for state, dict_ in self.resultAFD.items():
                for tran, s_set in dict_.items():
                    if(state == stateFromSet and tran == transition):
                        for id, state_val in statesToTest.items():
                            if(s_set == state_val):
                                resultSetArray.append(id)

        return resultSetArray

    def simAFD(self):
        '''
        Funcion para simular un AFD 
        '''
        print('\n Simulando AFD con la cadena a evaluar... ')
        F = self.getAFDAcceptingStates()
        s = [0]
        for token in self.chain:
            s = self.moveAFD(s,token)

        if(s == F):
            print('-------------------------------------------------')
            print('La cadena '+self.chain+' fue aceptada por el AFD.')
            print('-------------------------------------------------')
        else:
            print('-------------------------------------------------')
            print('La cadena '+self.chain+' NO fue aceptada por el AFD.')
            print('-------------------------------------------------')
        return 0

    def afn_to_afd_process(self):
        self.build_afd(self.AFDStates)
        self.simAFD()
        self.drawAFD()


    def getAFDAcceptingStates(self):
        '''
        Se verifica si el estado de aceptacion del AFN se encuentra en alguno de los
        sets de estados generados y asi saber que estado del AFD es de aceptacion.

        - Ej. acceptingStatesAFN = 10 --> (a|b)*abb
        '''
        #los estaods de aceptacion del AFD
        acceptingStates = []
        #Los Estados de aceptacion el AFN generado por thompson
        acceptingStatesAFN = getAcceptingStates(self.TAFN)[0]
        for state, values in self.resultAFD.items():
            #si el estado del AFN se encuentra en el set de estados en cuestion
            if(acceptingStatesAFN in values[0]):
                acceptingStates.append(state)
        return acceptingStates

    def getTestingStates(self):
        resultAFD = self.resultAFD
        dict_ = {}
        for key,val in resultAFD.items():
            dict_[key] = val[0]
        #for key,val in resultAFD.items():
        #    dict_[key] = val[0]

        return dict_

    def drawAFD(self, filename='subsets-afd'):
        print('\nDibujando representacion del AFD...\n')
        file_name = 'subsets-graphs/'+filename
        dot = Digraph(comment=filename, format='png')
        dot.attr(rankdir='LR', size='8,8')
        dot.attr('node', style='filled',color='lightpink') #,color='lightgrey'

        acceptingStates = self.getAFDAcceptingStates()
        dot.attr('node', shape='doublecircle')
        for state in acceptingStates:
            dot.node(str(state))
            #dot.node(get_abc_key(state))

        testingStates = self.getTestingStates()

        dot.attr('node', shape='circle')

        for state, values in self.resultAFD.items():
            for s_state, s_value in values.items():
                if(s_state != 0):
                    for id, valueState in testingStates.items():
                        if(s_value == valueState):
                            dot.edge(str(state), str(id), label=s_state)
                            #dot.edge(get_abc_key(state), str(id), label=get_abc_key(state))

        dot.attr(label=r'\n'+filename, fontsize='20')
        dot.render(filename=file_name, view=True)
        #dot.view()


    def build_afd(self,stateSets):
        # si ya hay sets de estados con los que se podamos comparar
        if(len(stateSets) > 0):
            #por cada token del alfabeto se iran construyendo los sets de estados
            for token in self.alphabet:
                counter = 0
                #recorremos cada set de estados
                for stateSet in stateSets:
                    #calculamos move de un set de estados x y el respectivo token
                    move = self.move(self.TAFN,stateSet,token)

                    d_tran = []
                    l_dict = {}
                    l_dict2 = {}
                    d_tran = self.e_clossure(self.TAFN,move)

                    #chequeamos si dtran tiene sets de estados
                    if(len(d_tran) > 0):
                        if(not(d_tran in self.AFDStates)):
                            l_dict[0] = d_tran
                            self.resultAFD[self.statesCounter + 1] = l_dict
                            
                            l_dict2[0] = stateSet
                            l_dict2[token] = d_tran
                            self.resultAFD[counter] = l_dict2
                            self.statesCounter += 1
                            counter += 1
                            self.AFDStates.append(d_tran)
                            self.build_afd(self.AFDStates)
                        else:
                            l_dict[0] = stateSet
                            l_dict[token] = d_tran
                            self.resultAFD[counter].update(l_dict)
                            counter += 1
                    #si dtran no tiene sets de estados entonces
                    else:
                        l_dict[0] = stateSet
                        l_dict[token] = d_tran
                        self.resultAFD[counter].update(l_dict)
                        if(counter < len(self.alphabet)):
                            counter += 1
        # si aun no hay sets de estados entonces
        else:
            l_dict = {}
            #calculamos la cerradura epsilon de 0
            initAFDState = self.e_clossure(self.TAFN,[0])
            #agregamos este estado inicial al arreglo que contendra
            #los sets de estados del AFN
            self.AFDStates.append(initAFDState)
            #Llamamos a build_afd
            self.build_afd(self.AFDStates)

