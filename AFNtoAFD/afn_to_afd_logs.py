def transition_afn_table(csvfile='afn-tran-table.csv'):
    #print(df.to_string()) # table
    #print(len(df))        #number of rows
    #print(df.values[0])   #each row
    #print(df.values[1]) 
    #print(df.values[2]) 
    #print(df.values[3]) 
    #print(df.values[4]) 
    return 0

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

    return 0


