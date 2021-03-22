######################################################
# Diego Sevilla
# 17238
######################################################
# Graph.py
######################################################
# Clase que genera la representacion grafica de un 
# grafo.
######################################################

from graphviz import Digraph
import sys
sys.path.append(".")
from graphs.Node import Node

class GraphGUI:
    '''
    Clase para construir un grafo y dibujarlo

    Atributos:
     - name = nombre del grafo
     - nodes = diccionario de nodos de tipo Node(). 
    '''
    def __init__(self,name,nodes):
        self.name = name
        self.nodes = nodes
        self.graph = Digraph(comment='Test 1',format='png', engine='sfdp')

    #others
    def drawGraph(self):
        file_name = 'graphs-output/'+self.name
        dot = Digraph(comment='Test 1',filename=file_name,format='png', engine='sfdp')
        dot.attr(size='8,5')
        dot.attr('node', shape='circle')
        dot.attr('node',style='filled',color='lightgrey')

        nodes = self.nodes
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


# Main________________________________________________
def main(): 
    '''nodeA = Node('A',['b,D','a,C']) 
    nodeB = Node('B',['a,C','b,A']) 
    nodeC = Node('C',['b,D','a,B']) 
    nodeD = Node('D') 
    arr = [nodeA,nodeB,nodeC,nodeD]

    graph = GraphGUI('g1',arr)

    graph.drawGraph()'''

if __name__ == "__main__":
    main()
