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
from infix_postfix_related.InfixRegexToPostfixWords import InfixRegexToPostfixWords

#Clase de implementacion_________________________________________________
class Cocor:
    """Clase con definiciones varias de COCO/R
    """
    # Constructor de las variables
    def __init__(self):

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
        self.tokensConvertionInFile = {}
        self.tokensReadyForPosFix = {}
        self.tokensPosFixInFile = {}
        #self.productionsInFile = {}

        self.test_patterns = []

        self.functions = functions()
        self.objToPostfix = InfixRegexToPostfixWords()

    def getTokens(self):
        return self.tokensConvertionInFile


    def read_def_cfg(self,file='def_file.cfg'):
        """Funcion para leer el archivo con la definicion de tokens
        """
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
        """Funcion para leer el archivo de prueba y almacenar sus contenidos.
        """
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


    def intoBraces(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de { } y retorna el valor de conversion ()*. 
        Puede tener recursion pero se asume que no habran mas {} dentro de la expresion.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        word_set = ['(']
        c += 1
        currentChar = (tokens_exp[c])
        while (c < len(tokens_exp) and (tokens_exp[c].isalpha() or tokens_exp[c] in "|}{'\"") ):
            if tokens_exp[c] == '}':
                word_set.append(')*')
                c += 1
                expArray.append(''.join(word_set))
                break
            elif tokens_exp[c] == '{':
                expArray, c = self.intoBraces(tokens_exp,c,expArray)
            else:
                word_set.append(tokens_exp[c])
                c += 1
        return expArray,c

    def intoBrackets(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de [ ] y retorna el valor. 
        Hay recursion ya que pueden haber mas [ ] dentro.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        word_set = ['(']
        expArray.append('(')
        c += 1
        currentChar = (tokens_exp[c])
        while (c < len(tokens_exp) and (tokens_exp[c].isalpha() or tokens_exp[c] in "|][}{'\"") ):
            currentChar = (tokens_exp[c])
            if tokens_exp[c] == ']':
                word_set.append(')|ε')
                openp = 0
                closep = 0
                for b in expArray:
                    if(')|ε' in b):
                        closep +=1
                    elif(b == '('):
                        openp += 1

                if(''.join(word_set) == "()|ε" and (closep != openp-1)):
                    exp = expArray.pop()
                    exp = exp + ')|ε'
                    expArray.append(exp)
                elif(''.join(word_set) == "()|ε" and (closep == openp-1)):
                    expArray.append(')|ε')
                else: 
                    expArray.append(''.join(word_set))
                c += 1
                break
            elif tokens_exp[c] == '[':
                expArray, c = self.intoBrackets(tokens_exp,c,expArray)
            elif tokens_exp[c] == '{':
                expArray, c = self.intoBraces(tokens_exp,c,expArray)
            elif tokens_exp[c] in "'\"":
                expArray, c = self.intoQuotationsApostrophes(tokens_exp,c,expArray)
            elif tokens_exp[c].isalpha():
                expArray, c = self.alphaNumericIterator(tokens_exp,c,expArray)
            else:
                word_set.append(tokens_exp[c])
                c += 1
        return expArray,c

    def intoParenthesis(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de ( ) y retorna el valor. 
        Hay recursion ya que pueden haber mas ( ) dentro.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        word_set = ['(']
        c += 1
        currentChar = (tokens_exp[c])
        while (c < len(tokens_exp) and (tokens_exp[c].isalpha() or tokens_exp[c] in "|)('\"") ):
            currentChar = (tokens_exp[c])
            if tokens_exp[c] == ')':
                word_set.append(tokens_exp[c])
                c += 1
                expArray.append(''.join(word_set))
                break
            elif tokens_exp[c] == '(':
                expArray, c = self.intoParenthesis(tokens_exp,c,expArray)
            else:
                word_set.append(tokens_exp[c])
                c += 1
        return expArray,c

    def intoQuotationsApostrophes(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de ' ' o " " considerando | dentro y retorna el valor.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        if tokens_exp[c] == '"':
            q = '"'
        elif tokens_exp[c] == "'":
            q = "'"
        word_set = []
        c += 1
        word_set.append(q)
        while c < len(tokens_exp):
            if tokens_exp[c+1] == "|":
                if tokens_exp[c+2] in "'\"":
                    word_set.append(tokens_exp[c]) #se inserta el '
                    word_set.append(tokens_exp[c+1]) #se inserta el |
                    word_set.append(tokens_exp[c+2]) #se inserta el proximo '
                    c += 3
                else:
                    word_set.append(tokens_exp[c])
                    c += 1
                #continue
            elif tokens_exp[c] == q:
                word_set.append(tokens_exp[c])
                c += 1
                break
            else:
                word_set.append(tokens_exp[c])
                c += 1
        expArray.append(''.join(word_set))
        return expArray, c 

    def intoQuotationsApostrophesV2(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de ' ' o " " sin cosidrerar | y retorna el valor.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        if tokens_exp[c] == '"':
            q = '"'
        elif tokens_exp[c] == "'":
            q = "'"
        word_set = []
        c += 1
        word_set.append(q)
        while c < len(tokens_exp):
            if tokens_exp[c] == q:
                word_set.append(tokens_exp[c])
                c += 1
                break
            else:
                word_set.append(tokens_exp[c])
                c += 1
        expArray.append(''.join(word_set))
        return expArray, c 
    
    def alphaNumericIterator(self,tokens_exp,c,expArray,considerOr=True):
        """Recorre una cadena de letras tomando en cuenta | y la retorna.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        word_set = []
        if considerOr:
            while (c < len(tokens_exp) and (tokens_exp[c].isalpha() or tokens_exp[c] == "|")):
                word_set.append(tokens_exp[c])
                c += 1
        else:
            while (c < len(tokens_exp) and tokens_exp[c].isalpha()):
                word_set.append(tokens_exp[c])
                c += 1
        word = ''.join(word_set)
        #if (word == 'EXCEPT' or word == 'KEYWORDS'):
        #    word_set.insert(0,' ') 
        expArray.append(''.join(word_set))
        return expArray, c


    def cocorToP1Convention(self):
        """funcion para acoplar las expresiones regulares al proyecto 1 haciendo conversiones como: 

        - kleene closure
            - digit{digit} = digit digit *
            - {} = * (0 o mas)  -->  r*

        - positive closure
            - [digit] = digit? = digit|ε
            - [] = ? (cero o una instancia)  -->  r? = r|ε

        - concatenacion
            - '~' = operador explicito para concatenacion
        """
        closures = []
        expArray = []
        for key, tokens_exp in self.tokensInFile.items():
            c = 0
            while c < len(tokens_exp):
                currentChar = tokens_exp[c]
                if tokens_exp[c] == " ":
                    c += 1
                    continue
                elif(tokens_exp[c] == "{"):
                    expArray, c = self.intoBraces(tokens_exp,c,expArray)
                elif(tokens_exp[c] == "("):
                    expArray, c = self.intoParenthesis(tokens_exp,c,expArray)
                elif(tokens_exp[c] == "["):
                    expArray, c = self.intoBrackets(tokens_exp,c,expArray)
                elif(tokens_exp[c].isalpha() or c == '|'):
                    expArray, c = self.alphaNumericIterator(tokens_exp,c,expArray)
                elif(tokens_exp[c] in "'\""):
                    expArray, c = self.intoQuotationsApostrophes(tokens_exp,c,expArray)
                elif(tokens_exp[c] in "})]"):
                    print('Revisar cerraduras de apertura en la expresion')
                else:
                    l = 0
                    print('else')

            finalExpArray = []
            c = 0
            #for exp in expArray:
            if('(' in expArray):
                while (c < len(expArray)):
                    if(expArray[c] == '('):
                        exp = expArray[c] + expArray[c+1]
                        finalExpArray.append(exp)
                        c += 2
                    else:
                        finalExpArray.append(expArray[c])
                        c += 1
                #finalExpArray[0] = '('+expArray[0]
                #if(expArray[len(expArray)-1] == ')|ε'):
                #    closure = finalExpArray.pop()
                #    token_before = finalExpArray.pop()
                #    joining = token_before+closure+')'
                #    finalExpArray.append(joining)
                #    finalExpArray.append('#')

                self.tokensConvertionInFile[key] = '~'.join(finalExpArray)
            else:
                self.tokensConvertionInFile[key] = '~'.join(expArray)
            expArray = []


    def tokensToPostfix(self):
        expOpArray = []
        except_arr = []
        for key, tokens_exp in self.tokensConvertionInFile.items():
            c = 0
            if ('EXCEPT' in tokens_exp or 'KEYWORDS' in tokens_exp):
                except_arr.append('EXCEPT KEYWORDS')
                numToRemove = (len('EXCEPT')+len('KEYWORDS')+2)
                numCharacters = len(tokens_exp)-numToRemove
                tokens_exp_new = tokens_exp[:numCharacters]
            else:
                tokens_exp_new = tokens_exp

            while c < len(tokens_exp_new):
                currentChar = tokens_exp_new[c]
                if tokens_exp_new[c] == " ":
                    c += 1
                    continue
                elif(tokens_exp_new[c] in "~*|)("):
                    expOpArray.append(tokens_exp_new[c])
                    c += 1
                elif(tokens_exp_new[c].isalpha()):
                    expOpArray, c = self.alphaNumericIterator(tokens_exp_new,c,expOpArray,False)
                elif(tokens_exp_new[c] in "'\""):
                    expOpArray, c = self.intoQuotationsApostrophesV2(tokens_exp_new,c,expOpArray)
                else:
                    l = 0
                    print('else')

            if(len(except_arr) == 0):
                self.tokensReadyForPosFix[key] = expOpArray
            else:
                self.tokensReadyForPosFix[key] = [expOpArray,except_arr]
            expOpArray = []
            except_arr = []

        print('')

        #for key, exp in self.tokensReadyForPosFix.items():
        #    self.tokensPosFixInFile[key] =  self.objToPostfix.infix_to_postfix(exp)


    def fileContents(self):
        self.cocorToP1Convention()
        self.tokensToPostfix()
        print(self.charactersInFile)
        print(self.keyWordsInFile)
        print(self.tokensInFile)
        print(self.tokensConvertionInFile)
        print(self.test_patterns)


#tests__________
def main():
    obj = Cocor()
    obj.read_def_cfg()
    obj.read_test_file()
    obj.cocorToP1Convention()
    obj.fileContents()


if __name__ == "__main__":
    main()



'''
ident=letter{letter|digit} EXCEPT KEYWORDS.
number=digit{digit}.
hexnumber="0x"hexdigit{hexdigit}.
float=digit{digit}'.'{digit}['E'['+'|'-']digit{digit}].
space = whitespace{whitespace}.
test = {digit|letter} digit letter letter.
'''