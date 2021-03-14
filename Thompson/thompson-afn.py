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
            break
    #eliminamos el nodo inicial del grafo B ya que este sera reemplazado por el nodo final del grafo A
    for i in range(len(graphB)):
        node = graphB[i]
        if(node.isInitial()):
            gb_node_init = node #se almacena nodo eliminado 
            graphB.pop(i) #graphB = [nodei,nodef] --> [nodef]
            break
    #se recorren las relaciones del nodo eliminado en el grafo B y se copian al nodo final del grafo A
    for i in range(len(gb_node_init.getRelations())):
        relation = gb_node_init.getRelations()[i]
        #se obvia el valor viejo de salida de la relacion Ej. (viejo,b,B) --> (nuevo,b,B)
        relation = graphA[ga_node_final_pos].getValue()+relation[1:] 
        graphA[ga_node_final_pos].setRelation(relation)

    val = int(graphA[ga_node_final_pos].getValue())
    #renumeracion de los nodos del grafo B a partir del valor del nodo final del grafo A
    for i in range(len(graphB)):
        val = val + 1 
        node = graphB[i] 
        node.setValue(str(val))
        





def or_afn(postfix):

    result = []

    return result

def kleene_afn():
    result = []

    return result

def tests():
    chil = 5
    return chil





