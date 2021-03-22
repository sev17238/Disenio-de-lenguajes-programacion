######################################################
# Diego Sevilla
# 17238
######################################################
# functions.py
######################################################
# Modulo de funciones utiles para el proyecto.
######################################################


def getRegExUniqueTokens(postfix_regex):
    '''
    Funcion que obtiene los tokens unicos o el lenguaje de una expresion regular en formato postfix.
    '''
    ops = '*|.'
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
