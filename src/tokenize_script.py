from tokenizer import Tokenizer

code = """
if x <= 5 and x != 10 then y <- 10;
while x >= 100 do x <- x + 1 od;
"""

tokenizer = Tokenizer(code)
tokens = tokenizer.tokenize()

for token in tokens:
    print(token)