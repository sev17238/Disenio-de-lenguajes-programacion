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
from InfixPostfixRelated import infix_regex_to_postfix
import collections


# functions ________________________

def welcome():
    print("_______________________________________BIENVENIDO______________________________________")
    print("Primera implementacion para la creacion de automatas a partir de expresiones regulares.")
    print()

def menu():
    os.system('cls')
    print("Seleccione una opcion.")
    print("\t1. Metodo de Thompson")
    print("\t1. Metodo Directo")

# Executions ________________________

welcome()

while True:

    menu()
    opcion = input('Ingrese una opacion: ')
    expresion = ''
    cadena = ''

    if(opcion == '1'):
        expresion = ''
        cadena = ''
        print()

        # Pruebas de funcionalidad
        expresion = input('Ingrese una expresion regular: ')
        expresion = expresion.replace(' ','')
        cadena = input('Ingrese la cadena a evaluar: ')
        cadena = expresion.replace(' ','')

        postfix = infix_regex_to_postfix()


