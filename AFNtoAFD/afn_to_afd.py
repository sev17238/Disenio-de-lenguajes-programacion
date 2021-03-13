######################################################
# Diego Sevilla
# 17238
######################################################
# afn_to_afd.py
######################################################
# Python3 programa que recibe una entrada.
# 1. AFN: Archivo csv con la tabla de transicion de
#         un AFN generada con el algoritmo de 
#         thompson.
######################################################

# imports _________________________
import csv
import pandas as pd
import sys, getopt
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
OUTPUTFILENAMES = ['afd-transitions-x-2.txt','afd-tran-table-x-2.txt']
INPUTFILENAME = 'afn-tran-table-x-2.csv'

#constants area______________________________________________
'''Abecedario'''
abc_dic = {
  'A': 1 ,
  'B': 2 ,
  'C': 3 ,
  'D': 4 ,
  'E': 5 ,
  'F': 6 ,
  'G': 7 ,
  'H': 8 ,
  'I': 9 ,
  'J': 10,
  'K': 11,
  'L': 12,
  'M': 13,
  'N': 14,
  'O': 15,
  'P': 16,
  'Q': 17,
  'R': 18,
  'S': 19,
  'T': 20,
  'U': 21,
  'V': 22,
  'W': 23,
  'X': 24,
  'Y': 25,
  'Z': 26
}

# Functions area______________________________________________
def get_key(character):
    '''
    Funcion que retorna la llave para un caracter cualquiera.

    Parametros:
     - character: un caracter o token 
    '''
    #print('character: '+character)
    for key, value in abc_dic.items():
        if character == value:
            return key

    return None

def transition_afn_table(csvfile=INPUTFILENAME):
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
            if(state != '~' and state.find(',') != -1): #chequeo de 1 o mas estados separados por comas
                result.append(transition_column[int(state_of_Set_param)].split(','))
            elif(state != '~' and state.find(',') == -1):
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
        if(epsilonStates[state_] != '~'):
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
        if(len(epsilonStates[i].split(',')) > 1 and epsilonStates[i] != '~'): 
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

            # Eliminacion de duplicados
            stateSet = list(dict.fromkeys(stateSet))
            # ordenamiento ascendente
            stateSet.sort(key = int)

        #Ej. epsilonState = '1'
        elif(len(epsilonStates[i].split(',')) == 1 and epsilonStates[i] != '~'):
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

            # Eliminacion de duplicados
            stateSet = list(dict.fromkeys(stateSet))
            # ordenamiento ascendente
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

    afn_states = []
    # calculo de epsilon-closure(move(['0']))
    estadoInicial = []
    m = move()
    afn_states.append(epsilon_closure(m,afn_tran_table))
    print('00 = '+str(epsilon_closure(m,afn_tran_table)))
    estadoInicial.append(m[0])

    afnS = 0
    trans_afds = [] #todas las transiciones del afd para cada estado del afn
    trans_afd_marks = []
    estadoAceptacion = []
    while (afnS < len(afn_states)):
        print('afn-states: '+str(afn_states))
        appends = 0
        trans_afd = [] #transiciones del afd de cada set de estados del afn
        trans_afd_mark = [] #marcadores de las transiciones del afd de cada set de estados del afn
        for token in range(len(alfabeto)): #0, 1 ~ a, b
            m = move(afn_states[afnS],token,afn_tran_table)
            d_tran = epsilon_closure(m,afn_tran_table)
            trans_afd.append(d_tran)

            # revisamos si el conjunto de estados ya existe en afn_states
            exist = False
            for x in range(len(afn_states)):
                if(d_tran == afn_states[x]):
                    exist = True
                    #trans_afd_mark.append(str(x+1)) # +1 debido a que abajo se hace append luego de agregar un elemento lo que hace 1 posicion mas largo el arreglo
                    trans_afd_mark.append(get_key(x+1))

            # si no existe entonces agregaremos un nuevo set de estados
            if(exist == False):
                '''#revisamos si tiene el estado de aceptacion para detener el ciclo
                print('d_tran last: '+str(d_tran[len(d_tran)-1])+' aceptacion: '+str(afn_tran_table[0][len(afn_tran_table[0])-1]))
                if(str(d_tran[len(d_tran)-1]) == str(afn_tran_table[0][len(afn_tran_table[0])-1])): 
                    print('aceptacion al extremo')
                    estadoAceptacion.append(str(afn_tran_table[0][len(afn_tran_table[0])-1]))
                    afn_states.append(d_tran)
                    appends += 1
                    trans_afd_mark.append(str(len(afn_states))) #marcas estados de transicion afd
                #sino contiene el estado de aceptacion continuar
                else:'''
                print(str(afnS)+' = '+str(d_tran))
                afn_states.append(d_tran) 
                appends += 1
                #trans_afd_mark.append(str(len(afn_states)))  #marcas estados de transicion afd
                trans_afd_mark.append(get_key(len(afn_states)))
        trans_afds.append(trans_afd)
        trans_afd_marks.append(trans_afd_mark)
        afnS += 1

    print('trans afd: '+ str(trans_afds))
    print('trans afd marks: '+ str(trans_afd_marks))

    afd_trans_table = []
    afn_states.insert(0,'AFN')
    afd_trans_table.append(afn_states)

    afd_states = []
    for i in range(1,len(afn_states)):
        #afd_states.append(str(i))
        afd_states.append(get_key(i))
    afd_states.insert(0,'AFD')
    afd_trans_table.append(afd_states)

    alfabet_cols = []
    for token in range(len(alfabeto)):
        alfabet_col = []
        for i in range(len(trans_afd_marks)):
            alfabet_col.append(trans_afd_marks[i][token])
        alfabet_col.insert(0,alfabeto[token])
        afd_trans_table.append(alfabet_col)
        alfabet_cols.append(alfabet_col)

    transAFD = []
    for i in range(1,len(afd_states)):
        trans = ''
        for token in range(len(alfabeto)):
            afdState = str(afd_states[i])
            tr = str(alfabet_cols[token][0])
            alfaState = str(alfabet_cols[token][i])
            trans = afdState + ', '+ tr + ', ' + alfaState
            transAFD.append(trans)
    print('transiciones: '+str(transAFD))

    # to text
    my_file = os.path.join(THIS_FOLDER, OUTPUTFILENAMES[1])
    f = open(my_file, "w")
    f.write(str(afd_trans_table)+'\n')
    f.close()

    my_file = os.path.join(THIS_FOLDER, OUTPUTFILENAMES[0])
    f = open(my_file, "w")
    afd_states.pop(0)
    f.write('estados = '+str(afd_states)+'\n')
    f.write('alfabeto = '+str(alfabeto)+'\n')
    f.write('inicial = '+str(estadoInicial)+'\n')
    f.write('aceptacion = '+str(estadoAceptacion)+'\n')
    f.write('transiciones = '+str(transAFD)+'\n')
    f.close()

    return afd_trans_table

def to_file(afd_tran_table,txtFile=OUTPUTFILENAMES[1]):
    '''
    Funcion que convierte el arreglo con la tabla de transiciones en arreglos del afd a un txt
    '''

    my_file = os.path.join(THIS_FOLDER, txtFile)
    f = open(my_file, "w")
    f.write(str(afd_tran_table))
    f.close()

    #!NOTA: numero de columnas es variable por alfabeto, esto on funcionara en este caso
    with open(OUTPUTFILENAMES[1], 'w',newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        afnStates = afd_tran_table[0]
        afdStates = afd_tran_table[1]
        a = afd_tran_table[2]
        b = afd_tran_table[3]
        var =''
        for i in range(len(afnStates)):
            filewriter.writerow([afnStates[i],afdStates[i],a[i],b[i]])
    

# Main______________________________________________
def main():
    file=''
    afn_tran_table = []

    #file = str(sys.argv[1])
    file = INPUTFILENAME
    afn_tran_table, alfabeto = transition_afn_table(file)
    print(file)
    print('tabla: '+str(afn_tran_table))
    print('alfabeto: '+str(alfabeto))

    afd_tran_table = convertion_from_afn_to_afd(afn_tran_table,alfabeto)
    print('afd table: ')
    print(str(afd_tran_table))


#Main ________________________
if __name__ == "__main__":
    main()
    #python afn_to_afd.py afn-tran-table.csv
