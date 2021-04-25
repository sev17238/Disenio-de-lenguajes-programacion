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
from infix_postfix_related.InfixRegexToPostfix import InfixRegexToPostfix
from thompson.AFNT import AFNT
from subsets.Subsets import Subsets
#from direct.DirectAFD_d import DirectAFD
from direct.DirectAFD import DirectAFD
from functions import functions
import collections


# functions ________________________

def welcome():
    print("________________________________________BIENVENIDO_________________________________________")
    print("Primera implementacion para la construccion de automatas a partir de expresiones regulares.")
    print()

def menu():
    #os.system('cls')
    print("Seleccione una opcion.")
    print("\t1. Metodo de Conversion por Thompson y Subconjuntos")
    print("\t2. Metodo de Conversion Directa")
    print("\t3. Salir")

def userInteraction():
    expresion = input('Ingrese una expresion regular: ')
    expresion = expresion.replace(' ','')
    chain = input('Ingrese la cadena a evaluar: ')
    chain = chain.replace(' ','')

    obj = InfixRegexToPostfix()
    postfix = obj.infix_to_postfix(expresion)

    return postfix, chain

def userInteractionDirect():
    '''En esta funcion se agrega el '#' para las operaciones relacionados a la conversion directa. '''
    expresion = input('Ingrese una expresion regular: ')
    expresion = expresion.replace(' ','')
    chain = input('Ingrese la cadena a evaluar: ')
    chain = chain.replace(' ','')

    obj = InfixRegexToPostfix()
    expresion = '('+expresion+')#'
    postfix = obj.infix_to_postfix(expresion)

    return postfix, chain


# Executions ________________________

welcome()
functions = functions()
while True:

    menu()
    option = input('Ingrese una opcion: ')

    if(option == '1'):
        chain = ''

        postfixRegex,chain = userInteraction()
        if(postfixRegex == 'ERROR_POSTFIX_)'):
            print('\n ")" faltante en la expresion regular ingresada. Vuelva a intentar. \n')
        else:
            print(' - postfix     = '+ postfixRegex)
            tokens = functions.getRegExUniqueTokens(postfixRegex)
            postfixRegex = functions.stringToArray(postfixRegex)

            print(' - alfabeto (tokens): '+str(tokens))

            obj_afn = AFNT(tokens,chain)
            AFN = obj_afn.generateAFN(postfixRegex)
            
            obj_afd = Subsets(tokens,chain,AFN)
            AFD = obj_afd.afn_to_afd_process()

    elif(option == '2'):
        # Pruebas de funcionalidad
        postfixRegex,chain = userInteractionDirect()
        if(postfixRegex == 'ERROR_POSTFIX_)'):
            print('\n ")" faltante en la expresion regular ingresada. Vuelva a intentar. \n')
        else:
            print(' - postfix     = '+ postfixRegex)
            tokens = functions.getRegExUniqueTokens(postfixRegex)
            postfixRegex = functions.stringToArray(postfixRegex)

            print(' - alfabeto (tokens): '+str(tokens))

            #objdirect = DirectAFD(tokens,chain,postfixRegex)2
            #AFD = objdirect.generateDirectAFD()

            objdirect = DirectAFD(tokens,chain,postfixRegex)
            AFD = objdirect.generateDirectAFD()

    elif(option == '3'):
        print('\nAdios! ')
        break
    else:
        input('No se ha elejido ninguna opcion en el menu. Intentalo otravez! Presiona Enter!')


