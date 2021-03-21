######################################################
# Diego Sevilla
# 17238
######################################################
# AFNT.py
######################################################

# imports _________________________
import time
import collections
from functions import *
from graphs.NodeT import *
from graphs.RelationT import RelationT
import sys
sys.path.append(".")
from graphviz import Digraph


class AFNT:
    '''
    Clase que comvierte una expresion regular en formato postfix a un automara finito no determinista.
    '''

    def __init__(self, tokens, chain):
        self.initString = ''
        #self.funciones = functions()
        self.stack = []
        self.top = -1

        # graphviz

        self.initNode = 0
        self.acceptNode = 0
        self.currentNode = 1

        self.AFNArray = []
        self.AFNResult = {}
        self.chain = chain
        self.alphabet = tokens

    def pop(self):
        if (self.pop == -1):
            return
        else:
            self.top -= 1
            return self.stack.pop()

    def push(self, i):
        self.top += 1
        self.stack.append(i)

    def postFixParser(self,expresion):
        for i in expresion:
            # si el iterador es un token
            if(i in "".join(self.alphabet)):
                self.token_afn()
            # si el iterador apunta a un operador
            elif(i in ".|*"):
                if(i == "."):
                    self.concat_afn()
                elif(i == "|"):
                    self.or_afn()
                elif(i == "*"):
                    self.kleene_afn()

        afnArrEnd = self.AFNArray.pop()
        self.AFNSim(afnArrEnd)
        self.drawGraph(afnArrEnd)
        return afnArrEnd

    def token_afn(self,a):
        '''
        Funcion para generar el par de nodos correspondientes.
        Ej. (Ni) --a--> (Nf)

        Parametros:
        - a - token cualquiera del alfabeto en cuestion que servira como transicion entre ambos nodos
        - return - un grafo pequeño compuesto por dos nodos
        '''
        #se crea un grafo local
        localGraph = {}
        counter = 0

        #Nodo inicial y final
        node1 = NodeT(isInitial=True)
        node2 = NodeT(isAccepting=True)

        # Relacion: origen ---a---> Destino
        relation = RelationT(counter,a,counter+1)
        node1.addRelation(relation)

        #estos nodos se agregan al grafo local
        localGraph[counter] = node1
        localGraph[counter+1] = node2

        #colocamos este grafo local en el AFN global
        self.AFNArray.append(localGraph)

        self.acceptNode = self.currentNode
        #Se suma 2 al valor del nodo en cuestion ya que se agregaron 2 nodos
        self.currentNode += 2

    def concat_afn(self):
        '''
        Funcion para concatenar 2 grafos cualesquiera. 
            Ej. (Gi) --a--> (Nu) --b--> (Gf)
        - El nodo final de Gi se convierte en el nodo inicial de Gf.

        Esta funcion no recibe parametros ya que concatenara dos grafos o 
        AFNs que se encuentren en el array global de afns (AFNArray).
        '''
        # se crea un grafo local
        localGraph = {}
        #Este contador actualiza los estados de los nodos
        counter = -1

        #obtenemos los grafos a concatenar
        graph1 = self.AFNArray.pop()
        graph2 = self.AFNArray.pop()

        #Se actualizan los estados de cada nodo del grafo1
        afnCounter1, newAFN1 = updateNodesId(counter,graph1)
        #se obtiene el id del nodo de aceptacion del nuevo grafo o afn
        id_fnode_graph1, newAFN1 = getAcceptingNodeId(newAFN1)

        #se obtiene el id final del nodo del grafo 1 y se actualiza
        
        #actualizamos los estados del afn2
        afnCounter2, newAFN2 = updateNodesId(afnCounter1-1,graph2)
        id_fnode_graph2, newAFN2 = getInitialNodeId(newAFN2)

        counter = afnCounter2

        localGraph.update(newAFN1)
        localGraph.update(newAFN2)

        #colocamos el resultado de la concatenacion en el array de afns
        self.AFNArray.append(localGraph)

        return 0

    def or_afn(self):
        '''
        Funcion para operar | entre dos grafos cualesquiera. 

        Esta funcion no recibe parametros ya que operara Or con dos grafos o 
        AFNs que se encuentren en el array global de afns (AFNArray).
        '''
        #El grafo que contendra el resultado
        orGraph = {}
        #Este contador actualiza los estados de los nodos
        counter = -1

        #obtenemos los grafos a concatenar
        graph1 = self.AFNArray.pop()
        graph2 = self.AFNArray.pop()


        # Se crea el nodo inicial del grafo OR --------------------------
        i_node = NodeT(isInitial=True)
        #colocameos el nodo incial al principio del grafo de resultado or
        orGraph[counter] = i_node

        #                                       < Construccion y actualizacion de estados >

        #Actualizamos estados del grafo 1
        afnCounter1, newAFN1 = updateNodesId(counter,graph1)
        #obtenemos nodos inicial y final del grafo 1
        id_inode_graph1, newAFN1 = getInitialNodeId(newAFN1)
        id_fnode_graph1, newAFN1 = getInitialNodeId(newAFN1)

        #Actualizamos estados del grafo 2
        afnCounter2, newAFN2 = updateNodesId(afnCounter1,graph2)
        #obtenemos nodos inicial y final del grafo 2
        id_inode_graph2, newAFN2 = getInitialNodeId(newAFN2)
        id_fnode_graph2, newAFN2 = getAcceptingNodeId(newAFN2)

        #Ingresamos los grafos actualizados al grafo que contendra el resultado de la operacion OR
        orGraph.update(newAFN1)
        orGraph.update(newAFN2)

        #se crea el nodo final del grafo OR --------------------------------
        f_node = NodeT(isAccepting=True)

        # relacion del nodo inicial de OR hacia el nodo inicial del grafo 1 a travez de epsilon
        i_node_rel_to_AFN1 = RelationT(counter,'ε',id_inode_graph1)
        # relacion del nodo inicial de OR hacia el nodo inicial del grafo 2 a travez de epsilon
        i_node_rel_to_AFN2 = RelationT(counter,'ε',id_inode_graph2)

        #se agregan las relaciones al nodo inicial del grafo OR
        orGraph[counter].addRelation(i_node_rel_to_AFN1)
        orGraph[counter].addRelation(i_node_rel_to_AFN2)
        counter = afnCounter2+1

        # relacion del nodo inicial de OR hacia el nodo inicial del grafo 1
        AFN1_to_f_node_OR = RelationT(id_fnode_graph1,'ε',counter)
        # relacion del nodo inicial de OR hacia el nodo inicial del grafo 2
        AFN2_to_f_node_OR = RelationT(id_fnode_graph2,'ε',counter)

        #relacionamos el ultimo nodo del grafo 1 al ultimo nodo del grafo OR con epsilon
        orGraph[afnCounter1].addRelation(AFN1_to_f_node_OR)
        #relacionamos el ultimo nodo del grafo 2 al ultimo nodo del grafo OR con epsilon
        orGraph[afnCounter2].addRelation(AFN2_to_f_node_OR)

        #agregamos el nodo final
        orGraph[counter] = f_node

        #colocamos el grafo de resultado en el array de afns global
        self.AFNArray.append(orGraph)


    def kleene_afn(self):
    
        return 0



    def drawGraph(self,afn):
        file_name = 'graphs-output/'+'test1'
        dot = Digraph(comment='Test 1',filename=file_name,format='png', engine='sfdp')
        dot.attr(size='8,5')
        dot.attr('node', shape='circle')
        dot.attr('node',style='filled',color='lightgrey')

        nodes = afn
        for i in nodes:
            node = nodes.get(i)
            print(node.getIsAccepting())
            print(node.getRelations())
            if(node.getIsAccepting()):
                dot.attr('node', shape='doublecircle')
                val = str(list(nodes.keys())[i])
            else:
                val = str(list(nodes.keys())[i])
            dot.node(val, val)
            if(len(node.getRelations()) > 1):
                for e in range(len(node.getRelations())):
                    rel = node.getSpecificRelation(e)
                    dot.edge(val, rel.getDestiny(),label=rel.getToken())
            elif(len(node.getRelations()) == 1):
                rel = node.getSpecificRelation(0)
                print('origin,token,destiny')
                print(rel.getOrigin(),rel.getToken(),rel.getDestiny())
                dot.edge(val, rel.getDestiny(),label=rel.getToken())

        dot.attr(label=r'\n'+self.name,fontsize='10')
        #dot.unflatten(stagger=3)
        # dot.render('test-output/test3.gv', view=True)
        dot.render(view=True)
        #dot.view()

    
