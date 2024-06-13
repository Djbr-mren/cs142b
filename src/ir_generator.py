from parser import Program, Declaration, Assignment, IfStatement, WhileStatement, ReturnStatement, FunctionCall, Expression, FunctionDeclaration
from ir import IR, BasicBlock, Instruction

class IRGenerator:
    def __init__(self):
        self.ir = IR()
        self.current_block = None
        self.block_counter = 0
        self.temp_counter = 0
        self.functions = {}

    def new_block(self):
        label = f"BB{self.block_counter}"
        self.block_counter += 1
        block = BasicBlock(label)
        self.ir.basic_blocks.append(block)
        self.current_block = block
        return block

    def new_temp(self):
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_name

    def generate(self, node):
        if isinstance(node, Program):
            self.visit_program(node)
        else:
            raise Exception(f"Unsupported node type: {type(node)}")
        return self.ir

    def visit_program(self, node):
        self.new_block()
        for decl in node.declarations:
            self.visit(decl)
        for stmt in node.statements:
            self.visit(stmt)

    def visit_declaration(self, node):
        pass

    def visit_assignment(self, node):
        expr_result = self.visit(node.expr)
        self.current_block.instructions.append(
            Instruction('assign', node.var, expr_result)
        )

    def visit_if_statement(self, node):
        cond_value = self.visit_expression(node.condition)
        cond_temp = self.new_temp()
        self.current_block.instructions.append(Instruction('assign', cond_temp, cond_value))
        true_block = self.new_block()
        false_block = self.new_block()
        end_block = self.new_block()

        self.current_block.instructions.append(Instruction('br', cond_temp, true_block.label, false_block.label))

        self.current_block = true_block
        for stmt in node.true_branch:
            self.visit(stmt)
        self.current_block.instructions.append(Instruction('jmp', end_block.label))

        self.current_block = false_block
        for stmt in node.false_branch:
            self.visit(stmt)
        self.current_block.instructions.append(Instruction('jmp', end_block.label))

        self.current_block = end_block

    def visit_while_statement(self, node):
        cond_block = self.new_block()
        body_block = self.new_block()
        end_block = self.new_block()

        self.current_block.instructions.append(Instruction('jmp', cond_block.label))

        self.current_block = cond_block
        cond = self.visit(node.condition)
        self.current_block.instructions.append(Instruction('br', cond, body_block.label, end_block.label))

        self.current_block = body_block
        for stmt in node.body:
            self.visit(stmt)
        self.current_block.instructions.append(Instruction('jmp', cond_block.label))

        self.current_block = end_block

    def visit_return_statement(self, node):
        self.current_block.instructions.append(
            Instruction('ret', self.visit(node.expr) if node.expr else None)
        )

    def visit_function_declaration(self, node):
        entry_block = self.new_block()
        self.functions[node.name] = entry_block
        self.current_block = entry_block
        for param in node.params:
            param_var = self.new_temp()
            self.current_block.instructions.append(Instruction('param', param, param_var))
        for stmt in node.body[1]:  # Body statements
            self.visit(stmt)
        self.current_block.instructions.append(Instruction('ret'))

    def visit_function_call(self, node):
        args = [self.visit(arg) for arg in node.args]
        call_instr = Instruction('call', node.func_name, *args)
        self.current_block.instructions.append(call_instr)
        return call_instr

    def visit_expression(self, node):
        left = self.visit(node.left) if not isinstance(node.left, (str, int)) else node.left
        right = self.visit(node.right) if node.right and not isinstance(node.right, (str, int)) else node.right
        if node.op:
            temp_var = self.new_temp()
            self.current_block.instructions.append(Instruction('assign', temp_var, Instruction(node.op, left, right)))
            return temp_var
        else:
            return node.left

    def visit(self, node):
        if isinstance(node, Declaration):
            self.visit_declaration(node)
        elif isinstance(node, Assignment):
            self.visit_assignment(node)
        elif isinstance(node, IfStatement):
            self.visit_if_statement(node)
        elif isinstance(node, WhileStatement):
            self.visit_while_statement(node)
        elif isinstance(node, ReturnStatement):
            self.visit_return_statement(node)
        elif isinstance(node, FunctionCall):
            return self.visit_function_call(node)
        elif isinstance(node, FunctionDeclaration):
            self.visit_function_declaration(node)
        elif isinstance(node, Expression):
            return self.visit_expression(node)
        elif isinstance(node, (str, int)):
            return node
        else:
            raise Exception(f"Unsupported node type: {type(node)}")

if __name__ == '__main__':
    from parser import Parser
    from tokenizer import Tokenizer

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
    ast = parser.parse()
    ir_generator = IRGenerator()
    ir = ir_generator.generate(ast)
    print(ir)
