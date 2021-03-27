######################################################
# Diego Sevilla
# 17238
######################################################
# Direct.py
######################################################

# imports _________________________
import time
import collections
from functions import *
from graphs.NodeD import *
import sys
sys.path.append(".")
from graphviz import Digraph

class DirectAFD:
    '''
    Clase que comvierte una expresion regular en formato postfix a un automara finito determinista AFD.
    '''

    def __init__(self, tokens, chain):
        self.AFNArray = []
        self.AFNResult = {}
        self.chain = chain
        self.alphabet = tokens

    def postFixParser(self, expresion):
        '''
        Funcion para recorrer la cadena postfix e interpretar
        cada uno de los tokens y operandos
        '''
        for i in expresion:
            # si el iterador es un token
            if(i in "".join(self.alphabet)):
                self.token_afn(i)
            # si el iterador apunta a un operador
            elif(i in ".|*"):
                if(i == "."):
                    self.concat_afn()
                elif(i == "|"):
                    self.or_afn()
                elif(i == "*"):
                    self.kleene_afn()

        endAFN = self.AFNArray.pop()
        self.simAFD(endAFN)
        self.drawGraph(endAFN)

        return endAFN


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

        start_time = time.perf_counter()
        F = self.getAFDAcceptingStates()
        s = [0]
        for token in self.chain:
            s = self.moveAFD(s,token)

        if(s == F):
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