
# Program to compute FIRST set of a given grammar

def compute_first(grammar):
    first = {non_terminal: set() for non_terminal in grammar}

    def first_of_symbol(symbol):
        # If symbol is a terminal
        if symbol not in grammar:
            return {symbol}

        return first[symbol]

    changed = True

    while changed:
        changed = False

        for non_terminal, productions in grammar.items():
            for production in productions:

                # Handle epsilon production
                if production == ['ε']:
                    if 'ε' not in first[non_terminal]:
                        first[non_terminal].add('ε')
                        changed = True
                    continue

                nullable = True

                for symbol in production:
                    symbol_first = first_of_symbol(symbol)

                    # Add all symbols except epsilon
                    new_symbols = symbol_first - {'ε'}

                    if not new_symbols.issubset(first[non_terminal]):
                        first[non_terminal].update(new_symbols)
                        changed = True

                    # If symbol cannot produce epsilon
                    if 'ε' not in symbol_first:
                        nullable = False
                        break

                # If all symbols can produce epsilon
                if nullable:
                    if 'ε' not in first[non_terminal]:
                        first[non_terminal].add('ε')
                        changed = True

    return first


# Input grammar
grammar = {
    'E': [['T', "E'"]],
    "E'": [['+', 'T', "E'"], ['ε']],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

# Compute FIRST sets
first_sets = compute_first(grammar)

# Display FIRST sets
print("FIRST Sets:")
for non_terminal, symbols in first_sets.items():
    print(f"FIRST({non_terminal}) = {{ {', '.join(sorted(symbols))} }}")
