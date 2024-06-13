from parser import Program, Declaration, Assignment, IfStatement, WhileStatement, ReturnStatement, FunctionCall, Expression
from ir import IR, BasicBlock, Instruction

class IRGenerator:
    def __init__(self):
        self.ir = IR()
        self.current_block = None
        self.block_counter = 0

    def new_block(self):
        label = f"BB{self.block_counter}"
        self.block_counter += 1
        block = BasicBlock(label)
        self.ir.basic_blocks.append(block)
        self.current_block = block
        return block

    def generate(self, node):
        if isinstance(node, Program):
            self.visit_program(node)
        else:
            raise Exception(f"Unsupported node type: {type(node)}")
        return self.ir

    def visit_program(self, node):
        # Initialize the first basic block
        entry_block = self.new_block()
        for decl in node.declarations:
            self.visit(decl)
        for stmt in node.statements:
            self.visit(stmt)
        # Add branch to the first statement
        self.current_block.instructions.append(Instruction('br', 'entry', entry_block.label))

    def visit_declaration(self, node):
        # Declarations are handled separately, so we don't need to do anything here
        pass

    def visit_assignment(self, node):
        self.current_block.instructions.append(
            Instruction('assign', node.var, self.visit(node.expr))
        )

    def visit_if_statement(self, node):
        cond = self.visit(node.condition)
        true_block = self.new_block()
        false_block = self.new_block()
        end_block = self.new_block()

        # Insert the branch instruction at the end of the current block
        self.current_block.instructions.append(Instruction('br', cond, true_block.label, false_block.label))

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

    def visit_function_call_statement(self, node):
        func_call = self.visit_function_call(node)
        self.current_block.instructions.append(func_call)

    def visit_function_call(self, node):
        return Instruction('call', node.func_name, *[self.visit(arg) for arg in node.args])

    def visit_expression(self, node):
        left = self.visit(node.left) if not isinstance(node.left, (str, int)) else node.left
        right = self.visit(node.right) if node.right and not isinstance(node.right, (str, int)) else node.right
        if node.op:
            return Instruction(node.op, left, right)
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
    ast = parser.parse()
    ir_generator = IRGenerator()
    ir = ir_generator.generate(ast)
    print(ir)
