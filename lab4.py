
import re

identifier = input("Enter an identifier: ")

pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'

if re.fullmatch(pattern, identifier):
    print("Valid Identifier")
else:
    print("Invalid Identifier")
