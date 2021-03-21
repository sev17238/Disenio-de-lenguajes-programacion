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
from graphs.NodeT import NodeT
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
        localGraph = {}
        counter = 0

        # Relacion: origen ---a---> Destino
        relation = RelationT(str(counter),a,str(counter+1))
        #Nodo inicial y final
        node1 = NodeT(isInitial=True,relation=[relation])
        node2 = NodeT(isAccepting=True)

        localGraph[counter] = node1
        localGraph[counter+1] = node2

        self.AFNArray.append(localGraph)

        self.acceptNode = self.currentNode
        self.currentNode += 2

    def or_afn(self):

        return 0

    def kleene_afn(self):
    
        return 0

    def concat_afn(self):
        
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

    
