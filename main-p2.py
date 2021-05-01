######################################################
# Diego Sevilla
# 17238
######################################################
# main.py
######################################################
# Archivo que centraliza las funcionalidades del
# proyecto.
######################################################

# imports _________________________
import os
import sys
sys.path.append(".")
from infix_postfix_related.InfixRegexToPostfixWords import InfixRegexToPostfixWords
from direct.DirectAFDWords import DirectAFDWords
from cocor.Cocor import Cocor

from cocor.Scanner import Scanner
from functions import functions
import collections
import pickle


# functions ________________________

def welcome():
    print("\n-----------------------Coco/R tests------------------")
    print("Welcome!!")

def menu():
    #os.system('cls')
    print("Seleccione una opcion.")
    print("\t1. Leer archivos")
    print("\t2. Metodo de Conversion Directa y generar scanner.py")
    print("\t3. Salir")

# Executions ________________________

welcome()
coco_obj = Cocor()
functions = functions()

postfixRegex = []
def_file = ''
while True:

    menu()
    option = input('Ingrese una opcion: ')

    if(option == '1'):
        def_file = input('Ingrese el nombre del archivo con las definiciones (Ej. Aritmetica.cfg): ')
        
        coco_obj.read_def_cfg(def_file)
        #coco_obj.read_test_file(test_file)

        coco_obj.charactersSubstitution()
        coco_obj.cocorToP1Convention()
        coco_obj.tokensPreparationPostfix()

        coco_obj.orBetweenExpresions()
        postfixRegex = coco_obj.expresionSubstitutions()


    elif(option == '2'):
        # Pruebas de funcionalidad
        #postfixRegex = ['digit', 'letter', '|', '*', 'digit', '~', 'letter', '~', 'letter', '~', '#', '~']
        #postfixRegex = ['a', 'b', '|', '*', 'a', '~', 'b', '~', 'b', '~', '#', '~']

        if(postfixRegex == ['ERROR_POSTFIX_)']):
            print('\n ")" faltante en la expresion regular ingresdigit. Vuelva a intentar. \n')
        else:
            print(' - postfix     = '+ str(postfixRegex))
            tokens = functions.getRegExUniqueTokensV2(postfixRegex)
            print(' - alfabeto (tokens): '+str(tokens))

            #chain = 'digit letter digit letter letter'
            chain = '12356'

            objdirect = DirectAFDWords(tokens,chain,postfixRegex)
            AFD = objdirect.generateDirectAFD()

            # Its important to use binary mode
            store_transitions = open('cocor/scanner'+def_file[:-4].lower(), 'ab')
            # source, destination
            pickle.dump(objdirect, store_transitions)                     
            store_transitions.close()

    elif(option == '3'):
        print('\nAdios! ')
        break
    else:
        input('No se ha elejido ninguna opcion en el menu. Intentalo otrdigitz! Enter -->')


