from tokenizer import Tokenizer

class Node:
    pass

class Program(Node):
    def __init__(self, declarations, functions, statements):
        self.declarations = declarations
        self.functions = functions
        self.statements = statements

    def __repr__(self):
        return f"Program(declarations={self.declarations}, functions={self.functions}, statements={self.statements})"

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

class WhileStatement(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStatement(condition={self.condition}, body={self.body})"

class ReturnStatement(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"ReturnStatement(expr={self.expr})"

class FunctionCall(Node):
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f"FunctionCall(func_name={self.func_name}, args={self.args})"

class FunctionDeclaration(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDeclaration(name={self.name}, params={self.params}, body={self.body})"

class Expression(Node):
    def __init__(self, left, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        if self.op:
            return f"Expression(left={self.left}, op={self.op}, right={self.right})"
        else:
            return f"Expression(value={self.left})"

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
        declarations = self.declarations()
        functions = self.functions()
        self.eat('KEYWORD')  # 'main'
        self.eat('LBRACE')
        statements = self.statement_sequence()
        self.eat('RBRACE')
        self.eat('END')
        return Program(declarations, functions, statements)

    def declarations(self):
        declarations = []
        while self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'var':
            self.eat('KEYWORD')
            while self.current_token.type == 'IDENT':
                var = self.current_token.value
                self.eat('IDENT')
                if self.current_token.type == 'COMMA':
                    self.eat('COMMA')
                else:
                    break
            self.eat('SEMICOLON')
            declarations.append(Declaration(var))
        return declarations

    def functions(self):
        functions = []
        while self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'function':
            functions.append(self.function_declaration())
        return functions

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
            elif self.current_token.value == 'return':
                return self.return_statement()
            elif self.current_token.value == 'function':
                return self.function_declaration()
        self.error(f"Invalid statement: {self.current_token}")

    def assignment(self):
        self.eat('KEYWORD')  # 'let'
        var = self.current_token.value
        self.eat('IDENT')
        self.eat('ASSIGN')
        expr = self.expression()
        return Assignment(var, expr)

    def if_statement(self):
        self.eat('KEYWORD')  # 'if'
        condition = self.relation()
        self.eat('KEYWORD')  # 'then'
        true_branch = self.statement_sequence()
        false_branch = []
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'else':
            self.eat('KEYWORD')
            false_branch = self.statement_sequence()
        self.eat('KEYWORD')  # 'fi'
        return IfStatement(condition, true_branch, false_branch)

    def while_statement(self):
        self.eat('KEYWORD')  # 'while'
        condition = self.relation()
        self.eat('KEYWORD')  # 'do'
        body = self.statement_sequence()
        self.eat('KEYWORD')  # 'od'
        return WhileStatement(condition, body)

    def return_statement(self):
        self.eat('KEYWORD')  # 'return'
        expr = None
        if self.current_token.type != 'SEMICOLON':
            expr = self.expression()
        return ReturnStatement(expr)

    def function_call_statement(self):
        func_call = self.function_call()
        return func_call

    def function_call(self):
        self.eat('KEYWORD')  # 'call'
        func_name = self.current_token.value
        self.eat('IDENT')
        self.eat('LPAREN')
        args = []
        if self.current_token.type != 'RPAREN':
            args.append(self.expression())
            while self.current_token.type == 'COMMA':
                self.eat('COMMA')
                args.append(self.expression())
        self.eat('RPAREN')
        return FunctionCall(func_name, args)

    def function_declaration(self):
        self.eat('KEYWORD')  # 'function'
        name = self.current_token.value
        self.eat('IDENT')
        params = self.formal_params()
        self.eat('SEMICOLON')
        body = self.func_body()
        self.eat('SEMICOLON')
        return FunctionDeclaration(name, params, body)

    def formal_params(self):
        params = []
        self.eat('LPAREN')
        if self.current_token.type != 'RPAREN':
            params.append(self.current_token.value)
            self.eat('IDENT')
            while self.current_token.type == 'COMMA':
                self.eat('COMMA')
                params.append(self.current_token.value)
                self.eat('IDENT')
        self.eat('RPAREN')
        return params

    def func_body(self):
        var_decls = []
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'var':
            var_decls = self.parse_var_decls()
        self.eat('LBRACE')
        statements = self.parse_stat_sequence()
        self.eat('RBRACE')
        return var_decls, statements

    def parse_var_decls(self):
        var_decls = []
        self.eat('KEYWORD')  # 'var'
        var_decls.append(self.current_token.value)
        self.eat('IDENT')
        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            var_decls.append(self.current_token.value)
            self.eat('IDENT')
        self.eat('SEMICOLON')
        return var_decls

    def parse_stat_sequence(self):
        statements = []
        statements.append(self.parse_statement())
        while self.current_token.type == 'SEMICOLON':
            self.eat('SEMICOLON')
            if self.current_token.type == 'RBRACE':
                break
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        if self.current_token.type == 'KEYWORD':
            if self.current_token.value == 'let':
                return self.assignment()
            elif self.current_token.value == 'if':
                return self.if_statement()
            elif self.current_token.value == 'call':
                return self.function_call_statement()
            elif self.current_token.value == 'while':
                return self.while_statement()
            elif self.current_token.value == 'return':
                return self.return_statement()
            elif self.current_token.value == 'function':
                return self.function_declaration()
        self.error(f"Invalid statement: {self.current_token}")

    def expression(self):
        left = self.term()
        while self.current_token and self.current_token.type == 'OP':
            op = self.current_token.value
            self.eat('OP')
            right = self.term()
            left = Expression(left, op, right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token and self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.factor()
            left = Expression(left, op, right)
        return left

    def factor(self):
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
            self.error(f"Invalid factor: {token}")

    def relation(self):
        left = self.expression()
        if self.current_token.type == 'REL_OP':
            op = self.current_token.value
            self.eat('REL_OP')
            right = self.expression()
            return Expression(left, op, right)
        else:
            self.error(f"Invalid relation: {self.current_token}")

if __name__ == '__main__':
    code = """
    function foo(a, b) {
        let c <- a + b;
        return c
    };
    main
    var x; {
        let x <- call foo(1, 2);
        call OutputNum(x)
    }.
    """
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    print(result)
