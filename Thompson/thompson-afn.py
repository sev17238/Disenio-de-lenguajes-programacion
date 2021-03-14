######################################################
# Diego Sevilla
# 17238
######################################################
# afn_to_afd.py
######################################################
# Python3 programa que recibe una entrada.
# 1. RegEx: Expresion regular postfix.
######################################################

# imports _________________________
import sys
sys.path.append(".")
from graphs.Node import Node
from graphs.Graph import Graph

#constants _________________________
node_init_name = '0'
node_accept_name = '1'

#Functions _________________________

def token_afn(a):
    '''
    Funcion para generar el par de nodos correspondientes.
    Ej. (Ni) --a--> (Nf)

    Parametros:
     - a - token cualquiera del alfabeto en cuestion que servira como transicion entre ambos nodos
    '''
    relation = node_init_name+','+a+','+node_accept_name
    node1 = Node(value=node_init_name,relations=[relation],isInitial=True)
    node2 = Node(value=node_accept_name,isAccepting=True)
    nodes = [node1,node2]
    return nodes

def concat_afn(A,B,i):
    '''
    Funcion para concatenar caracteres. 
        Ej. (Gi) --a--> (Nu) --b--> (Gf)
    - Nodo de union entre ambos grafos. Es el final de Gi y el inicial de Gf.

    Parametros:
     - A, B - arreglos conteniendo los nodos de un grafo cualguiera. Estos grafos se concatenaran.
     - i - el valor del nodo intermedio
    '''
    graphA = A
    graphB = B
    ga_node_final_pos = 0
    ga_node_final_value = ''
    gb_node_init = None
    #encontramos el nodo final del grafo A que se convertira en el nodo inicial del grafo B
    for i in range(len(graphA)):
        node = graphA[i]
        if(node.isAccepting()):
            ga_node_final_pos = i
            node.isAccepting(False)
            break
    #eliminamos el nodo inicial del grafo B ya que este sera reemplazado por el nodo final del grafo A
    for i in range(len(graphB)):
        node = graphB[i]
        if(node.isInitial()):
            gb_node_init = node #se almacena nodo eliminado 
            graphB.pop(i) #graphB = [nodei,nodef] --> [nodef]
        graphA.append(node)
    
    #grafo con las relaciones de ambos grafos A y B
    #NOTA: se deben actualizar relaciones y enumerar de nuevo a los nodos del grafo B
    graphAB = graphA 
    
    #nodo final del grafo A
    ga_final_node = graphAB[ga_node_final_pos]

    #se recorren las relaciones del nodo eliminado en el grafo B y se copian al nodo final del grafo A
    for i in range(len(gb_node_init.getRelations())):
        '''if(len(gb_node_init.getRelations())>1):'''
        relation = gb_node_init.getRelations()[i]
        #valor viejo de destino de la transicion
        old_d = int(relation[2])
        
        #se crea una nueva relacion reemplazando el valor de destino y copiando la transicion. Ej. (b,old_d) --> (b,new_d)
        #y se suman el valor del nodo final y el valor viejo de la relacion para actualizar correctamente la relacion
        relation = relation[0:1]+str(int(ga_final_node.getValue())+old_d) 

        #se agrega la relacion
        ga_final_node.setRelation(relation)
        '''else:
            relation = gb_node_init.getRelations()[i]
            #se crea una nueva relacion reemplazando el valor de destino y copiando la transicion. Ej. (b,old_d) --> (b,new_d)
            relation = relation[0:1]+str((int(ga_final_node.getValue())+1))
            ga_final_node.setRelation(relation)'''

    val = int(ga_final_node.getValue())
    old_val = ''
    #enumeracion de los nodos del grafo B a partir del valor del nodo final del grafo A
    #NOTA: se deben actualizar las relaciones entre nodos con estos nuevos valores
    for i in range(ga_node_final_pos+1,len(graphAB)): #+1 porque queremos el nodo que viene luego del nodo final del grafo A
        val = val + 1 
        node = graphB[i] 
        old_val = node.getValue()
        node.setValue(str(val)) 

        for e in range(i+1,len(graphAB)): #+1 porque queremos ver si los nodos siguientes se conectan con este nodo
            node_n = graphAB(e)
            if(len(node_n.getRelations()) > 0):
                for r in range(len(node_n.getRelations())):
                    rel = node.getRelations()[r]
                    if(rel[2] == old_val): #si este nodo tiene de destino al nodo que se le acaba de cambiar el valor
                        node.modifyDestinyRelation(r,str(val)) #se reemplaza el valor de destino de la relacion








def or_afn(postfix):

    result = []

    return result

def kleene_afn():
    result = []

    return result

def tests():
    chil = 5
    return chil





