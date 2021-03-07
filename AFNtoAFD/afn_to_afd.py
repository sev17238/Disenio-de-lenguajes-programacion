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
     - return - [[Estados,...],[a,...],[b,...],...,[Epsilon,...]]
    '''
    my_file = os.path.join(THIS_FOLDER, csvfile)
    df = pd.read_csv(my_file,sep=";")
    #df = pd.read_csv(my_file,sep=";",header=None)
    #df_no_headers = df = pd.read_csv(my_file,sep=";")

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
     - return - [3,8]
    '''


    return 0

def find_epsilon_transitions_state(epsilonStates,afnStates,state):
    '''
    Funcion que retorna las transiciones en epsilon de un estado determinado.

    Parametros:
     - epsilonStates: lista que contiene los estados o set de estados con transicion en epsilon
     - afnStates: lista que contiene los estados del AFN
     - state: el estado del AFN determinado
     - return - [2,4]
    '''
    statesThroughEpsilon = []
    '''for i in range(len(afnStates)):
        if (afnStates[i] == int(state)):
            if(epsilonStates[i] != 'vacio'):
                statesThroughEpsilon = epsilonStates[i].split(',')
                #print('sheet')
                return statesThroughEpsilon'''
    state_ = int(state)
    if (afnStates[state_] == state_):
        if(epsilonStates[state_] != 'vacio'):
            statesThroughEpsilon = epsilonStates[state_].split(',')
            #print('sheet')
            return statesThroughEpsilon

    return statesThroughEpsilon


def epsilon_closure(move,afnTranTable,start=False):
    '''
    Funcion de cerradura epsilon que retorna todos los estados a los que se 
    puede llegar en el AFN a travez de epsilon. 
    Ej. epsilon_closure({3,8},transition_afn_table(),True)

    Params:
     - move: Resultado proporcionado por la funcion mover()
     - afnTranTable: tabla de transiciones del AFN en question
     - return - Dtran(A,a) = epsilon_closure(move(A,a)) = [1,2,3,4,6,7,8]
    '''
    stateSet = []
    if (start):
        stateSet.append(move[0])
        epsilonStates = afnTranTable[len(afnTranTable)-1] #ultima posicion de afnTranTable = Estados_transicion_epsilon

        # epsilon = [['1,7'],['2,4'],...,[s]]
        #for i in range(len(epsilonStates)):

        i = 0
        # Ej. epsilonState = '1,7'
        print(epsilonStates[i].split(','))
        if(len(epsilonStates[i].split(',')) > 1 and epsilonStates[i] != 'vacio'): 
            epsilonStateSet = epsilonStates[i].split(',') # ['1','7'] (i = 0)
            for e in range(len(epsilonStateSet)):
                #stateSet = ['1',...].append('7') (e = 1)
                state = epsilonStateSet[e] #7
                stateSet.append(state) 
                epsilonTransitionState = find_epsilon_transitions_state(epsilonStates,afnTranTable[0],state)

                if(len(epsilonTransitionState) > 1):
                    for ii in range(len(epsilonTransitionState)):
                        stateSet.append(epsilonTransitionState[ii])
                elif(len(epsilonTransitionState) == 1):
                    stateSet.append(epsilonTransitionState[0])

            # order states
            stateSet = list(dict.fromkeys(stateSet))
            stateSet.sort(key = int) 
        #Ej. epsilonState = '1'
        elif(len(epsilonStates[i].split(',')) == 1 and epsilonStates[i] != 'vacio'):
            epsilonStateSet = epsilonStates[i]
            stateSet.append(epsilonStateSet)
            epsilonTransitionState = find_epsilon_transitions_state(epsilonStates,afnTranTable[0],epsilonStateSet)
            #print(str(epsilonStates) +'; '+str(afnTranTable[0])+'; '+str(epsilonStateSet))
            if(len(epsilonTransitionState) > 1):
                for ii in range(len(epsilonTransitionState)):
                    stateSet.append(epsilonTransitionState[ii])
            elif(len(epsilonTransitionState) == 1):
                stateSet.append(epsilonTransitionState[0])

            #break




    return stateSet




def convertion_from_afn_to_afd():
    '''
    Funcion que utiliza Dtran[A,a] = epsilon_closure(move(A,a)) para generar 
    la tabla de transiciones del afd.
    '''

    return 0



# Main______________________________________________
def main():
    file=''
    afn_tran_table = []

    #file = str(sys.argv[1])
    file = 'afn-tran-table.csv'
    afn_tran_table = transition_afn_table(file)
    print(file)
    print(afn_tran_table)

    '''

    sarray = ''
    arr = sarray.split(',')
    print(arr)
    lala = ['a', 'b', 'c'] 
    lele = ['a', 'b', 'c'] 
    lili = ['a', 'c', 'b'] 
    print(lala == lele)
    print(lala == lili)'''

    m = ['0']
    A = epsilon_closure(m,afn_tran_table,True)
    print('A: '+str(A))
    #
    #print(m[0])s






    # print(x.get_string(fields=["Estado"])[0])
    # print(x)



if __name__ == "__main__":
    main()


#python afn_to_afd.py afn-tran-table.csv
