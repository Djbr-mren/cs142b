import re


class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value}, {self.line}, {self.column})'

    def __eq__(self, other):
        if isinstance(other, Token):
            return (self.type, self.value, self.line, self.column) == (
            other.type, other.value, other.line, other.column)
        return False


class Tokenizer:
    TOKEN_SPECIFICATION = [
        ('NUMBER', r'\d+'),
        ('KEYWORD', r'\b(if|then|else|fi|while|do|od|and|or|not|let|call|return)\b'),
        ('IDENT', r'[a-zA-Z_][a-zA-Z_0-9]*'),
        ('OP', r'[+\-*/]'),
        ('ASSIGN', r'<-'),
        ('REL_OP', r'==|!=|<=|>=|<|>'),
        ('SEMICOLON', r';'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('WHITESPACE', r'[ \t]+'),
        ('NEWLINE', r'\n'),
    ]

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        line = 1
        column = 1
        for mo in re.finditer(
                '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.TOKEN_SPECIFICATION),
                self.code):
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'NEWLINE':
                line += 1
                column = 1
            elif kind == 'WHITESPACE':
                column += len(value)
            else:
                self.tokens.append(Token(kind, value, line, column))
                column += len(value)
        return self.tokens


if __name__ == '__main__':
    code = """
    if x <= 5 and x != 10 then y <- 10;
    while x >= 100 do x <- x + 1 od;
    """

    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()

    for token in tokens:
        print(token)