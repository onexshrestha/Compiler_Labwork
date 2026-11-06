
import re

# Given Grammar
grammar = {
    'E': [['T', "E'"]],
    "E'": [['+', 'T', "E'"], []],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], []],
    'F': [['(', 'E', ')'], ['id']]
}

start_symbol = 'E'
non_terminals = set(grammar)
terminals = {'id', '+', '*', '(', ')', '$'}


# Compute FIRST sets
def compute_first():
    first = {nt: set() for nt in grammar}

    changed = True
    while changed:
        changed = False

        for nt, productions in grammar.items():
            for production in productions:
                result = set()
                nullable = True

                for symbol in production:
                    fs = first[symbol] if symbol in grammar else {symbol}
                    result.update(fs - {'ε'})

                    if 'ε' not in fs:
                        nullable = False
                        break

                if nullable:
                    result.add('ε')

                if not result.issubset(first[nt]):
                    first[nt].update(result)
                    changed = True

    return first


# FIRST of a production
def first_of_sequence(sequence, first):
    result = set()
    nullable = True

    for symbol in sequence:
        fs = first[symbol] if symbol in grammar else {symbol}
        result.update(fs - {'ε'})

        if 'ε' not in fs:
            nullable = False
            break

    if nullable:
        result.add('ε')

    return result


# Compute FOLLOW sets
def compute_follow(first):
    follow = {nt: set() for nt in grammar}
    follow[start_symbol].add('$')

    changed = True
    while changed:
        changed = False

        for nt, productions in grammar.items():
            for production in productions:
                for i, symbol in enumerate(production):

                    if symbol not in grammar:
                        continue

                    beta = production[i + 1:]
                    fs = first_of_sequence(beta, first)

                    new = fs - {'ε'}

                    if not new.issubset(follow[symbol]):
                        follow[symbol].update(new)
                        changed = True

                    if 'ε' in fs:
                        if not follow[nt].issubset(follow[symbol]):
                            follow[symbol].update(follow[nt])
                            changed = True

    return follow


# Construct LL(1) Parsing Table
def construct_table(first, follow):
    table = {nt: {} for nt in grammar}

    for nt, productions in grammar.items():
        for production in productions:
            fs = first_of_sequence(production, first)

            for terminal in fs - {'ε'}:
                table[nt][terminal] = production

            if 'ε' in fs:
                for terminal in follow[nt]:
                    table[nt][terminal] = production

    return table


# Tokenize and validate input
def tokenize(string):
    tokens = []
    pattern = re.compile(r'id|[()+*]')

    position = 0
    for match in pattern.finditer(string):
        # Reject invalid characters between tokens
        if string[position:match.start()].strip():
            raise ValueError("Invalid input symbol")

        tokens.append(match.group())
        position = match.end()

    if string[position:].strip():
        raise ValueError("Invalid input symbol")

    return tokens + ['$']


# Predictive Parsing
def parse_string(tokens, table):
    stack = ['$' , start_symbol]
    index = 0

    print("\nStack\t\tInput\t\tAction")

    while stack:
        top = stack[-1]
        current = tokens[index]

        print(stack, "\t", tokens[index:], end="\t")

        # Match terminal
        if top not in grammar:
            if top == current:
                stack.pop()
                index += 1
                print("Match", current)
            else:
                print("Rejected")
                return False

        # Expand non-terminal
        else:
            production = table[top].get(current)

            if production is None:
                print("Rejected")
                return False

            stack.pop()

            if production:
                stack.extend(reversed(production))

            print(top, "->", " ".join(production) if production else "ε")

    return index == len(tokens)


# Main Program
first = compute_first()
follow = compute_follow(first)
table = construct_table(first, follow)

# Display Parsing Table
print("LL(1) Parsing Table")
print("NT\tid\t+\t*\t(\t)\t$")

for nt in grammar:
    row = []
    for terminal in ['id', '+', '*', '(', ')', '$']:
        production = table[nt].get(terminal)

        if production is not None:
            value = " ".join(production) if production else "ε"
            row.append(f"{nt}->{value}")
        else:
            row.append("-")

    print(nt, "\t", "\t".join(row))


# Input and Result
input_string = input("\nEnter input string (e.g. id+id*id): ")

try:
    tokens = tokenize(input_string)

    if parse_string(tokens, table):
        print("\nString Accepted")
    else:
        print("\nString Rejected")

except ValueError as error:
    print("\nString Rejected:", error)
