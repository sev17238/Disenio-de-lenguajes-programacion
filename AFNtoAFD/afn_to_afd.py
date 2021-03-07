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
#conjuntos = []  # contendra los estados
#afn_tran_table = [] #tabla de transisicion del automata finito no determinista
#afd_tran_table= []

# Functions area______________________________________________
def transition_afn_table(csvfile='afn-tran-table.csv'):
    '''
    Funcion para leer la tabla de transiciones de un afn cualquiera 
    desde un archivo csv separado por ';'.

    Params:
     - csvFile: archivo csv con la representacion de un afn cualquiera
     - return - [[Estados,...],[a,...],[b,...],[c,...]....,[Epsilon,...]]
    '''
    my_file = os.path.join(THIS_FOLDER, csvfile)
    df = pd.read_csv(my_file,sep=";")
    df_header = pd.read_csv(my_file,sep=";",header=None)

    #print(df.to_string()) # table
        #print(len(df))        #number of rows
        #print(df.values[0])   #each row
        #print(df.values[1]) 
        #print(df.values[2]) 
        #print(df.values[3]) 
        #print(df.values[4]) 

    transiciones = []
    for col in range(len(df.values[0])):
        alfabetoTrans = []
        for row in range(len(df)):
            alfabetoTrans.append(df.values[row][col])
        transiciones.append(alfabetoTrans)

    alfabeto = []
    for abc in range(1,len(df_header.values[0])-1):
        alfabeto.append(df_header.values[0][abc])

    return transiciones, alfabeto

def move(statesSet=[],transition=None,afnTranTable=[]):
    '''
    Funcion mover() que retorna los estados del conjunto de estados proporcionado, que pasan 
    por la transicion especificada. Ej. move(A,a) ~ move(A,0)

    Params:
     - statesSet: Un conjunto de estados de un AFN Ej. A = {0,1,2,4,7}
     - transition: transicion por la que pueden pasar algunos de los estados en A. En 
       este caso sabemos que (a, b, c ~ 0, 1, 2) por lo tanto se ingresa la posicion 
       del token en el array con el alfabeto.
     - afnTranTable: tabla de transiciones del AFN en question
     - return - [3,8]
    '''
    if(transition == None):
        return ['0']
    else:
        result = []
        transition_column = afnTranTable[transition+1]
        for i in range(len(statesSet)):
            state_of_Set_param = statesSet[i] #0
            state = transition_column[int(state_of_Set_param)]
            # Se revisa que el estado no sea nulo
            if(state != 'vacio' and int(state) == False):
                result.append(transition_column[int(state_of_Set_param)].split(','))
            elif(state != 'vacio' and int(state)):
                result.append(transition_column[int(state_of_Set_param)])

        return result

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
    state_ = int(state)
    if (afnStates[state_] == state_):
        if(epsilonStates[state_] != 'vacio'):
            statesThroughEpsilon = epsilonStates[state_].split(',')
            return statesThroughEpsilon

    return statesThroughEpsilon

def epsilon_closure(move,afnTranTable):
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
    epsilonStates = afnTranTable[len(afnTranTable)-1] #ultima posicion de afnTranTable = Estados_transicion_epsilon
    
    for m in range(len(move)):
        i = int(move[m])
        stateSet.append(move[m])

        # epsilon = [['1,7'],['2,4'],...,[s]]
        
        # Ej. epsilonState = '1,7'
        if(len(epsilonStates[i].split(',')) > 1 and epsilonStates[i] != 'vacio'): 
            epsilonStateSet = epsilonStates[i].split(',') # ['1','7'] (i = 0)
            for e in range(len(epsilonStateSet)):
                #stateSet = ['1',...].append('7') (e = 1)
                state = epsilonStateSet[e] #7
                stateSet.append(state) 
                epsilonTransitionState = find_epsilon_transitions_state(epsilonStates,afnTranTable[0],state)
                lastAppends = 0
                if(len(epsilonTransitionState) > 1):
                    for ii in range(len(epsilonTransitionState)):
                        stateSet.append(epsilonTransitionState[ii])
                        lastAppends += 1
                elif(len(epsilonTransitionState) == 1):
                    stateSet.append(epsilonTransitionState[0])
                    lastAppends += 1

            s = len(stateSet)-lastAppends
            while (s != len(stateSet)):
                stateSetAppends = stateSet[s]
                epsilonTransitionState = find_epsilon_transitions_state(epsilonStates,afnTranTable[0],stateSetAppends)

                if(len(epsilonTransitionState) > 1):
                    for ii in range(len(epsilonTransitionState)):
                        stateSet.append(epsilonTransitionState[ii])
                elif(len(epsilonTransitionState) == 1):
                    stateSet.append(epsilonTransitionState[0])
                s += 1

            # delete duplicate values
            stateSet = list(dict.fromkeys(stateSet))
            #sort ascendent
            stateSet.sort(key = int)

        #Ej. epsilonState = '1'
        elif(len(epsilonStates[i].split(',')) == 1 and epsilonStates[i] != 'vacio'):
            epsilonStateSet = epsilonStates[i]
            stateSet.append(epsilonStateSet)
            epsilonTransitionState = find_epsilon_transitions_state(epsilonStates,afnTranTable[0],epsilonStateSet)

            lastAppends = 0
            if(len(epsilonTransitionState) > 1):
                for ii in range(len(epsilonTransitionState)):
                    stateSet.append(epsilonTransitionState[ii])
                    lastAppends += 1
            elif(len(epsilonTransitionState) == 1):
                stateSet.append(epsilonTransitionState[0])
                lastAppends = 1

            s = len(stateSet)-lastAppends
            while (s != len(stateSet)):
                stateSetAppends = stateSet[s]
                epsilonTransitionState = find_epsilon_transitions_state(epsilonStates,afnTranTable[0],stateSetAppends)

                if(len(epsilonTransitionState) > 1):
                    for ii in range(len(epsilonTransitionState)):
                        stateSet.append(epsilonTransitionState[ii])
                elif(len(epsilonTransitionState) == 1):
                    stateSet.append(epsilonTransitionState[0])
                s += 1
            
            # delete duplicate values
            stateSet = list(dict.fromkeys(stateSet))
            #sort ascendent
            stateSet.sort(key = int)

    return stateSet


def convertion_from_afn_to_afd(afn_tran_table,alfabeto):
    '''
    Funcion que utiliza Dtran[A,a] = epsilon_closure(move(A,a)) para generar 
    los estados del afn en la tabla de transiciones del afd.

    Parametros:
     - afn_tran_table: tabla de transiciones del afn
     - alfabeto: el alfabeto de entrada
    '''

    '''m = move()
    A = epsilon_closure(m,afn_tran_table)
    print('A = '+str(A))

    m = move(A,0,afn_tran_table)
    print('move(A,a) = '+str(m))
    B = epsilon_closure(m,afn_tran_table)
    print('B = '+str(B))

    m = move(A,1,afn_tran_table)
    print('move(A,b) = '+str(m))
    C = epsilon_closure(m,afn_tran_table)
    print('C = '+str(C))

    m = move(B,0,afn_tran_table)
    print('move(B,a) = '+str(m))
    B = epsilon_closure(m,afn_tran_table)
    print('B = '+str(B))

    m = move(B,1,afn_tran_table)
    print('move(B,b) = '+str(m))
    D = epsilon_closure(m,afn_tran_table)
    print('D = '+str(D))

    m = move(D,1,afn_tran_table)
    print('move(D,b) = '+str(m))
    E = epsilon_closure(m,afn_tran_table)
    print('E = '+str(E))'''

    afn_states = []
    m = move()
    afn_states.append(epsilon_closure(m,afn_tran_table))
    print('A = '+str(epsilon_closure(m,afn_tran_table)))

    #afn_states_len = len(afn_states)
    #for afnS in range(0,afn_states_len):
    afnS = 0
    while (afnS < len(afn_states)):
        print('len(afn)'+str(afnS))
        print('afn-states: '+str(afn_states))
        appends = 0
        for token in range(len(alfabeto)): #0, 1 ~ a, b
            m = move(afn_states[afnS],token,afn_tran_table)
            d_tran = epsilon_closure(m,afn_tran_table)

            # revisamos si el conjunto de estados ya existe en afn_states
            exist = False
            for x in range(len(afn_states)):
                if(d_tran == afn_states[x]):
                    exist = True
            # si no existe entonces agregaremos un nuevo set de estados
            if(exist == False):
                #revisamos si tiene el estado de aceptacion para detener el ciclo
                print('d_tran last: '+str(d_tran[len(d_tran)-1])+' aceptacion: '+str(afn_tran_table[0][len(afn_tran_table[0])-1]))
                if(str(d_tran[len(d_tran)-1]) == str(afn_tran_table[0][len(afn_tran_table[0])-1])): 
                    print('sdfaslkdjfa')
                    afn_states.append(d_tran)
                    appends += 1
                    #afnS = len(afn_states)
                    #break
                #sino contiene el estado de aceptacion continuar
                else:
                    print(str(afnS)+' = '+str(d_tran))
                    afn_states.append(d_tran) 
                    appends += 1
        afnS += 1

    

    return afn_states


# Main______________________________________________
def main():
    file=''
    afn_tran_table = []

    #file = str(sys.argv[1])
    file = 'afn-tran-table.csv'
    afn_tran_table, alfabeto = transition_afn_table(file)
    print(file)
    print('tabla: '+str(afn_tran_table))
    print('alfabeto: '+str(alfabeto))

    '''tests..
    sarray = ''
    arr = sarray.split(',')
    print(arr)
    lala = ['a', 'b', 'c'] 
    lele = ['a', 'b', 'c'] 
    lili = ['a', 'c', 'b'] 
    print(lala == lele)
    print(lala == lili)'''

    convertion_from_afn_to_afd(afn_tran_table,alfabeto)




#Main ________________________
if __name__ == "__main__":
    main()


#python afn_to_afd.py afn-tran-table.csv
