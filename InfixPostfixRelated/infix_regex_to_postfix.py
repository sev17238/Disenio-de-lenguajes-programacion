######################################################
# Diego Sevilla
# 17238
######################################################
# infix_regex_to_postfix.py
######################################################
# Programa que evalua una expresion regular en notacion
# infix, sustituye operadores equivalentes y la 
# traduce a notacion postfix usando el algoritmo 
# de Shunting-yard.
######################################################

#Descripcion de algoritmo______________________________________________
'''
A simple conversion, Shunting-yard algorithm
    1. Input: 3 + 4
    2. Push 3 to the output queue (whenever a number is read it is pushed to the output)
    3. Push + (or its ID) onto the operator stack
    4. Push 4 to the output queue
    5. After reading the expression, pop the operators off the stack and add them to the output.
       In this case there is only one, "+".

    6. Output: 3 4 +

This already shows a couple of rules:
    All numbers are pushed to the output when they are read.
    At the end of reading the expression, pop all operators off the stack and onto the output.
'''

#constants area______________________________________________
'''Diccionario de precedencias'''
operators_precedence = {
  1: '(',
  2: '|',
  3: '.', # operador de concatenacion explicito
  4: '?',
  4: '*',
  4: '+',
  5: '^',
}

#Functions area______________________________________________
def get_key(character):
    '''
    Funcion que retorna la llave para un caracter cualquiera.

    Parametros:
     - character: un caracter o token 
    '''
    #print('character: '+character)
    for key, value in operators_precedence.items():
        if character == value:
            return key

    return None

def get_precendence(character):
    '''
    Funcion que retorna la precedencia del operador ingresado.

    Parametros:
     - character: un caracter o token 
     - return - la precedencia correspondiente
    '''
    precedence = get_key(character)
    precedence = 6 if precedence == None else precedence
    return precedence

def replace_case_with_equivalent(regex,t=0):
    '''
    Funcion que reemplaza el operador a? o el operador a+ por sus equivalentes. 
    Eq. r+ = r|r*, r? = r|ε

    Parametros:
     - regex: una expresion regular con posibles operadores ? o +
     - t: una posicion mas del indice donde se encontro el ultimo caracter y se le reemplazo (a|b)a?a* => (a|b)(a|ε)a* => t = 10
     - retorna cadena equivalente sustituyendo una ocurrencia de ? o +
    '''
    eqRegex = regex
    index = 0
    equivalent = ''
    substringToReplace = ''
    addToIndex = 0
    opQ = eqRegex.find('?',t)
    opPlus = eqRegex.find('+',t)
    Q = False
    Plus = False
    if(opQ != -1 and opPlus != -1):
        if(opQ > opPlus):
            index = opPlus
            Plus = True
        else:
            index = opQ
            Q = True
    elif(opQ != -1):
        index = opQ
        Q = True
    elif(opPlus != -1):
        index = opPlus
        Plus = True

    if(Q == True):
        #index = eqRegex.find('?',t)
        itemBeforeOp = eqRegex[index-1]
        if(itemBeforeOp == ')'):
            for i in range(index-1,-1,-1):
                equivalent = eqRegex[i] + equivalent
                addToIndex = addToIndex +1
                if(eqRegex[i] == '('):
                    break
            substringToReplace = equivalent +'?'
            equivalent = '('+equivalent+'|ε)'
            #print('finish reverse for')
        else:
            addToIndex = addToIndex +1
            substringToReplace = itemBeforeOp+'?'
            equivalent = '('+itemBeforeOp+'|ε)'
        eqRegex = eqRegex.replace(substringToReplace,equivalent)
    if(Plus == True):
        #index = eqRegex.find('+',t)
        itemBeforeOp = eqRegex[index-1]
        if(itemBeforeOp == ')'):
            for i in range(index-1,-1,-1):
                equivalent = eqRegex[i] + equivalent
                addToIndex = addToIndex +1
                if(eqRegex[i] == '('):
                    break
            substringToReplace = equivalent +'+'
            equivalent = '('+equivalent+')('+equivalent+')*'
            #print('finish reverse for')
        else:
            addToIndex = addToIndex +1
            substringToReplace = itemBeforeOp+'+'
            equivalent = '('+itemBeforeOp+')('+itemBeforeOp+')*'
        eqRegex = eqRegex.replace(substringToReplace,equivalent)

    index = index + addToIndex
    return eqRegex, index

def replace_cases_with_equivalents(regex):
    '''
    Funcion que utiliza replace_case_with_equivalent() recuerrentemente para convertir todos los a? y a+
    a sus equivalentes.

    Parametros:
     - regex: expresion regular
     - return - la expresion regular con todos los casos equivalentes
    '''
    t=0
    eqLastRegex, index = replace_case_with_equivalent(regex)
    eqRegex = eqLastRegex
    if(eqLastRegex != regex):
        t = index
        while(t < len(eqRegex)):
            if(eqLastRegex.find('?',t) != -1 or eqLastRegex.find('+',t) != -1):
                eqLastRegex, index = replace_case_with_equivalent(eqLastRegex,t)
                eqRegex = eqLastRegex
                t = index
            else:
                t = t+1

    return eqRegex

def format_reg_ex(regex):
    ''' 
        Funcion que transforma una expresion regular insertando un '.' 
        como indicador/operador explicito de concatenacion.

        Parametros:
         - regex: una cadena (expresion regular)
    '''
    res = ''
    allOperators = ['|','?','+','*','^']
    binaryOperators = ['^','|']

    for i in range(0,len(regex)):
        c1 = regex[i]
        if(i+1 < len(regex)):
            c2 = regex[i+1]
            res += c1
            # si c1 no existe en el conjunto de operadores, c2 no existe en el de operadores binarios y tampoco son parentesis
            if(c1 != '(' and c2 != ')' and (c2 in set(allOperators)) == False and (c1 in set(binaryOperators)) == False): 
                res += '.'

    res += regex[len(regex)-1]

    return res

def infix_to_postfix(regex):
    '''
    Funcion que convierte una expresion regular en formato infix a formato postfix

    Parametros:
     - regex: una cadena (expresion regular)
    '''
    postfix = ''
    stack = []
    formattedRegex = format_reg_ex(regex)

    for cc in range(len(formattedRegex)):
        c = formattedRegex[cc]
        if (c == '('):
            stack.append(c)
        elif(c == ')'):
            #si el ultimo elemento de la pila es '(' 
            while (stack[-1] != '('): 
                postfix += stack.pop()
            stack.pop();
        else:
            while(len(stack) > 0):
                peekedChar = stack[-1]

                peekedCharPrecedence = get_precendence(peekedChar)
                currentCharPrecedence = get_precendence(c)
                #print(str(peekedCharPrecedence)+' '+str(currentCharPrecedence))

                if(peekedCharPrecedence >= currentCharPrecedence):
                    postfix += stack.pop()
                else:
                    break

            stack.append(c)

    while(len(stack) > 0):
        postfix += stack.pop()

    print('infix   = '+regex)
    return postfix

# Main______________________________________________
def main():
    #regEx = str(sys.argv[1])
    
    '''
    regEx1  = '(a*|b*)c'
    regEx2  = '(b|b)*abb(a|b)*'
    regEx3  = '(a|ε)b(a+)c?'
    regEx4  = '(a|b)*a(a|b)(a|b)'
    regEx5  = 'b*ab?'
    regEx6  = 'b+abc+'
    regEx7  = 'ab*ab*'
    regEx8  = '0(0|1)*0'
    regEx9  = '((ε|0)1*)*'
    regEx10 = '(0|1)*0(0|1)(0|1)'
    regEx11 = '(00)*(11)*'
    regEx12 = '(0|1)1*(0|1)'
    regEx13 = '0?(1|ε)?0*'
    regEx14 = '((1?)*)*'
    regEx15 = '(01)*(10)*'
    regEx16 = '(a|b)*a(a|b)(a|b)'

    print('postfix = ' + infix_to_postfix(regEx1) );
    print('postfix = ' + infix_to_postfix(regEx2) );
    print('postfix = ' + infix_to_postfix(regEx3) );
    print('postfix = ' + infix_to_postfix(regEx4) );
    print('postfix = ' + infix_to_postfix(regEx5) );
    print('postfix = ' + infix_to_postfix(regEx6) );
    print('postfix = ' + infix_to_postfix(regEx7) );
    print('postfix = ' + infix_to_postfix(regEx8) );
    print('postfix = ' + infix_to_postfix(regEx9) );
    print('postfix = ' + infix_to_postfix(regEx10));
    print('postfix = ' + infix_to_postfix(regEx11));
    print('postfix = ' + infix_to_postfix(regEx12));
    print('postfix = ' + infix_to_postfix(regEx13));
    print('postfix = ' + infix_to_postfix(regEx14));
    print('postfix = ' + infix_to_postfix(regEx15));
    print('postfix = ' + infix_to_postfix(regEx16));
    '''

    #E. R. CORRECTAS
    print('EXPRESIONES REGULARES CORRECTAS ----')
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(a|b)*a(a|b)(a|b)+')).replace('..','.'))
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('((1?)*)*')).replace('..','.'))
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(a|ε)b(a+)c?')).replace('..','.'))
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(1|0)+001')).replace('..','.'))
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(a|ε)b(a+)c?')).replace('..','.'))
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(εa|εb)*abb')).replace('..','.'))

    #E. R. Incorrectas (manejo de errores)
    '''print('EXPRESIONES REGULARES INCORRECTAS ----')
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(a|b*a(a|b)(a|b)+')).replace('..','.'))
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(a|b)*a(a|b)(a|b)+')).replace('..','.'))
    print()
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('((1?)**')).replace('..','.'))
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(1?)*')).replace('..','.'))
    print()
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(a|ε)b(a+c?')).replace('..','.'))
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(a|ε)b(a+c?)')).replace('..','.'))
    print()
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(εa|εb)*(ab)b')).replace('..','.'))
    print('postfix = ' + infix_to_postfix(replace_cases_with_equivalents('(εa|εb)*ab)b')).replace('..','.'))'''
    

    


if __name__ == "__main__":
    main()


