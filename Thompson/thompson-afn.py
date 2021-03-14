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

    #relation1 = node_init_name+','+a+','+str(i)
    #relation2 = str(i)+','+b+','+node_accept_name
    #node1 = Node(value=node_init_name,relations=[relation1],isInitial=True)
    #node2 = Node(value=str(i),relations=[relation2])
    #node3 = Node(value=node_accept_name,isAccepting=True)
    #nodes = [node1,node2,node3]
    #return nodes

def or_afn(postfix):

    result = []

    return result

def kleene_afn():
    result = []

    return result

def tests():
    chil = 5
    return chil





