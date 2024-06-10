from tokenizer import Tokenizer, Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def error(self, message):
        raise Exception(f'Error parsing input: {message}')

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = Token('EOF', '', self.current_token.line, self.current_token.column)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            self.error(f'Expected token {token_type}, got {self.current_token.type}')

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return token
        elif token.type == 'IDENT':
            self.eat('IDENT')
            return token
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expression()
            self.eat('RPAREN')
            return node
        else:
            self.error('Invalid factor')

    def term(self):
        node = self.factor()
        while self.current_token.type in ('OP', 'MUL', 'DIV'):
            token = self.current_token
            if token.type == 'OP':
                self.eat('OP')
            node = (token, node, self.factor())
        return node

    def expression(self):
        node = self.term()
        while self.current_token.type in ('OP', 'ADD', 'SUB'):
            token = self.current_token
            if token.type == 'OP':
                self.eat('OP')
            node = (token, node, self.term())
        return node

    def assignment(self):
        self.eat('KEYWORD')  # 'let'
        var = self.current_token
        self.eat('IDENT')
        self.eat('ASSIGN')
        expr = self.expression()
        return ('ASSIGN', var, expr)

    def statement(self):
        if self.current_token.type == 'KEYWORD':
            if self.current_token.value == 'if':
                return self.if_statement()
            elif self.current_token.value == 'while':
                return self.while_statement()
        elif self.current_token.type == 'IDENT':
            return self.assignment()
        self.error('Invalid statement')

    def if_statement(self):
        self.eat('KEYWORD')  # 'if'
        condition = self.expression()
        self.eat('KEYWORD')  # 'then'
        true_branch = self.statement()
        false_branch = None
        if self.current_token.value == 'else':
            self.eat('KEYWORD')  # 'else'
            false_branch = self.statement()
        self.eat('KEYWORD')  # 'fi'
        return ('IF', condition, true_branch, false_branch)

    def while_statement(self):
        self.eat('KEYWORD')  # 'while'
        condition = self.expression()
        self.eat('KEYWORD')  # 'do'
        body = self.statement()
        self.eat('KEYWORD')  # 'od'
        return ('WHILE', condition, body)

    def parse(self):
        return self.statement()

if __name__ == '__main__':
    code = """
    if x <= 5 and x != 10 then y <- 10;
    while x >= 100 do x <- x + 1 od;
    """
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    print(result)
