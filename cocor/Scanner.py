######################################################
# Diego Sevilla
# 17238
######################################################
# Cocor.py
######################################################

#imports
import os
import sys
sys.path.append(".")
from os.path import basename
from functions import functions
from infix_postfix_related.InfixRegexToPostfixWords import InfixRegexToPostfixWords
import string
import pickle
import time

#Clase de implementacion_________________________________________________
class Scanner:
    """Archivo que utiliza las transiciones para leer el archivo de prueba
    """
    # Constructor de las variables
    def __init__(self):
        self.sc = open('cocor/scanner', 'rb')     
        self.scanner = pickle.load(self.sc)

        self.test_patterns = []

        self.testFile = 'test_file.cfg'

    def read_test_file(self):
        """Funcion para leer el archivo de prueba y almacenar sus contenidos.
        """
        here = os.path.dirname(os.path.abspath(__file__))
        file_ = self.testFile
        filepath = os.path.join(here, file_)
        with open(filepath,'r') as fp:
            line = fp.readline()
            while line:
                line = line.rstrip()
                for i in line.split(' '):
                    if len(i) > 0:
                        self.test_patterns.append(i)
                        s = ''
                print("Line #: {}".format( line.strip()))
                line = fp.readline()

    def simulation(self):
        
        return 0

#tests__________
def main():
    obj = Scanner()
    obj.read_test_file()


    print()
    


if __name__ == "__main__":
    main()
