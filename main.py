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
from InfixPostfixRelated.InfixRegexToPostfix import InfixRegexToPostfix

from functions import *
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
    cadena = input('Ingrese la cadena a evaluar: ')
    cadena = expresion.replace(' ','')

    obj = InfixRegexToPostfix()
    postfix = obj.infix_to_postfix(expresion)

    return postfix, cadena


# Executions ________________________

welcome()

while True:

    menu()
    opcion = input('Ingrese una opacion: ')

    if(opcion == '1'):
        cadena = ''

        postfixRegex,cadena = userInteraction()
        if(postfixRegex == 'ERROR_POSTFIX_)'):
            print('\n ")" faltante en la expresion regular ingresada. Vuelva a intentar. \n')
        else:
            print(' - postfix   = '+ postfixRegex)
            tokens = getRegExUniqueTokens(postfixRegex)
            postfixRegex = stringToArray(postfixRegex)

            print(' - alfabeto (tokens): '+str(tokens))
            #print(str(postfixRegex))

            '''objafn = AFNT(tokens,cadena)
            AFN = objafn.generateAFN(postfixRegex)

            objafd = AFDS(tokens,cadena,AFN)
            AFD = objafd.generateAFDFromAFN()'''

    elif(opcion == '2'):
        # Pruebas de funcionalidad
        postfixRegex,cadena = userInteraction()
        if(postfixRegex == 'ERROR_POSTFIX_)'):
            print('\n ")" faltante en la expresion regular ingresada. Vuelva a intentar. \n')
        else:
            print('\nExpresion postfix: '+ postfixRegex)
            tokens = getRegExUniqueTokens(postfixRegex)
            postfixRegex = stringToArray(postfixRegex)

            print(tokens)
            print(postfixRegex)

            '''objdirect = AFDD(tokens,cadena,postfixRegex)
            AFD = objdirect.generateDirectAFD()'''

    elif(opcion == '3'):
        print('\nAdios! ')
        break
    else:
        input('No se ha elejido ninguna opcion en el menu. Intentalo otravez! Presiona Enter!')


