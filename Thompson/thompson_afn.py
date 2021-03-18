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
from graphs.Relation import Relation
import collections

#constants _________________________

#Functions _________________________

def token_afn(a):
    '''
    Funcion para generar el par de nodos correspondientes.
    Ej. (Ni) --a--> (Nf)

    Parametros:
     - a - token cualquiera del alfabeto en cuestion que servira como transicion entre ambos nodos
     - return - un grafo pequeño compuesto por dos nodos
    '''
    relation = Relation('0',a,'1')
    node1 = Node(relations=[relation],isInitial=True)
    node2 = Node(isAccepting=True)
    nodes = {0:node1,1:node2}
    return nodes

def updateNodeRelations(graphAB,lengthA):
    '''
    
    '''
    i = lengthA-1 #contador que empieza a partir del nodo final del grafo A. Puede empezar a partir de cualquier numero
    counter = 1 #contador para valores antiguo de 
    #for i in range(len(graphAB)-1,len(graphB)):
    while(i < len(graphAB)):
        node = graphAB.get(i)

        if(len(node.getRelations()) > 0):
            for e in range(len(node.getRelations())):
                rel = node.getSpecificRelation(e)
                
                if(rel.getDestiny() == str(counter+1)):
                    rel.setOrigin(str(i))
                    rel.setDestiny(str(i+1))
                elif(rel.getDestiny() == str(counter)): # cuando suceda que (N0 --> N1 --> N1 --> Nn)
                    rel.setOrigin(str(i))
                    rel.setDestiny(str(i+1))
                elif(int(rel.getDestiny()) < (counter+1)):
                    # en una cerradura kleene es posible que algunas relaciones se dirijan hacia nodos anteriores y no al siguiente
                    # nodo del grafo. Por esa razon se resta el viejo origen y el viejo destino para obtener la distancia hacia
                    # ese nodo anterior. Esa distancia se restara de i, el contador a partir del ultimmo nodo de graphAB para 
                    # obtener el nuevo destino de la relacion en question.

                    #!old_temp_origin = rel.getOrigin()
                    old_temp_origin = counter
                    old_temp_destiny = int(rel.getDestiny())
                    new_destiny_substraction = old_temp_origin - old_temp_destiny
                    new_destiny = i - new_destiny_substraction

                    #!pueden haber errores por no usar counter
                    rel.setOrigin(str(i))
                    rel.setDestiny(new_destiny)
                elif(int(rel.getDestiny()) > (counter+1)):
                    # la misma logica para el caso en el que en una cerradura kleene la relacion 
                    old_temp_origin = counter
                    old_temp_destiny = int(rel.getDestiny())
                    new_destiny_addition = old_temp_destiny - old_temp_origin
                    new_destiny = i + new_destiny_addition


        #graphAB.update({i:graphB[counter]})
        i += 1
        counter += 1

    return graphAB

def concat_afn(A={0:Node()},B={0:Node()}):
    '''
    Funcion para concatenar 2 grafos cualesquiera. 
        Ej. (Gi) --a--> (Nu) --b--> (Gf)
    - El nodo final de Gi se convierte en el nodo inicial de Gf.

    Parametros:
     - A, B - diccionarios conteniendo los nodos de un grafo cualguiera. Estos grafos se concatenaran.
    '''
    graphA = A
    graphB = B

    gb_node_init = graphB.get(0)
    gb_node_init.setIsInitial(False)

    #se copian atributos del grafo inicial de B, y se pegan al grafo final de A
    relations_,isInit_,isAccept_ = gb_node_init.copyNodeAtributes() 
    graphA[len(graphA)-1].pasteNodeAtributes(relations_,isInit_,isAccept_) 

    #se elimina el nodo inicial del grafo A
    graphB.pop(0)
    key_ = len(graphA)
    lenA = len(graphA)
    #grafos se unen
    for i in range(0,len(graphB)):
        graphA.update({key_:graphB.get(i+1)})
        key_ += 1

    print('graphAB: '+str(graphA))

    #graphA_ = collections.OrderedDict(sorted(graphA.items()))

    graphAB = {}
    graphAB = updateNodeRelations(graphA,lenA)

    #grafo con los nodos del grafo A y B
    return graphAB

def or_afn(A,B):
    '''
    Funcion para operar | entre dos grafos cualesquiera. 

    Parametros:
     - A, B - arreglos conteniendo los nodos de un grafo cualguiera. Estos grafos operarn con |.
    '''

    graphA = A
    graphB = B

    #los nodos finales e iniciales de los grafos A y B ya no tendran esta etiqueta
    graphA.get(len(graphA)-1).setIsAccepting(False)
    graphA.get(0).setIsInitial(False)
    graphB.get(len(graphB)-1).setIsAccepting(False)
    graphB.get(0).setIsInitial(False)

    #el nodo inicial (aun no se haran las relaciones ε hacia A y B debido a que no se a enumerado)
    node_i = Node(isInitial=True)

    #grafo or que tendra el resultado de la operacion | entre A y B
    graphOr = {}
    #se agrega el nodo inicial al grafo OR
    graphOr.update({0:node_i})

    #almacenamiento del tamaño de ambos grafos A y B
    lenA = len(graphA)
    lenB = len(graphB)

    #unimos grafos A y B entre si
    key_ = len(graphA)
    for i in range(0,len(graphB)):
        graphA.update({key_:graphB.get(i)})
        key_ += 1

    print(graphA)
    #unimos grafos A y B al grafo Or
    key__ = len(graphOr)
    for i in range(0,len(graphA)):
        graphOr.update({key__:graphA.get(i)})
        key__ += 1

    print(graphOr)
    #grafo de resultado
    graphAB = {} 
    #empezaremos en 1, ya que se debe enumerar ambos grafos A y B a partir del nodo inicial del grafo OR con 0
    graphAB = updateNodeRelations(graphOr,1) 

    #relaciones del nodo inicial del grafo OR a los nodos iniciales de los grafos A y B
    relations = [Relation('0','ε',str(list(graphAB.keys())[1])),Relation('0','ε',str(list(graphAB.keys())[lenA+1]))]
    node_i.setRelations(relations)

    #nodo final del grafo con operador OR
    node_f = Node(isAccepting=True)

    lenAB = len(graphAB)
    graphAB.get(lenA).setRelation(Relation(str(lenA),'ε',str(lenAB)))
    graphAB.get(lenA+lenB).setRelation(Relation(str(lenA+lenB),'ε',str(lenAB)))

    graphAB.update({lenAB:node_f})
    return graphAB


def kleene_afn():
    result = []

    return result

def tests():
    chil = 5
    return chil





