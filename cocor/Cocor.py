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

        self.tokensConvertionInFile = {}

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
                        arr_[1] = arr_[1][:-1]
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
        self.cocorToP1Convention()
        print(self.tokensConvertionInFile)
        
        print(self.test_patterns)


    def intoBraces(self,token_def,c,expArray):
        word_set = ['(']
        c += 1
        currentChar = (token_def[c])
        while (c < len(token_def) and (token_def[c].isalpha() or token_def[c] in "|}{'\"") ):
            if token_def[c] == '}':
                word_set.append(')*')
                c += 1
                expArray.append(''.join(word_set))
                break
            elif token_def[c] == '{':
                expArray, c = self.intoBraces(token_def,c,expArray)
            else:
                word_set.append(token_def[c])
                c += 1
        return expArray,c

    def intoBrackets(self,token_def,c,expArray):
        word_set = ['(']
        expArray.append('(')
        c += 1
        currentChar = (token_def[c])
        while (c < len(token_def) and (token_def[c].isalpha() or token_def[c] in "|][}{'\"") ):
            currentChar = (token_def[c])
            if token_def[c] == ']':
                word_set.append(')?')
                openp = 0
                closep = 0
                for b in expArray:
                    if(')?' in b):
                        closep +=1
                    elif(b == '('):
                        openp += 1

                if(''.join(word_set) == "()?" and (closep != openp-1)):
                    exp = expArray.pop()
                    exp = exp + ')?'
                    expArray.append(exp)
                elif(''.join(word_set) == "()?" and (closep == openp-1)):
                    expArray.append(')?')
                else: 
                    expArray.append(''.join(word_set))
                c += 1
                break
            elif token_def[c] == '[':
                expArray, c = self.intoBrackets(token_def,c,expArray)
            elif token_def[c] == '{':
                expArray, c = self.intoBraces(token_def,c,expArray)
            elif token_def[c] in "'\"":
                expArray, c = self.intoQuotationsApostrophes(token_def,c,expArray)
            elif token_def[c].isalpha():
                expArray, c = self.alphaNumericIterator(token_def,c,expArray)
            else:
                word_set.append(token_def[c])
                c += 1
        return expArray,c

    def intoParenthesis(self,token_def,c,expArray):
        word_set = ['(']
        c += 1
        currentChar = (token_def[c])
        while (c < len(token_def) and (token_def[c].isalpha() or token_def[c] in "|)('\"") ):
            currentChar = (token_def[c])
            if token_def[c] == ')':
                word_set.append(token_def[c])
                c += 1
                expArray.append(''.join(word_set))
                break
            elif token_def[c] == '(':
                expArray, c = self.intoParenthesis(token_def,c,expArray)
            else:
                word_set.append(token_def[c])
                c += 1
        return expArray,c

    def intoQuotationsApostrophes(self,token_def,c,expArray):
        if token_def[c] == '"':
            q = '"'
        elif token_def[c] == "'":
            q = "'"
        word_set = []
        c += 1
        word_set.append(q)
        while c < len(token_def):
            if token_def[c+1] == "|":
                if token_def[c+2] in "'\"":
                    word_set.append(token_def[c]) #se inserta el '
                    word_set.append(token_def[c+1]) #se inserta el |
                    word_set.append(token_def[c+2]) #se inserta el proximo '
                    c += 3
                else:
                    word_set.append(token_def[c])
                    c += 1
                #continue
            elif token_def[c] == q:
                word_set.append(token_def[c])
                c += 1
                break
            else:
                word_set.append(token_def[c])
                c += 1
        expArray.append(''.join(word_set))
        return expArray, c 

    def alphaNumericIterator(self,token_def,c,expArray):
        word_set = []
        while (c < len(token_def) and (token_def[c].isalpha() or token_def[c] == "|")):
            word_set.append(token_def[c])
            c += 1
        word = ''.join(word_set)
        if (word == 'EXCEPT' or word == 'KEYWORDS'):
            word_set.insert(0,' ') 
        expArray.append(''.join(word_set))
        return expArray, c


    def cocorToP1Convention(self):
        """funcion para hacer conversions como: 

        - kleene closure
            - digit{digit} = digit digit *
            - {} = * (0 o mas)  -->  r*

        - positive closure
            - [digit] = digit? = digit|e
            - [] = ? (cero o una instancia)  -->  r? = r|e
        """
        closures = []
        expArray = []
        for key, token_def in self.tokensInFile.items():
            c = 0
            while c < len(token_def):
                currentChar = token_def[c]
                if token_def[c] == " ":
                    c += 1
                    continue
                elif(token_def[c] == "{"):
                    expArray, c = self.intoBraces(token_def,c,expArray)
                elif(token_def[c] == "("):
                    expArray, c = self.intoParenthesis(token_def,c,expArray)
                elif(token_def[c] == "["):
                    expArray, c = self.intoBrackets(token_def,c,expArray)
                elif(token_def[c].isalpha() or c == '|'):
                    expArray, c = self.alphaNumericIterator(token_def,c,expArray)
                    #c -= 1
                elif(token_def[c] in "'\""):
                    expArray, c = self.intoQuotationsApostrophes(token_def,c,expArray)
                    #c -= 1
                elif(token_def[c] in "})]"):
                    print('Revisar cerraduras de apertura en la expresion')
                else:
                    l = 0

                #c -= 1

            self.tokensConvertionInFile[key] = ''.join(expArray)
            expArray = []

        return 0

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



