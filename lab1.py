
text = input("Enter a string: ")

text = text.strip()

if text.startswith("//"):
    print("Valid single-line comment")
elif text.startswith("/*") and text.endswith("*/"):
    print("Valid multi-line comment")
else:
    print("Not a valid comment")
