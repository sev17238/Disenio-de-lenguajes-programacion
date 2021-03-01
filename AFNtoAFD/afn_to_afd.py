######################################################
# Diego Sevilla
# 17238
######################################################
# afn_to_afd.py
######################################################
# Python3 programa que recibe dos entradas.
# 1. String: Contendra una expresion regular
# 2. AFN: Archivo csv con la tabla de transicion de
#         un AFN.
######################################################

# imports _________________________
from prettytable import PrettyTable
from prettytable import from_csv

import pandas as pd
import sys, getopt

import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


# Definitions _________________________
conjuntos = []  # contendra los estados
afn_tran_table = [] #tabla de transisicion del automata finito no determinista

afd_tran_table= []

# Functions area______________________________________________
def transition_afn_table(csvfile='afn-tran-table.csv'):
    '''
    Funcion para leer la tabla de transiciones de un afn cualquiera 
    desde un archivo csv separado por ';'.

    Params:
     - csvFile: archivo csv con la representacion de un afn cualquiera
    '''
    my_file = os.path.join(THIS_FOLDER, csvfile)
    df = pd.read_csv(my_file,sep=";",header=None)
    
    #print(df.to_string()) # table
        #print(len(df))        #number of rows
        #print(df.values[0])   #each row
        #print(df.values[1]) 
        #print(df.values[2]) 
        #print(df.values[3]) 
        #print(df.values[4]) 
        #
        #estados = []
        #for estado in range(len(df)):
        #    estados.append(df.values[estado][0])
        #print(str(estados))

    transiciones = []
    for col in range(len(df.values[0])):
        alfabetoTrans = []
        for row in range(len(df)):
            alfabetoTrans.append(df.values[row][col])
        transiciones.append(alfabetoTrans)

    return transiciones

def move(conjuntoEstados,transicion,afnTranTable):
    '''
    Funcion mover() que retorna los estados del conjunto de estados proporcionado, que pasan 
    por la transicion especificada. Ej. move(A,a)

    Params:
     - conjuntoEstados: Un conjunto de estados de un AFN Ej. A = {0,1,2,4,7}
     - transicion: transicion por la que pueden pasar algunos de los estados en A
     - afnTranTable: tabla de transiciones del AFN en question
    '''


    return 0

def epsilon_closure(move,afnTranTable,start=False):
    '''
    Funcion de cerradura epsilon que retorna todos los estados a los que se puede
    llegar en el AFN a travez de epsilon 

    Params:
     - move: Resultado proporcionado por la funcion mover()
     - afnTranTable: tabla de transiciones del AFN en question
     - **Dtran(A,a) = epsilon_closure(move(A,a))
    '''
    stateSet = []
    if (start):
        _move_ = ['0']
        stateSet.append[_move_]
        epsilonStates = afnTranTable[len(afnTranTable)-1] #ultima posicion de atnTranTable = Estados_epsilon
        for i in range(len(epsilonStates)):
            # Ej. epsilonState = '1,2,3' o epsilonState = '1'
            if(len(epsilonStates[i].split(',')) > 1): 
                epsilonStateSet = epsilonStates[i].split(',')
                for e in range(len(epsilonStateSet)):
                    #stateSet = [0,1,2,...,s]
                    stateSet.append(epsilonStateSet[e])
            else:
                epsilonStateSet = epsilonStates[i]
                stateSet.append(epsilonStateSet)
            break
        

    else:
        c = 's'


    return stateSet




def convertion_from_afn_to_afd():
    '''
    Funcion que utiliza 
    '''

    return 0



# Main______________________________________________
def main():
    file=''
    afn_tran_table = []

    try:
        file = str(sys.argv[1])
        afn_tran_table = transition_afn_table(file)

        print(file)
        print(afn_tran_table)

        sarray = '1'
        arr = sarray.split(',')
        print(arr)

    except ValueError:
        print("Check the input parameters. Try again...")

    # print(x.get_string(fields=["Estado"])[0])
    # print(x)



if __name__ == "__main__":
    main()


#python afn_to_afd.py afn-tran-table.csv
