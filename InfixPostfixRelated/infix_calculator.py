######################################################
# Diego Sevilla
# 17238
######################################################
# infix_calculator.py
######################################################
# Programa para evualuar una expresion aritmetica 
# con espacios en blanco o no.
######################################################

#Functions area______________________________________________

def precedence(op):
    '''Function to find precedence of operators.'''
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0

def applyOp(a, b, op):
    '''Function to perform arithmetic operations.'''
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b

def isDecimal(s):
    '''Check decimal existence in the string'''
    if s.find('.') == -1:
        return False
    else:
        return True

def evaluate(tokens):
    ''' Function that returns value of expression after evaluation.

        Parameters:
         - param str tokens: a string expression
         - raises Error: if the input string expression has errors
    '''
    values = [] # stack to store integer values.
    ops = [] # stack to store operators.
    i = 0

    try:
        while i < len(tokens):
            # Current token is a whitespace, skip it.
            if tokens[i] == ' ':
                i += 1
                continue
            # Current token is an opening brace, push it to 'ops'
            elif tokens[i] == '(':
                ops.append(tokens[i])
            # Current token is a number, push it to stack for numbers.
            elif tokens[i].isdigit():
                val = 0
                decP = ''
                valAfterD = 0
                # There may be more than one digits in the number.
                while (i < len(tokens) and (tokens[i].isdigit() or isDecimal(tokens[i])) ):
                    # Check if current token is a number again
                    if(tokens[i].isdigit()):
                        val = (val*10) + int(tokens[i])
                    # Check if current token is a decimal
                    elif (tokens[i].isdigit() == False):
                        decP = str(tokens[i]) #decimal dot
                        while (i < len(tokens) and (tokens[i].isdigit() or isDecimal(tokens[i])) ):
                            if(isDecimal(tokens[i]) == False):
                                valAfterD = (valAfterD*10) + int(tokens[i])
                            i += 1

                        i -= 1 #correct the offset because the while loop also increases i

                        valStr = str(val)+decP+str(valAfterD)
                        val = float(valStr)

                    #print('i: '+str(i)) 
                    i += 1
                #print('val after while: '+str(val))
                values.append(val)

                # right now the i points to the character next to the digit,
                # since the for loop also increases the i, we would skip one
                # token position; we need to decrease the value of i by 1 to
                # correct the offset.
                i -= 1

            # handle case when user input is .2 instead of 0.2
            elif isDecimal(tokens[i]):
                val = 0
                decP = tokens[i]
                valAfterD = 0
                i = i+1 #iterator points to the number after the decimal dot
                while (i < len(tokens) and tokens[i].isdigit()):
                    valAfterD = (valAfterD*10) + int(tokens[i])
                    i += 1
                valStr = str(val)+decP+str(valAfterD)
                val = float(valStr)
                values.append(val)

                i -= 1 #correct the offset because the while loop also increases i

            # Closing brace encountered, solve entire brace.
            elif tokens[i] == ')':
                while (len(ops) != 0 and ops[-1] != '('):
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()

                    values.append(applyOp(val1, val2, op))
                # pop opening brace.
                ops.pop()

            # Current token is an operator.
            else:

                # While top of 'ops' has same or greater precedence to current
                # token, which is an operator. Apply operator on top of 'ops'
                # to top two elements in values stack.
                while (len(ops) != 0 and precedence(ops[-1]) >= precedence(tokens[i])):
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()

                    values.append(applyOp(val1, val2, op))
                # Push current token to 'ops'.
                ops.append(tokens[i])

            i += 1

        # Entire expression has been parsed at this point, apply remaining ops to remaining values.
        while len(ops) != 0:
            val2 = values.pop()
            val1 = values.pop()
            op = ops.pop()

            values.append(applyOp(val1, val2, op))

        # Top of 'values' contains result, return it.
        return values[-1]

    except Exception as e:
        print('Error while parsing the operations string!')
        print (" '" + str(e)+ "'")


#Main______________________________________________
if __name__ == "__main__":
    print(evaluate("100+2*6"))
    print(evaluate("10*(2+(1.2*(20+2/3)))/14"))
    print(evaluate('26+(.248+(5/.2335))'))

