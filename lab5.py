
import re

# Define keywords
keywords = {
    "int", "float", "char", "double", "void",
    "if", "else", "while", "for", "return",
    "break", "continue", "switch", "case",
    "default", "do", "struct"
}

# Define operators
operators = {
    "+", "-", "*", "/", "%", "=",
    "==", "!=", "<", ">", "<=", ">=",
    "&&", "||", "!", "++", "--",
    "+=", "-=", "*=", "/="
}

# Define special symbols
special_symbols = {
    "(", ")", "{", "}", "[", "]",
    ";", ",", "#"
}

# Read source code
with open("lab5source.txt", "r") as file:
    code = file.read()

# Token pattern
pattern = r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\d+\.\d+|\d+|[A-Za-z_]\w*|==|!=|<=|>=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|[+\-*/%=<>!]|[(){}\[\];,#]'

tokens = re.findall(pattern, code)

print("\nLEXICAL ANALYSIS")
print("-" * 40)

for token in tokens:

    if token.startswith("//") or token.startswith("/*"):
        category = "Comment"

    elif token in keywords:
        category = "Keyword"

    elif token in operators:
        category = "Operator"

    elif token in special_symbols:
        category = "Special Symbol"

    elif re.fullmatch(r'\d+(\.\d+)?', token):
        category = "Constant"

    elif token.startswith('"') or token.startswith("'"):
        category = "String Literal"

    elif re.fullmatch(r'[A-Za-z_]\w*', token):
        category = "Identifier"

    else:
        category = "Unknown"

    print(f"{token:<25} -> {category}")
