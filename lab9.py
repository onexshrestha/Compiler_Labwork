
# Program to construct SLR(1) Parsing Table
# and check acceptance or rejection of a string

import re
from collections import defaultdict

# Grammar
grammar = [
    ("E'", ["E"]),
    ("E", ["E", "+", "T"]),
    ("E", ["T"]),
    ("T", ["T", "*", "F"]),
    ("T", ["F"]),
    ("F", ["(", "E", ")"]),
    ("F", ["id"])
]

start_symbol = "E'"
non_terminals = {lhs for lhs, rhs in grammar}
terminals = {s for lhs, rhs in grammar for s in rhs
             if s not in non_terminals}
terminals.add("$")

# Production numbers
productions = list(enumerate(grammar))


# Compute FOLLOW sets
def compute_follow():
    follow = {nt: set() for nt in non_terminals}
    follow[start_symbol].add("$")

    changed = True
    while changed:
        changed = False

        for lhs, rhs in grammar:
            for i, symbol in enumerate(rhs):
                if symbol not in non_terminals:
                    continue

                beta = rhs[i + 1:]

                if beta:
                    first_beta = beta[0]
                    if first_beta not in non_terminals:
                        new = {first_beta}
                    else:
                        # This grammar has no epsilon productions
                        new = set()

                    if not new.issubset(follow[symbol]):
                        follow[symbol].update(new)
                        changed = True

                else:
                    if not follow[lhs].issubset(follow[symbol]):
                        follow[symbol].update(follow[lhs])
                        changed = True

    return follow


# LR(0) Closure
def closure(items):
    items = set(items)

    changed = True
    while changed:
        changed = False

        for p, dot in list(items):
            lhs, rhs = grammar[p]

            if dot < len(rhs):
                symbol = rhs[dot]

                if symbol in non_terminals:
                    for q, (left, right) in productions:
                        if left == symbol and (q, 0) not in items:
                            items.add((q, 0))
                            changed = True

    return frozenset(items)


# GOTO function
def goto(items, symbol):
    moved = set()

    for p, dot in items:
        lhs, rhs = grammar[p]

        if dot < len(rhs) and rhs[dot] == symbol:
            moved.add((p, dot + 1))

    return closure(moved) if moved else frozenset()


# Construct LR(0) item sets
def construct_states():
    states = [closure({(0, 0)})]
    transitions = {}

    i = 0
    while i < len(states):
        symbols = non_terminals | terminals - {"$"}

        for symbol in symbols:
            next_state = goto(states[i], symbol)

            if next_state:
                if next_state not in states:
                    states.append(next_state)

                transitions[(i, symbol)] = states.index(next_state)

        i += 1

    return states, transitions


# Construct SLR Parsing Table
def construct_table(states, transitions, follow):
    action = defaultdict(dict)
    goto_table = defaultdict(dict)

    for i, items in enumerate(states):
        for p, dot in items:
            lhs, rhs = grammar[p]

            # Shift
            if dot < len(rhs):
                symbol = rhs[dot]

                if symbol in terminals:
                    action[i][symbol] = ("shift", transitions[(i, symbol)])

                elif symbol in non_terminals:
                    goto_table[i][symbol] = transitions[(i, symbol)]

            # Reduce or Accept
            else:
                if p == 0:
                    action[i]["$"] = ("accept",)

                else:
                    for symbol in follow[lhs]:
                        action[i][symbol] = ("reduce", p)

    return action, goto_table


# Tokenize input
def tokenize(string):
    pattern = re.compile(r'id|[()+*]')
    tokens = []
    position = 0

    for match in pattern.finditer(string):
        if string[position:match.start()].strip():
            raise ValueError("Invalid input symbol")

        tokens.append(match.group())
        position = match.end()

    if string[position:].strip():
        raise ValueError("Invalid input symbol")

    return tokens + ["$"]


# SLR Parsing
def parse(tokens, action, goto_table):
    stack = [0]
    index = 0

    print("\nStack\t\tInput\t\tAction")

    while True:
        state = stack[-1]
        symbol = tokens[index]

        print(stack, "\t", tokens[index:], end="\t")

        entry = action[state].get(symbol)

        if entry is None:
            print("Rejected")
            return False

        if entry[0] == "shift":
            stack.append(symbol)
            stack.append(entry[1])
            index += 1
            print("Shift", symbol)

        elif entry[0] == "reduce":
            p = entry[1]
            lhs, rhs = grammar[p]

            for _ in range(2 * len(rhs)):
                stack.pop()

            state = stack[-1]
            stack.append(lhs)
            stack.append(goto_table[state][lhs])

            print("Reduce", lhs, "->", " ".join(rhs))

        elif entry[0] == "accept":
            print("Accept")
            return True


# Main Program
follow = compute_follow()
states, transitions = construct_states()
action, goto_table = construct_table(states, transitions, follow)

# Display Parsing Table
print("SLR(1) Parsing Table")
print("State\tACTION\t\tGOTO")

for i in range(len(states)):
    print(i, "\t", action[i], "\t", goto_table[i])

# Input String
input_string = input("\nEnter input string (e.g. id+id*id): ")

try:
    tokens = tokenize(input_string)

    if parse(tokens, action, goto_table):
        print("\nString Accepted")
    else:
        print("\nString Rejected")

except (ValueError, KeyError, IndexError):
    print("\nString Rejected")
