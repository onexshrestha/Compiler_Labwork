
# Program for Final Code Generation
# Converts Three Address Code (TAC) into Assembly-like Code

import re

# Generate target code from TAC
def generate_code(tac):
    target_code = []

    for instruction in tac:
        instruction = instruction.strip()

        # Match: result = operand1 operator operand2
        match = re.fullmatch(
            r'(\w+)\s*=\s*(\w+)\s*([+\-*/])\s*(\w+)',
            instruction
        )

        # Match: result = operand
        assign = re.fullmatch(
            r'(\w+)\s*=\s*(\w+)',
            instruction
        )

        if match:
            result, op1, operator, op2 = match.groups()

            target_code.append(f"MOV R0, {op1}")
            target_code.append(f"MOV R1, {op2}")

            if operator == '+':
                target_code.append("ADD R0, R1")
            elif operator == '-':
                target_code.append("SUB R0, R1")
            elif operator == '*':
                target_code.append("MUL R0, R1")
            elif operator == '/':
                target_code.append("DIV R0, R1")

            target_code.append(f"MOV {result}, R0")

        elif assign:
            result, operand = assign.groups()
            target_code.append(f"MOV {result}, {operand}")

        else:
            raise ValueError(f"Invalid TAC instruction: {instruction}")

    return target_code


# Main Program
print("Enter Three Address Code (TAC)")
print("Enter 'END' to finish input")

tac = []

while True:
    instruction = input("TAC: ").strip()

    if instruction.upper() == "END":
        break

    if instruction:
        tac.append(instruction)

try:
    final_code = generate_code(tac)

    print("\nFinal Target Code:")
    for instruction in final_code:
        print(instruction)

except ValueError as error:
    print(error)
