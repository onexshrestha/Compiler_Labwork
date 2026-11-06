
# Program for Intermediate Code Generation
# using Three Address Code (TAC)

import re

# Operator precedence
precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}


# Convert infix expression to postfix
def infix_to_postfix(expression):
    tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[()+\-*/]', expression)

    # Validate input tokens
    if ''.join(tokens) != re.sub(r'\s+', '', expression):
        raise ValueError("Invalid expression")

    output = []
    stack = []

    for token in tokens:

        if re.fullmatch(r'[a-zA-Z_]\w*|\d+', token):
            output.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())

            if not stack:
                raise ValueError("Unmatched parentheses")

            stack.pop()

        else:
            while (stack and stack[-1] != '(' and
                   precedence[stack[-1]] >= precedence[token]):
                output.append(stack.pop())

            stack.append(token)

    while stack:
        if stack[-1] == '(':
            raise ValueError("Unmatched parentheses")

        output.append(stack.pop())

    return output


# Generate Three Address Code
def generate_tac(postfix):
    stack = []
    code = []
    temp_count = 1

    for token in postfix:

        if token not in precedence:
            stack.append(token)

        else:
            if len(stack) < 2:
                raise ValueError("Invalid expression")

            operand2 = stack.pop()
            operand1 = stack.pop()

            temp = f"t{temp_count}"
            temp_count += 1

            code.append(f"{temp} = {operand1} {token} {operand2}")
            stack.append(temp)

    if len(stack) != 1:
        raise ValueError("Invalid expression")

    return code, stack[0]


# Main Program
expression = input("Enter arithmetic expression: ")

try:
    postfix = infix_to_postfix(expression)
    tac, result = generate_tac(postfix)

    print("\nIntermediate Code (Three Address Code):")

    for instruction in tac:
        print(instruction)

    print(f"Result = {result}")

except ValueError as error:
    print("Invalid Expression:", error)
