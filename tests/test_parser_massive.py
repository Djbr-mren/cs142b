import unittest
from tokenizer import Tokenizer
from parser import Parser, Program, Declaration, Assignment, IfStatement, WhileStatement, ReturnStatement, FunctionCall, Expression

class TestParserMassive(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            {
                "input": """
                main
                var x, y; {
                    let x <- 1;
                    let y <- 1;
                    let x <- x + y
                }.
                """,
                "expected": "Program(declarations=[Declaration(var=x), Declaration(var=y)], statements=[Assignment(var=x, expr=1), Assignment(var=y, expr=1), Assignment(var=x, expr=Expression(left=x, op=+, right=y))])"
            },
            {
                "input": """
                main
                var x; {
                    let x <- 1 + 1 + 1;
                    call OutputNum(x)
                }.
                """,
                "expected": "Program(declarations=[Declaration(var=x)], statements=[Assignment(var=x, expr=Expression(left=Expression(left=Expression(left=1, op=+, right=1), op=+, right=1))), FunctionCall(func_name=OutputNum, args=[x])])"
            },
            {
                "input": """
                main
                var a; {
                    let a <- call InputNum() + call InputNum();
                    call OutputNum(a)
                }.
                """,
                "expected": "Program(declarations=[Declaration(var=a)], statements=[Assignment(var=a, expr=Expression(left=FunctionCall(func_name=InputNum, args=[]), op=+, right=FunctionCall(func_name=InputNum, args=[]))), FunctionCall(func_name=OutputNum, args=[a])])"
            },
            {
                "input": """
                main
                var a; {
                    let a <- call InputNum() * call InputNum();
                    call OutputNum(a)
                }.
                """,
                "expected": "Program(declarations=[Declaration(var=a)], statements=[Assignment(var=a, expr=Expression(left=FunctionCall(func_name=InputNum, args=[]), op=*, right=FunctionCall(func_name=InputNum, args=[]))), FunctionCall(func_name=OutputNum, args=[a])])"
            },
            {
                "input": """
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
                """,
                "expected": "Program(declarations=[Declaration(var=x)], statements=[Assignment(var=x, expr=FunctionCall(func_name=InputNum, args=[])), IfStatement(condition=Expression(left=x, op===, right=1), true_branch=[Assignment(var=x, expr=1)], false_branch=[Assignment(var=x, expr=2)]), FunctionCall(func_name=OutputNum, args=[x])])"
            },
            # Add more test cases as needed...
        ]

    def test_parser(self):
        for case in self.test_cases:
            tokenizer = Tokenizer(case["input"])
            tokens = tokenizer.tokenize()
            parser = Parser(tokens)
            result = parser.parse()
            self.assertEqual(repr(result), case["expected"])

if __name__ == '__main__':
    unittest.main()
