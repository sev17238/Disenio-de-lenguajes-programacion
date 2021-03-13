######################################################
# Diego Sevilla
# 17238
######################################################
# Graph.py
######################################################
# Clase que genera la representacion de un grafo.
######################################################

from graphviz import Digraph
import sys
sys.path.append(".")
from graphs.Node import Node

class Graph:
    '''
    Clase para construir un grafo y dibujarlo

    Atributos:
     - name = nombre del grafo
     - nodes = arreglo de nodos de la clase Node(). 
    '''
    def __init__(self,name,nodes):
        self.name = name
        self.nodes = nodes

    #gets
    def getName(self):
        return self.name

    def getNodes(self):
        return self.nodes

    #sets
    def setName(self,name):
        self.name = name

    #others
    def drawGraph(self):
        file_name = 'graphs-output/'+self.name
        dot = Digraph(comment='Test 1',filename=file_name,
        node_attr={'color': 'lightblue1', 'style': 'filled'})
        #dot.attr('node',style='filled',color='lightgrey')

        nodes = self.nodes
        for i in range(len(nodes)):
            node = nodes[i]
            val = node.getValue()
            dot.node(val, val)
            if(len(node.getRelations()) > 1):
                for e in range(len(node.getRelations())):
                    rel = node.getRelations()[e]
                    dot.edge(val, rel[4],label=rel[2])
            elif(len(node.getRelations()) == 1):
                rel = node.getRelations()[0]
                dot.edge(val, rel[4],label=rel[2])
            else: 
                continue
        
        dot.attr(label=r'\nDiego Sevilla\n17238',fontsize='10')
        #dot.render('test-output/test3.gv', view=True)
        dot.view()


# Main________________________________________________
def main(): 
    nodeA = Node('A',['A,b,D','A,a,C']) 
    nodeB = Node('B',['B,a,C','B,b,A']) 
    nodeC = Node('C',['C,b,D','C,a,B']) 
    nodeD = Node('D') 
    arr = [nodeA,nodeB,nodeC,nodeD]

    graph = Graph('g1',arr)

    graph.drawGraph()

if __name__ == "__main__":
    main()
