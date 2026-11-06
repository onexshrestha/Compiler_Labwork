
import re

# Open the source file
with open("lab2source.txt", "r") as file:
    text = file.read()

# Define token patterns
token_pattern = r'\b\d+\b|\b[A-Za-z_][A-Za-z0-9_]*\b|[+\-*/=<>!]+|[();{},]'

# Identify tokens
tokens = re.findall(token_pattern, text)

# Display tokens
print("Tokens identified from the source file:")

for token in tokens:
    print(token)
