######################################################
# Diego Sevilla
# 17238
######################################################
# Cocol.py
######################################################

#imports
import os
import sys
sys.path.append(".")
from os.path import basename
from functions import functions


#Clase de implementacion_________________________________________________
class Cocor:
    """Clase con definiciones varias de COCO/R
    """
    # Constructor de las variables
    def __init__(self):

        #definicion patrones base del vocabulario   
        '''self.vocabulary = {
            'ident' : "letter{letter|digit}.",
            'number': "digit{digit}.",
            'string': "'"' {anyButQuote} '"'.",
            'char'  : "'\'' anyButApostrophe '\''."
        }'''

        self.keywords = {
            # conditionals, iterators
            "if":"if",
            "elif":"elif",
            "else":"else",
            "while":"while",
            "for":"for", 
            # jumps, interuptions
            "assert":"assert",
            "break":"break",
            "continue":"continue",
            "except":"except",
            "raise":"raise",
            "finally":"finally",
            "pass":"pass",
            "with":"with", 
            #shot keywords
            "as":"as",
            "in":"in",
            "is":"is", 
            #logical operators
            "and":"and",
            "or":"or",
            "not":"not", 
            #bools and None
            "False":"False", 
            "True":"True", 
            "None":"None", 
            #funcions and classes
            "class":"class",
            "def":"def",
            "del":"del",
            "from":"from",
            "global":"global",
            "nonlocal":"nonlocal",
            "import":"import",
            "return":"return",
            #lambdas
            "lambda":"lambda",
            "yield":"yield",
        }

        self.charactersInFile = {}
        self.keyWordsInFile = {}
        self.tokensInFile = {}
        #self.productionsInFile = {}

        self.test_patterns = []

        self.functions = functions()


    def read_def_cfg(self,file='def_file.cfg'):
        here = os.path.dirname(os.path.abspath(__file__))
        file_ = file
        filepath = os.path.join(here, file_)
        header = ''

        with open(filepath,'r') as fp:
            line = fp.readline()
            cnt = 1
            while line:
                line = line.rstrip()
                if not(line.startswith('(.')) and len(line) > 0:
                    
                    if(line.startswith('CHARACTERS')):
                        header = 'CHARACTERS'
                    elif(line.startswith('KEYWORDS')):
                        header = 'KEYWORDS'
                    elif(line.startswith('TOKENS')):
                        header = 'TOKENS'
                    #elif(line.startswith('PRODUCTIONS')):
                    #    header = 'PRODUCTIONS'

                    if('=' in line):
                        
                        arr_ = line.split('=')
                        arr_[0] = arr_[0].replace(' ','')
                        #arr_[1] = arr_[1].replace(' ','')
                        arr_[1] = arr_[1].replace('.','')
                        if(header == 'CHARACTERS'):
                            self.charactersInFile[arr_[0]] = arr_[1]
                        elif(header == 'KEYWORDS'):
                            self.keyWordsInFile[arr_[0]] = arr_[1]
                        elif(header == 'TOKENS'):
                            self.tokensInFile[arr_[0]] = arr_[1]
                        #if(header == 'PRODUCTIONS'):
                        #   self.productionsInFile[arr_[0]] = arr_[1]

                #print("Line {}: {}".format(cnt, line.strip()))
                line = fp.readline()
                cnt += 1

    def read_test_file(self,file='test_file.cfg'):
        here = os.path.dirname(os.path.abspath(__file__))
        file_ = file
        filepath = os.path.join(here, file_)
        with open(filepath,'r') as fp:
            line = fp.readline()
            while line:
                line = line.rstrip()
                for i in line.split(' '):
                    if len(i) > 0:
                        self.test_patterns.append(i)
                line = fp.readline()
                


    def fileContents(self):
        print(self.charactersInFile)
        print(self.keyWordsInFile)
        print(self.tokensInFile)
        
        print(self.test_patterns)

    def parser(self):
        
        return 0






#tests__________
def main():
    obj = Cocor()
    obj.read_def_cfg()
    obj.read_test_file()
    obj.fileContents()

if __name__ == "__main__":
    main()




