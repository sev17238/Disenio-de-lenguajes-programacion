######################################################
# Diego Sevilla
# 17238
######################################################
# functions.py
######################################################
# Modulo de funciones utiles para el proyecto.
######################################################


#constants area______________________________________________
'''Abc just for displaying AFD states as letters'''
abc_dic = {
  'A':  1 ,
  'B':  2 ,
  'C':  3 ,
  'D':  4 ,
  'E':  5 ,
  'F':  6 ,
  'G':  7 ,
  'H':  8 ,
  'I':  9 ,
  'J':  10,
  'K':  11,
  'L':  12,
  'M':  13,
  'N':  14,
  'O':  15,
  'P':  16,
  'Q':  17,
  'R':  18,
  'S':  19,
  'T':  20,
  'U':  21,
  'V':  22,
  'W':  23,
  'X':  24,
  'Y':  25,
  'Z':  26,
  'AA': 27,
  'BB': 28,
  'CC': 29,
  'DD': 30,
  'EE': 31,
  'FF': 32,
  'GG': 33,
  'HH': 34,
  'II': 35,
  'JJ': 36,
  'KK': 37,
  'LL': 38,
  'MM': 39,
  'NN': 40,
  'OO': 41,
  'PP': 42,
  'QQ': 43,
  'RR': 44,
  'SS': 45,
  'TT': 46,
  'UU': 47,
  'VV': 48,
  'WW': 49,
  'XX': 50,
  'YY': 51,
  'ZZ': 52
}

# Functions area______________________________________________
def get_abc_key(number):
    '''
    Funcion que retorna la llave para un caracter cualquiera en un diccionario.

    Parametros:
     - character: un caracter o token 
    '''
    #print('character: '+character)
    for key, value in abc_dic.items():
        if number == value:
            return key

    return None

def getRegExUniqueTokens(postfix_regex):
    '''
    Funcion que obtiene los tokens unicos o el lenguaje de una expresion regular en formato postfix.
    '''
    ops = '*|.#'
    tokens = []
    for i in range(len(postfix_regex)):
        token = postfix_regex[i]
        op_exist = token in ops
        if(op_exist == False):
            tokens.append(token)

    return list(dict.fromkeys(tokens))
    #print(getRegExUniqueTokens('10|10|*.0.0.1.'))


def stringToArray(string):
    result = string.replace('',' ').split(' ')
    result.pop(0)
    result.pop()
    return result
    #print(spacesToString('1ε|**'))

def representsInt(st):
        try: 
            int(st)
            return True
        except ValueError:
            return False

class functions:
    """functions class
    """

    def isOperand(self,character):
        """
        REtorna TRUE si el caracter ingresado es un alfanumerico, FALSE de lo contrario
        *@param ch: el caracter a ser probado
        """
        if character.isalnum() or character == "ε" or character == "#":
            return True
        return False

    def is_op(self, a):
        """
        Testeamos si el caracter de entrada es un operando
        *@param a: caracter a ser probado
        """
        if a == '+' or a == '.' or a == '*' or a == '?' or a == '|':
            return True
        return False

    def replace_all_non_alphabet_chars_string(self,currentString,type):
        resultString = ''.join([s for s in currentString if s.isalpha()])
        return resultString

    def replace_all_non_digit_chars_string(self,currentString):
        resultString = ''.join([s for s in currentString if s.isdigit()])
        return resultString