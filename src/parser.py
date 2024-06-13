# src/parser.py

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

    def assignment(self):
        self.eat('KEYWORD')  # 'let'
        var = self.current_token
        self.eat('IDENT')
        self.eat('ASSIGN')
        expr = self.expression()
        return ('ASSIGN', var, expr)

    def statement(self):
        print(f'Parsing statement: {self.current_token}')
        if self.current_token.type == 'KEYWORD':
            if self.current_token.value == 'if':
                return self.if_statement()
            elif self.current_token.value == 'while':
                return self.while_statement()
            elif self.current_token.value == 'let':
                return self.assignment()
            elif self.current_token.value == 'call':
                return self.call_statement()
            else:
                self.error(f'Invalid statement keyword: {self.current_token.value}')
        else:
            self.error(f'Invalid statement: {self.current_token}')

    def if_statement(self):
        self.eat('KEYWORD')  # 'if'
        condition = self.expression()
        self.eat('KEYWORD')  # 'then'
        true_branch = self.statement_sequence()
        false_branch = None
        if self.current_token.value == 'else':
            self.eat('KEYWORD')  # 'else'
            false_branch = self.statement_sequence()
        self.eat('KEYWORD')  # 'fi'
        return ('IF', condition, true_branch, false_branch)

    def while_statement(self):
        self.eat('KEYWORD')  # 'while'
        condition = self.expression()
        self.eat('KEYWORD')  # 'do'
        body = self.statement_sequence()
        self.eat('KEYWORD')  # 'od'
        return ('WHILE', condition, body)

    def call_statement(self):
        self.eat('KEYWORD')  # 'call'
        function = self.current_token
        self.eat('IDENT')
        self.eat('LPAREN')
        args = []
        if self.current_token.type != 'RPAREN':
            args.append(self.expression())
            while self.current_token.type == 'COMMA':
                self.eat('COMMA')
                args.append(self.expression())
        self.eat('RPAREN')
        return ('CALL', function, args)

    def statement_sequence(self):
        statements = []
        while self.current_token.type != 'EOF' and not (self.current_token.type == 'KEYWORD' and self.current_token.value in ('else', 'fi', 'od')):
            print(f'Parsing statement in sequence: {self.current_token}')
            statement = self.statement()
            statements.append(statement)
            if self.current_token.type == 'SEMICOLON':
                self.eat('SEMICOLON')
        return statements

    def parse(self):
        return self.program()

    def program(self):
        self.eat('KEYWORD')  # 'main'
        var_decls = self.var_declarations()
        self.eat('LBRACE')
        statements = self.statement_sequence()
        self.eat('RBRACE')
        self.eat('END')
        return ('PROGRAM', var_decls, statements)

    def var_declarations(self):
        declarations = []
        while self.current_token.type == 'KEYWORD' and self.current_token.value == 'var':
            self.eat('KEYWORD')  # 'var'
            var = self.current_token
            self.eat('IDENT')
            declarations.append(var)
            if self.current_token.type == 'COMMA':
                self.eat('COMMA')
        self.eat('SEMICOLON')
        return declarations

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

    def relation(self):
        node = self.term()
        while self.current_token.type == 'REL_OP':
            token = self.current_token
            self.eat('REL_OP')
            node = (token, node, self.term())
        return node

    def logical_expr(self):
        node = self.relation()
        while self.current_token.type == 'KEYWORD' and self.current_token.value in ('and', 'or'):
            token = self.current_token
            self.eat('KEYWORD')
            node = (token, node, self.relation())
        return node

    def expression(self):
        node = self.logical_expr()
        while self.current_token.type in ('OP', 'ADD', 'SUB'):
            token = self.current_token
            if token.type == 'OP':
                self.eat('OP')
            node = (token, node, self.logical_expr())
        return node

if __name__ == '__main__':
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
    parser = Parser(tokens)
    result = parser.parse()
    print(result)
