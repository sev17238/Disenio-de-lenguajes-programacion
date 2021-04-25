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
from functions import functions
import collections


# functions ________________________

def welcome():
    print("Coco/R tests")
    print()

def menu():
    #os.system('cls')
    print("Seleccione una opcion.")
    print("\t1. Leer archivos")
    print("\t2. Metodo de Conversion Directa")
    print("\t3. Salir")

# Executions ________________________

welcome()
coco_obj = Cocor()
functions = functions()

while True:

    menu()
    option = input('Ingrese una opcion: ')

    if(option == '1'):
        def_file = input('Ingrese el nombre del archivo con las definiciones (def_file.cfg): ')
        test_file = input('Ingrese el nombre del archivo de prueba (test_file.cfg): ')
        coco_obj.read_def_cfg(def_file)
        coco_obj.read_test_file(test_file)
        coco_obj.cocorToP1Convention()
        coco_obj.tokensToPosfix()


    elif(option == '2'):
        # Pruebas de funcionalidad
        postfixRegex = ['digit', 'letter', '|', '*', 'digit', '~', 'letter', '~', 'letter', '~', 'α', '~']
        #postfixRegex = ['a', 'b', '|', '*', 'a', '~', 'b', '~', 'b', '~', 'α', '~']

        if(postfixRegex == 'ERROR_POSTFIX_)'):
            print('\n ")" faltante en la expresion regular ingresdigit. Vuelva a intentar. \n')
        else:
            print(' - postfix     = '+ str(postfixRegex))
            tokens = functions.getRegExUniqueTokensV2(postfixRegex)
            print(' - alfabeto (tokens): '+str(tokens))

            #chain = 'digit letter digit letter letter'

            chain = 'ababb'
            objdirect = DirectAFDWords(tokens,chain,postfixRegex)
            AFD = objdirect.generateDirectAFD()

    elif(option == '3'):
        print('\nAdios! ')
        break
    else:
        input('No se ha elejido ninguna opcion en el menu. Intentalo otrdigitz! Presiona Enter!')


