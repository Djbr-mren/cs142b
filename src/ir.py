class IR:
    def __init__(self):
        self.basic_blocks = []

    def __repr__(self):
        return f"IR(basic_blocks={self.basic_blocks})"

class BasicBlock:
    def __init__(self, label):
        self.label = label
        self.instructions = []

    def __repr__(self):
        return f"BasicBlock(label={self.label}, instructions={self.instructions})"

class Instruction:
    def __init__(self, op, *args):
        self.op = op
        self.args = args

    def __repr__(self):
        return f"Instruction(op={self.op}, args={self.args})"
