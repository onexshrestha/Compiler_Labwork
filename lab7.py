
# Program to compute FOLLOW set of a given grammar

def compute_first(grammar):
    first = {nt: set() for nt in grammar}

    def first_symbol(symbol):
        if symbol not in grammar:
            return {symbol}
        return first[symbol]

    changed = True
    while changed:
        changed = False

        for nt, productions in grammar.items():
            for production in productions:
                nullable = True

                for symbol in production:
                    fs = first_symbol(symbol)
                    new = fs - {'ε'}

                    if not new.issubset(first[nt]):
                        first[nt].update(new)
                        changed = True

                    if 'ε' not in fs:
                        nullable = False
                        break

                if nullable and 'ε' not in first[nt]:
                    first[nt].add('ε')
                    changed = True

    return first


def compute_follow(grammar, start_symbol):
    first = compute_first(grammar)
    follow = {nt: set() for nt in grammar}

    # End marker for start symbol
    follow[start_symbol].add('$')

    changed = True
    while changed:
        changed = False

        for nt, productions in grammar.items():
            for production in productions:

                for i, symbol in enumerate(production):
                    if symbol not in grammar:
                        continue

                    # Symbols after the current non-terminal
                    beta = production[i + 1:]

                    # Add FIRST(beta) - epsilon
                    if beta:
                        nullable = True

                        for b in beta:
                            if b in grammar:
                                fs = first[b]
                            else:
                                fs = {b}

                            new = fs - {'ε'}

                            if not new.issubset(follow[symbol]):
                                follow[symbol].update(new)
                                changed = True

                            if 'ε' not in fs:
                                nullable = False
                                break

                        # If beta can derive epsilon
                        if nullable:
                            if not follow[nt].issubset(follow[symbol]):
                                follow[symbol].update(follow[nt])
                                changed = True

                    else:
                        # If current non-terminal is at the end
                        if not follow[nt].issubset(follow[symbol]):
                            follow[symbol].update(follow[nt])
                            changed = True

    return follow


# Given Grammar
grammar = {
    'E': [['T', "E'"]],
    "E'": [['+', 'T', "E'"], ['ε']],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

# Start Symbol
start_symbol = 'E'

# Compute FOLLOW sets
follow_sets = compute_follow(grammar, start_symbol)

# Display FOLLOW sets
print("FOLLOW Sets:")
for nt, symbols in follow_sets.items():
    print(f"FOLLOW({nt}) = {{ {', '.join(sorted(symbols))} }}")
