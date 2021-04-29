######################################################
# Diego Sevilla
# 17238
######################################################
# InfixRegexToPostfix.py
######################################################
# Programa que evalua una expresion regular en notacion
# infix, sustituye operadores equivalentes y la 
# traduce a notacion postfix 
######################################################

#Clase de implementacion_________________________________________________
class InfixRegexToPostfixWords:
    '''
    Clase que convierte una expresion infix a formato postfix

    Atributos:
     - expresion --> la expresion regular en formato infix
    '''
    # Constructor de las variables
    def __init__(self):
        self.operators_precedence = {
        1: '(',
        2: '|',
        3: '~', # operador de concatenacion explicito
        4: '?',
        4: '*',
        4: '+'
        }

    def get_key(self,character):
        '''
        Funcion que retorna la llave para un caracter cualquiera.

        Parametros:
        - character: un caracter o token 
        '''
        #print('character: '+character)
        for key, value in self.operators_precedence.items():
            if character == value:
                return key
        return None

    def get_precendence(self,character):
        '''
        Funcion que retorna la precedencia del operador ingresado.
        Parametros:
        - character: un caracter o token
        - return - la precedencia correspondiente
        '''
        precedence = self.get_key(character)
        precedence = 5 if precedence == None else precedence
        return precedence

    def infix_to_postfix(self,expresion):
        '''
        Funcion que convierte una expresion regular en formato infix a formato postfix.
        Esta expresion regular es ingresada al instancia un objeto de esta clase.
        '''

        postfix = ''
        postfix_exp = []
        stack = []


        #!la expresion ya viene lista para pasarse a posfix
        eqRegex = expresion

        #formattedRegex = self.format_reg_ex(regex)
        #eqRegex = self.replace_cases_with_equivalents(formattedRegex)
        
        if('EXCEPT KEYWORDS' in expresion[1]):
            eqRegex = expresion[0]
        else:
            eqRegex = expresion

        #c puede ser tanto un posible token como un operador
        for counter in range(len(eqRegex)):
            c = eqRegex[counter]
            if (c == '('):
                stack.append(c)
            elif(c == ')'):
                #si el ultimo elemento de la pila es '(' 
                while (stack[-1] != '('): 
                    #postfix += stack.pop()
                    postfix_exp.append(stack.pop())

                stack.pop();
            else:
                while(len(stack) > 0):
                    peekedChar = stack[-1]

                    peekedCharPrecedence = self.get_precendence(peekedChar)
                    currentCharPrecedence = self.get_precendence(c)
                    #print(str(peekedCharPrecedence)+' '+str(currentCharPrecedence))

                    if(peekedCharPrecedence >= currentCharPrecedence):
                        #postfix += stack.pop()
                        postfix_exp.append(stack.pop())
                    else:
                        break

                stack.append(c)


        while(len(stack) > 0):
            #postfix += stack.pop()
            postfix_exp.append(stack.pop())

        #if(postfix.find('(') != -1):

        if('(' in postfix_exp):
            #postfix = 'ERROR_POSTFIX_)'
            postfix_exp = ['ERROR_POSTFIX_)']

        #print(' - infixEq     = '+str(eqRegex))

        print(' - infixEq     = '+''.join(eqRegex))
        #print('postfix   = '+postfix)
        print(' - postfix     = '+''.join(postfix_exp))

        if '~~' in postfix_exp:
            for counter in len(postfix_exp):
                item = postfix_exp[counter]
                if item == '~~':
                    postfix_exp[counter] = '~'

        return postfix_exp

# Main______________________________________________
def main():
    obj = InfixRegexToPostfixWords()

if __name__ == "__main__":
    main()


