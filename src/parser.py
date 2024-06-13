from tokenizer import Tokenizer, Token

class Node:
    pass

class Program(Node):
    def __init__(self, declarations, statements):
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        return f"Program(declarations={self.declarations}, statements={self.statements})"

class Declaration(Node):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"Declaration(var={self.var})"

class Assignment(Node):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __repr__(self):
        return f"Assignment(var={self.var}, expr={self.expr})"

class IfStatement(Node):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f"IfStatement(condition={self.condition}, true_branch={self.true_branch}, false_branch={self.false_branch})"

class FunctionCall(Node):
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f"FunctionCall(func_name={self.func_name}, args={self.args})"

class Expression(Node):
    def __init__(self, left, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        if self.op:
            return f"Expression({self.left} {self.op} {self.right})"
        else:
            return f"Expression({self.left})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.next_token()

    def next_token(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def error(self, message):
        raise Exception(f"Error parsing input: {message}")

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.next_token()
        else:
            self.error(f"Expected token {token_type}, got {self.current_token}")

    def parse(self):
        return self.program()

    def program(self):
        self.eat('KEYWORD')  # 'main'
        declarations = self.declarations()
        self.eat('LBRACE')
        statements = self.statement_sequence()
        self.eat('RBRACE')
        self.eat('END')
        return Program(declarations, statements)

    def declarations(self):
        declarations = []
        while self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'var':
            self.eat('KEYWORD')
            declarations.append(self.declaration())
        return declarations

    def declaration(self):
        var = self.current_token.value
        self.eat('IDENT')
        self.eat('SEMICOLON')
        return Declaration(var)

    def statement_sequence(self):
        statements = []
        while self.current_token and self.current_token.type not in ('RBRACE', 'END', 'KEYWORD') or (self.current_token.type == 'KEYWORD' and self.current_token.value not in ('else', 'fi', 'od')):
            statements.append(self.statement())
            if self.current_token and self.current_token.type == 'SEMICOLON':
                self.eat('SEMICOLON')
        return statements

    def statement(self):
        if self.current_token.type == 'KEYWORD':
            if self.current_token.value == 'let':
                return self.assignment()
            elif self.current_token.value == 'if':
                return self.if_statement()
            elif self.current_token.value == 'call':
                return self.function_call_statement()
            elif self.current_token.value == 'while':
                return self.while_statement()
        self.error(f"Invalid statement: {self.current_token}")

    def assignment(self):
        self.eat('KEYWORD')
        var = self.current_token.value
        self.eat('IDENT')
        self.eat('ASSIGN')
        expr = self.expression()
        return Assignment(var, expr)

    def if_statement(self):
        self.eat('KEYWORD')
        condition = self.expression()
        self.eat('KEYWORD')  # 'then'
        true_branch = self.statement_sequence()
        false_branch = []
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'else':
            self.eat('KEYWORD')
            false_branch = self.statement_sequence()
        self.eat('KEYWORD')  # 'fi'
        return IfStatement(condition, true_branch, false_branch)

    def while_statement(self):
        self.eat('KEYWORD')
        condition = self.expression()
        self.eat('KEYWORD')  # 'do'
        body = self.statement_sequence()
        self.eat('KEYWORD')  # 'od'
        return WhileStatement(condition, body)

    def function_call_statement(self):
        func_call = self.function_call()
        return FunctionCall(func_call.func_name, func_call.args)

    def function_call(self):
        self.eat('KEYWORD')
        func_name = self.current_token.value
        self.eat('IDENT')
        self.eat('LPAREN')
        args = []
        while self.current_token.type != 'RPAREN':
            args.append(self.expression())
            if self.current_token.type == 'COMMA':
                self.eat('COMMA')
        self.eat('RPAREN')
        return FunctionCall(func_name, args)

    def expression(self):
        left = self.term()
        while self.current_token and self.current_token.type in ('OP', 'REL_OP'):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.term()
            left = Expression(left, op, right)
        return left

    def term(self):
        token = self.current_token
        if token.type == 'IDENT':
            self.eat('IDENT')
            return token.value
        elif token.type == 'NUMBER':
            self.eat('NUMBER')
            return token.value
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.expression()
            self.eat('RPAREN')
            return expr
        elif token.type == 'KEYWORD' and token.value == 'call':
            return self.function_call()
        else:
            self.error(f"Invalid term: {self.current_token}")

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
    parser = Parser(tokens)
    result = parser.parse()
    print(result)

