
import re

s = input("Enter a string: ")

if re.fullmatch(r'a*', s):
    print("String belongs to a*")
elif re.fullmatch(r'abb', s):
    print("String belongs to abb")
elif re.fullmatch(r'a*b+', s):
    print("String belongs to a*b+")

else:
    print("String does not belong to any language")
