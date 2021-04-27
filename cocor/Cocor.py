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
import string

#Clase de implementacion_________________________________________________
class Cocor:
    """Clase con definiciones varias de COCO/R
    """
    # Constructor de las variables
    def __init__(self):

        self.asciiTable = set([chr(char) for char in range(0,255)])
        self.alphabetLower = 'abcdefghijklmnopqrstuvwxyz'
        self.alphabetUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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
        self.charactersInFileSubs2 = {}
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

# ZONA PARA LA LECTURA DEL ARCHIVO-----------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
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
                line.rstrip()
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


# ZONA DE FUNCIONES PARA RECORRER EXPRESIONES REGULARES DE COCO/R -----------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
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

# ZONA DE TRATAMIENTO DE CARACTERES -----------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

    def setOperations(self,i,char_def,set1):
        chr_result_operations = [set1]
        while i < len(char_def):
            if(char_def[i] == '+'):
                set2 = char_def[i+1]
                set1_ = chr_result_operations.pop()
                snum = ''
                if('chr(' in set2.lower()):
                    for e in set2:
                        if(e.isdigit()):
                            snum += e
                    num = int(snum)
                    set2 = set(chr(num))
                    chr_result_operations.append(set1_.union(set2))
                else:
                    ssss = type(set1_)
                    if(isinstance(set1_, str)):
                        set1_ = set(set1_)
                    if(isinstance(set2, str)):
                        set2 = set(set2)
                    chr_result_operations.append(set1_.union(set2))
                i += 2
            elif(char_def[i] == '-'):
                set2 = char_def[i+1]
                set1_ = chr_result_operations.pop()
                snum = ''
                if('chr(' in set2.lower()):
                    for e in set2:
                        if(e.isdigit()):
                            snum += e
                    num = int(snum)
                    set2 = set(chr(num))
                    chr_result_operations.append(set1_.difference(set2))
                else:
                    chr_result_operations.append(set1_.difference(set2))
                i += 2
            else:
                print('no operations else!!!!!!!!!!! :O')
                i += 1
        return i, chr_result_operations

    def whenChrFound(self,char_def,i,subs_char_def):
        if('..' in char_def):
            snum = ''
            enum = ''
            for e in char_def[i]:
                if(e.isdigit()):
                    snum += e
            for e in char_def[i+2]:
                if(e.isdigit()):
                    enum += e
            start = int(snum)
            end = int(enum)
            i += 3
            chr_range = set([chr(char) for char in range(start,end)])
            if(i < len(char_def)):
                i,chr_result_operations = self.setOperations(i,char_def,chr_range)
                subs_char_def.append(chr_result_operations)
            else:
                subs_char_def.append(chr_range)

            return i, subs_char_def
        else:
            snum = ''
            for e in char_def[i]:
                if(e.isdigit()):
                    snum += e
            num = int(snum)
            i += 1
            first_char_in_expresion = chr(num)
            if(i < len(char_def)):
                i,chr_result_operations = self.setOperations(i,char_def,first_char_in_expresion)
                subs_char_def.append(chr_result_operations) 
            else:
                subs_char_def.append(first_char_in_expresion)

            return i, subs_char_def

    def whenAoraFound(self,char_def,i,subs_char_def):
        if('..' in char_def):
            start = ord(char_def[i])
            end = ord(char_def[i+2])
            letter_range = set([chr(char) for char in range(start,end)])
            i += 3
            if(i < len(char_def)):
                i,chr_result_operations = self.setOperations(i,char_def,letter_range)
                subs_char_def.append(chr_result_operations)
            else:
                subs_char_def.append(letter_range)
        else:
            any_word = char_def[i]
            i += 1
            if(i < len(char_def)):
                i,chr_result_operations = self.setOperations(i,char_def,any_word)
                subs_char_def.append(chr_result_operations)
            else:
                subs_char_def.append(any_word)

        return i, subs_char_def

    def whenANYFound(self,char_def,i,subs_char_def):
        anyy = set([chr(char) for char in range(0,255)])
        i += 1
        if(i < len(char_def)):
            i,chr_result_operations = self.setOperations(i,char_def,anyy)
            subs_char_def.append(chr_result_operations) 
        else:
            subs_char_def.append(anyy)

        return i, subs_char_def

    def dictSubstitionItself(self,dict1):
        dict_result = {}
        for key,char_def in dict1.items():
            i = 0
            new_exp = []
            while i < len(char_def):
                value_key = char_def[i]
                substitution = self.functions.get_value_from_dict(value_key,dict1)
                if(substitution != None):
                    new_exp.append(substitution[0])
                else:
                    new_exp.append(char_def[i])
                i += 1

            dict_result[key] = new_exp
        return dict_result

    def dictSubstitionOther(self,dict1,dict2):
        dict_result = {}
        for key,char_def in dict1.items():
            i = 0
            new_exp = []
            while i < len(char_def):
                value_key = char_def[i]
                substitution = self.functions.get_value_from_dict(value_key,dict2)
                if(substitution != None):
                    new_exp.append(substitution[0])
                else:
                    new_exp.append(char_def[i])
                i += 1

            dict_result[key] = new_exp
        return  dict_result

    def charactersSubstitution(self):
        charactersInFileSubs0 = {}
        charArray = []
        # ciclo para convertir los strings en arrays que encapsulen cada operando (item) de la expresion del caracter
        for key, char_def in self.charactersInFile.items():
            new_char_def = []
            for i in char_def.split(' '):
                if (len(i) > 0):
                    e = ''
                    if(i.count('"') == 2):
                        e = i.replace('"','')
                        new_char_def.append(e)
                    elif(i.count("'") == 2):
                        e = i.replace("'",'')
                        new_char_def.append(e)
                    else:
                        new_char_def.append(i)
            charactersInFileSubs0[key] = new_char_def

        #print(':\\\\.')
        #print('"\'"')
        #print('\'"\'')

        print('')

        charactersInFileSubs1 = self.dictSubstitionItself(charactersInFileSubs0)

        print('')

        #self.charactersInFileSubs2 = charactersInFileSubs1

        # sustitucion de las especificaciones de la tabla ascii en el archivo

        #! CHECAR LUEGO DE HEXDIGIT!!!!
        for key,char_def in charactersInFileSubs1.items():
            if(key not in 'letter digit'):
                subs_char_def = []
                subs_char_def2 = []

                i = 0
                while i < len(char_def):
                    curr = char_def[i]
                    if(char_def[i] == ' '):
                        i +=1
                        continue
                    elif('chr(' in char_def[i].lower()):
                        i, subs_char_def = self.whenChrFound(char_def,i,subs_char_def)
                    elif('ANY' in char_def[i]):
                        i,subs_char_def = self.whenANYFound(char_def,i,subs_char_def)
                    elif('A' in char_def[i] or 'a' in char_def[i]):
                        i,subs_char_def = self.whenAoraFound(char_def,i,subs_char_def)
                    else:
                        any_word = set(char_def[i])
                        i += 1
                        if(i < len(char_def)):
                            i,chr_result_operations = self.setOperations(i,char_def,any_word)
                            subs_char_def.append(chr_result_operations) 
                        else:
                            subs_char_def.append(any_word)

                self.charactersInFileSubs2[key] = subs_char_def[0]
                '''if('+' in char_def or '-' in char_def):
                    i = 0
                    while i < len(char_def):
                        if type(char_def[i]) != 'set':
                            chr_capsule = set(char_def[i])
                        i,chr_result_operations = self.setOperations(i,char_def,chr_capsule)
                        subs_char_def2.append(chr_result_operations)

                    self.charactersInFileSubs2[key] = subs_char_def2
                else:
                    self.charactersInFileSubs2[key] = subs_char_def'''



        print(self.charactersInFileSubs2['files'][0])
        print('')

        

# ZONA DE TRATAMIENTO DE TOKENS -----------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
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


    def tokensSubstitution(self):
        dict1 = self.tokensReadyForPosFix
        dict2 = self.charactersInFileSubs2
        self.tokensSubstitution = self.dictSubstitionOther(dict1,dict2)

        return 0


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
    obj.charactersSubstitution()
    obj.cocorToP1Convention()
    obj.tokensToPostfix()

    '''s = set([chr(char) for char in range(0,255)])
    z = ''.join(s)

    print(s)
    print('')
    print(z)'''

    
    
    '''d = {
        'letter': ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'],
        'digit': ['0123456789'],
        'hexdigit': ['digit', '+', 'BCDEF'],
        'tab': ['CHR(9)'],
        'eol': ['CHR(10)'],
        'files': ['letter', '+', 'digit', '+', ':\\\\.'],
        'chars': ['CHR(32)', '..', 'CHR(255)', '-', "'"],
        'string': ['CHR(32)', '..', 'CHR(255)', '-', '"'],
        'macros': ['ANY', '-', 'eol']
    }

    f = d
    z = {}
    for key,value in d.items():
        i = 0
        new_arr = []
        while i < len(value):
            val = value[i]
            substitution = obj.functions.get_value_from_dict(value[i],f)
            if(substitution !=None):
                new_arr.append(substitution)
            else:
                new_arr.append(value[i])
            i += 1
        z[key] = new_arr

    print('')'''



    #obj.fileContents()

    #i = ['a','s','..']
    #e = '..'
    #if(e in i): print(True)


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