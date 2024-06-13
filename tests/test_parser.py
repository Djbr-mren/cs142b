import unittest
from tokenizer import Tokenizer
from parser import Parser, Program, Declaration, Assignment, IfStatement, FunctionCall, Expression


class TestParser(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_parse(self):
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

        expected_result = Program(
            declarations = [Declaration(var = 'x')],
            statements = [
                Assignment(var = 'x', expr = FunctionCall(func_name = 'InputNum', args = [])),
                IfStatement(
                    condition = Expression(left = 'x', op = '==', right = '1'),
                    true_branch = [Assignment(var = 'x', expr = '1')],
                    false_branch = [Assignment(var = 'x', expr = '2')]
                ),
                FunctionCall(func_name = 'OutputNum', args = ['x'])
            ]
        )
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
