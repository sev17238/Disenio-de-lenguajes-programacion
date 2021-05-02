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
    def __init__(self,testFile = 'test_file.txt'):
        self.scanner = pickle.load(open('cocor/scanner'+testFile[:-4]+'.scann'.lower(),'rb'))
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
        """Regresara el identificador del estado

        Args:
            states_list (list): lista de estados

        Returns:
            int: el estado
        """
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
        """Funcion que retornara el identificador explicito 
        del token en cuestion. Retornara el lado izquierdo
        de la expresion. Ej. number = digit(digit)*

        Args:
            estados (list): lista de estados

        Returns:
            set: el set con los posibles caracteres pertenecientes
            a ese token particular
        """
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
        """Funcion que retornara el identificador no explicito 
        del token en cuestion. Retornara el lado derecho
        de la expresion. Ej. number = digit(digit)*

        Args:
            estados (list): lista de estados

        Returns:
            set: el set con los posibles caracteres pertenecientes
            a ese token particular
        """
        token = ""
        for trans in self.resultAFDArray:
            for estado in estados:
                if(estado == trans[0]):
                    for estadoInd in trans[1]:
                        acc1 = self.acceptingStatesOfEachExp
                        acc2 = self.getAcceptingStatesAFD()
                        #if(int(estadoInd) in acc1):
                        if(int(estadoInd) in acc2):
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
        """Obtenemos estados de aceptacion 
        del AFD

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
        token_construction = ""
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
                token_construction += characterToEvaluate
                S = self.move(S,characterToEvaluate)
                token = self.getTokenNonExplicitIdentifier(S)
                #lastId = self.getAcceptingStatesAFD()
                if(len(token) == 0):
                #if(S[0] not in lastId):
                    print('Invalid token: ', token_construction)
                    break
                print('token: '+ token_construction + ' has type: '+str(token))
            characterToEvaluate = self.line_to_read[counter]
            nextCharacterToEvaluate = self.line_to_read[counter+1]
            token_construction += characterToEvaluate
            S = self.move(S,characterToEvaluate)
            S_next = self.move(S,nextCharacterToEvaluate)

            # Este caso se da cuando a travez del siguiente token ya no hay 
            # transicion hacia otro estado
            if(len(S) > 0 and len(S_next) == 0):  
                token = self.getTokenNonExplicitIdentifier(S)
                #lastId = self.getAcceptingStatesAFD()
                if(len(token) == 0):
                #if(S[0] not in lastId):
                    print('Invalid token: ', token_construction)
                    S = [0]
                    S_next = [0]
                    token_construction = ""
                    counter -= 1
                else:
                    print('token: '+ token_construction + ' has type: '+str(token))
                    S = [0]
                    S_next = [0]
                    token_construction = ""
            elif(len(S) == 0):
                print('Invalid token: ', token_construction)
                S = [0]
                S_next = [0]
                token_construction = ""

            counter += 1
            character_popping = string_array.pop()

        print('')

    def simulationV2(self):
        """Simulacion del AFD de resultado
        """
        s = [0]
        s2 = [0]
        counter = 0
        token_construction = ''

        while counter < len(self.line_to_read)-1:
            curr_char = self.line_to_read[counter]
            next_char = self.line_to_read[counter+1]
            s = self.move(s, curr_char)
            s2 = self.move(s, next_char)
            token_construction += curr_char

            #si el caracter siguiente es cero, entonces ahi debemos parar de evaluar una cadena
            if(len(s) > 0 and len(s2) == 0): # 
                token = self.getTokenNonExplicitIdentifier(s)
                lastId = self.getAcceptingStatesAFD()
                if(len(token) == 0):
                #if(S[0] not in lastId):
                    print('Invalid token: ', token_construction)
                    s = [0]
                    s2 = [0]
                    token_construction = ""
                else:
                    if s[0] in lastId:
                        print('La cadena '+token_construction+' fue aceptada por el AFD.')
                    else: 
                        print('La cadena '+token_construction+' NO fue aceptada por el AFD.')

                    print('token: '+ token_construction + ' has type: '+str(token))
                    s = [0]
                    s2 = [0]
                    token_construction = ""
                print('Invalid token: --> '+ str(curr_char)+' <--')
            #si el caracter actual es cero entonces el token es invalido.
            else:
                print('La cadena '+token_construction+' NO fue aceptada por el AFD.')
                print('Invalid token: ', token_construction)
                S = [0]
                S_next = [0]
                token_construction = ""
            
            counter +=1
        
        '''lastId = self.getAcceptingStatesAFD()

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
            print('-------------------------------------------------')'''


    

# tests__________

# functions ________________________

def welcome():
    print("\n-----------------------SCANNER------------------")
    print("")

def menu():
    #os.system('cls')
    print("Seleccione una opcion.")
    print("\t1. Leer archivo de prueba")
    print("\t2. Leer un solo string en archivo (pruebas)")
    #print("\t3. Leer archivo de pruebaa (pruebas)")
    print("\t4. Salir")

def main():
    welcome()

    while True:
        menu()
        option = input('Ingrese una opcion: ')

        if(option == '1'):
            file_name = str(input("Ingrese el nombre del archivo de prueba (Ej. aritmetica.txt): "))
            obj = Scanner(file_name)
            obj.read_test_file()
            obj.simulation()

        elif(option == '2'):
            file_name = str(input("Ingrese el nombre del archivo de prueba (Ej. aritmetica.txt): "))
            obj = Scanner(file_name)
            obj.read_test_file()
            obj.simulationTest()
            #obj.simulationV2()

        #elif(option == '3'):
        #    file_name = str(input("Ingrese el nombre del archivo de prueba (Ej. aritmetica.txt): "))
        #    obj = Scanner(file_name)
        #    obj.read_test_file()
        #    obj.simulationV2()

        elif(option == '4'):
            print('\nAdios! ')
            break
        else:
            input('No se ha elejido ninguna opcion en el menu. Intentalo de nuevo! Enter -->')


if __name__ == "__main__":
    main()

