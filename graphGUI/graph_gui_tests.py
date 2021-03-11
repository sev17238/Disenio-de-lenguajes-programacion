######################################################
# Diego Sevilla
# 17238
######################################################
# graph_gui_tests.py
######################################################
# Programa para pruebas dibujando grafos.
######################################################
#Imports______________________________________________
#!/usr/bin/python
import sys
import os
#os.system("xdg-open "+ <string>)
#import subprocess

#import gv
from graphviz import Digraph

#Functions____________________________________________


# Main________________________________________________
def main(): 

    dot = Digraph(comment='Shiet Happens')

    dot.node('A', 'A')
    dot.node('B', 'B')
    dot.node('C', 'C')
    #dot.edges(['AB', 'AL'])
    dot.edge('B', 'C', constraint='false',label='a')
    dot.edge('A', 'B', constraint='false',label='b')
    dot.edge('A', 'C', constraint='false',label='b')

    print(dot.source)
    dot.render('test-output/round-table.gv', view=True)



#Main ________________________
if __name__ == "__main__":
    main()
    #python afn_to_afd.py afn-tran-table.csv