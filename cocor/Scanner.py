######################################################
# Diego Sevilla
# 17238
######################################################
# Cocor.py
######################################################

# imports__________________________

import os
from os.path import basename
import sys
sys.path.append(".")

import time
import pickle
import string
from functions import functions



# Clase de implementacion_________________________________________________

class Scanner:
    """Archivo que utiliza las transiciones del AFD
    para reconocer los tokens en el archivo de prueba.
    """
    def __init__(self,testFile = 'test_file.cfg'):
        self.scanner = pickle.load(open('cocor/scanner','rb'))
        #self.acceptingStatesDict = pickle.load(open('cocor/accADict','rb'))
        self.resultAFDArray = self.scanner.resultAFDArray
        self.acceptingStatesOfEachExp = self.scanner.acceptingStatesOfEachExp
        self.acceptingStatesDict = self.scanner.acceptingStatesDict

        self.test_patterns = []
        self.testFile = 'tests\\'+testFile
        self.line_to_read = ''

    def read_test_file(self):
        """Funcion para leer el archivo de prueba 
            y almacenar sus contenidos.
        """
        here = os.path.dirname(os.path.abspath(__file__))
        file_ = self.testFile
        filepath = os.path.join(here, file_)
        with open(filepath, 'r') as fp:
            line = fp.readline()
            while line:
                #line = line.rstrip()
                #for i in line.split(' '):
                #    if len(i) > 0:
                #        self.test_patterns.append(i)
                #        s = ''
                print("Line #: {}".format(line.strip()))
                self.line_to_read = line
                line = fp.readline()


    def getStateId(self, states_list):
        for value in self.resultAFDArray:
            if(value[1] == states_list):
                return value[0]

    def move(self,states_set,character):
        """Representacion de la funcion move(A,a) 
        para la simulacion del AFD formado a partir 
        de los tokens definidos en un archivo atg.

        - Args:
            - states_set (list): arreglo de estados
            - c_state (set): el caracter o estado en cuestion

        - Returns:
            - list: nuevo array de estados si hay transicion
        """
        new_states_array = []
        for state in states_set:
            # trans sera nuestra transicion y debemos 
            # verificar si el caracter en cuestion esta
            # en ese set con uno o varios valores
            for trans in self.resultAFDArray:
                for i in trans[2]:
                    #if( ord(character) == i and len(trans[3]) > 0 and state == trans[0]):
                    if( i == character and len(trans[3]) > 0 and state == trans[0]):
                        nextState = self.getStateId(trans[3])
                        if(nextState not in new_states_array):
                            new_states_array.append(nextState)
        return new_states_array


    def getTokenExplicitIdentifier(self, estados):
        token = ""
        for trans in self.resultAFDArray:
            for estado in estados:
                if(estado == trans[0]):
                    for estadoInd in trans[1]:
                        for key, valor in self.acceptingStatesDict.items(): #aun no
                            if(int(estadoInd) == int(key)):
                                token = valor

                                return token
        return token

    def getTokenNonExplicitIdentifier(self, estados):
        token = ""
        for trans in self.resultAFDArray:
            for estado in estados:
                if(estado == trans[0]):
                    for estadoInd in trans[1]:
                        if(int(estadoInd) in self.acceptingStatesOfEachExp):
                            token = trans[2]
                            return token
        return token


    def moveV2(self,states_set,character):
        #! deprecated
        """Representacion de la funcion move(A,a) 
        para la simulacion del AFD formado a partir 
        de los tokens definidos en un archivo atg.
        Esta toma en cuenta que los caracteres en el 
        set de estados en cuestion sean asciis

        -Args:
            - states_set (list): arreglo de estados
            - c_state (set): el caracter o estado en cuestion

        -Returns:
            - list: nuevo arreglo de estados si hay transicion
        """
        new_states_array = []
        for state in states_set:
            # trans sera nuestra transicion y debemos 
            # verificar si el caracter en cuestion esta
            # en ese set con uno o varios valores
            for trans in self.resultAFDArray:
                for i in trans[2]:
                    if( ord(character) == i and len(trans[3]) > 0 and state == trans[0]):
                    #if( character == i and len(trans[3]) > 0 and state == trans[0]):
                        nextState = None
                        for value in self.resultAFDArray:
                            if(value[1] == trans[3]):
                                nextState = value[0]
                                break;
                        if(nextState not in new_states_array):
                            new_states_array.append(nextState)
        return new_states_array

    def getAcceptingStatesAFD(self):
        """Obtenemos estados de aceptacion del AFD

        Returns:
            list: los estados de aceptacion del afd
        """
        arrayValores = []
        for value in self.resultAFDArray:
            finalstates = self.scanner.getFinalStateId()
            for fstate in finalstates:
                if(str(fstate) in value[1]):
                    arrayValores.append(value[0])

        return arrayValores

    def simulationTest(self):
        """Simulacion del AFD de resultado
        """
        s = [0]
        for x in self.line_to_read:
            s = self.move(s, x)
        lastId = self.getAcceptingStatesAFD()

        if(len(s) > 0):
            if(s[0] in lastId):
                print('-------------------------------------------------')
                print('La cadena '+self.line_to_read+' fue aceptada por el AFD.')
                print('-------------------------------------------------')
            else:
                print('-------------------------------------------------')
                print('La cadena '+self.line_to_read+' NO fue aceptada por el AFD.')
                print('-------------------------------------------------')
        else:
            print('-------------------------------------------------')
            print('La cadena '+self.line_to_read+' NO fue aceptada por el AFD.')
            print('-------------------------------------------------')


    def simulationV1(self):
        """Simulacion del AFD de resultado
        """
        s = [0]
        for x in self.line_to_read:
            s = self.move(s, x)
        lastId = self.getAcceptingStatesAFD()

        if(len(s) > 0):
            if(s[0] in lastId):
                print('-------------------------------------------------')
                print('La cadena '+self.line_to_read+' fue aceptada por el AFD.')
                print('-------------------------------------------------')
            else:
                print('-------------------------------------------------')
                print('La cadena '+self.line_to_read+' NO fue aceptada por el AFD.')
                print('-------------------------------------------------')
        else:
            print('-------------------------------------------------')
            print('La cadena '+self.line_to_read+' NO fue aceptada por el AFD.')
            print('-------------------------------------------------')


    def simulation(self):
        """Funcion para simular una linea de entrada
        desde un archivo de prueba.

        - Returns:
            - int: 0
        """

        #contador local para llevar la posicion del caracter leido
        counter = 0

        #la dinamica aqui es leer un token y leer al mismo tiempo el siguiente
        # para saber si existira transicion cuando pasemos al siguiente
        # caracter leido, de lo contrario no sabriamos como continuar 
        # en cierto punto
        S = [0]
        S_next = [0]

        #construccion de la cadena leida
        accumulator = ""
        #acumulador de estados
        string_array = []
        #estado de aceptacion
        accepting_state = []

        # En este ciclo encapsularemos cada uno de 
        # los caracteres de la linea de entrada
        for character in self.line_to_read:
            string_array.append(character)

        #insertamos un espacio vacio al inicio
        string_array.append(" ")
        
        #Este caso se da cuando hay un solo token en el archivo
        while len(string_array) > 0:
            if(counter == len(self.line_to_read)-1):
                characterToEvaluate = self.line_to_read[counter]
                accumulator += characterToEvaluate
                S = self.move(S,characterToEvaluate)
                token = self.getTokenNonExplicitIdentifier(S)
                #lastId = self.getAcceptingStatesAFD()
                if(len(token) == 0):
                #if(S[0] not in lastId):
                    print('Invalid token: ', accumulator)
                    break
                else:
                    print('token: '+ accumulator + ' has type: '+str(token))
                    break
            characterToEvaluate = self.line_to_read[counter]
            nextCharacterToEvaluate = self.line_to_read[counter+1]
            accumulator += characterToEvaluate
            S = self.move(S,characterToEvaluate)
            S_next = self.move(S,nextCharacterToEvaluate)

            # Este caso se da cuando a travez del siguiente token ya no hay 
            # transicion hacia otro estado
            if(len(S_next) == 0 and len(S) > 0):
                token = self.getTokenNonExplicitIdentifier(S)
                #lastId = self.getAcceptingStatesAFD()
                if(len(token) == 0):
                #if(S[0] not in lastId):
                    print('Invalid token: ', accumulator)
                    S = [0]
                    S_next = [0]
                    accumulator = ""
                else:
                    print('token: '+ accumulator + ' has type: '+str(token))
                    S = [0]
                    S_next = [0]
                    accumulator = ""
            else:
                print('Invalid token: ', accumulator)
                S = [0]
                S_next = [0]
                accumulator = ""

            counter += 1
            character_popping = string_array.pop()
        return 0

# tests__________

# functions ________________________

def welcome():
    print("\n-----------------------SCANNER------------------")
    print("")

def menu():
    #os.system('cls')
    print("Seleccione una opcion.")
    print("\t1. Leer archivo de prueba")
    print("\t2. Salir")

def main():
    welcome()

    while True:
        menu()
        option = input('Ingrese una opcion: ')

        if(option == '1'):
            file_name = str(input("Ingrese el nombre del archivo de prueba(test_file.txt): "))
            obj = Scanner(file_name)
            obj.read_test_file()
            #obj.simulationTest()
            obj.simulation()

        elif(option == '2'):
            print('\nAdios! ')
            break
        else:
            input('No se ha elejido ninguna opcion en el menu. Intentalo otrdigitz! Presiona Enter!')


if __name__ == "__main__":
    main()

