import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}, {self.column})"

class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.keywords = {'let', 'if', 'then', 'else', 'fi', 'while', 'do', 'od', 'call', 'main', 'var'}
        self.token_specification = [
            ('NUMBER',   r'\d+'),
            ('ASSIGN',   r'<-'),
            ('END',      r'\.'),
            ('IDENT',    r'[A-Za-z_]\w*'),
            ('OP',       r'[+\-*/]'),
            ('REL_OP',   r'==|!=|<=|>=|<|>'),
            ('SEMICOLON', r';'),
            ('COMMA',    r','),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('LBRACE',   r'\{'),
            ('RBRACE',   r'\}'),
            ('SKIP',     r'[ \t]+'),
            ('NEWLINE',  r'\n'),
            ('MISMATCH', r'.'),
        ]

    def tokenize(self):
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        line_num = 1
        line_start = 0
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == 'NUMBER':
                value = int(value)
            elif kind == 'IDENT' and value in self.keywords:
                kind = 'KEYWORD'
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            self.tokens.append(Token(kind, value, line_num, column))
        return self.tokens

if __name__ == "__main__":
    code = """
    main
    var x; {
        let x <- call InputNum();
        if x == 1 then
            let x <- 1
        else
            let x <- 2
        fi;
        call OutputNum(x)
    }.
    """
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    for token in tokens:
        print(token)

