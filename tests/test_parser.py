# tests/test_parser.py

import unittest
from tokenizer import Tokenizer
from parser import Parser


class TestParser(unittest.TestCase):

    def test_parse(self):
        code = """
        if x <= 5 and x != 10 then y <- 10;
        while x >= 100 do x <- x + 1 od;
        """
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        result = parser.parse()
        expected_result = [
            (
                'IF',
                ('and',
                 ('<=', ('IDENT', 'x', 2, 8), ('NUMBER', '5', 2, 13)),
                 ('!=', ('IDENT', 'x', 2, 19), ('NUMBER', '10', 2, 24))
                 ),
                [('ASSIGN', ('IDENT', 'y', 2, 32), ('NUMBER', '10', 2, 37))],
                None
            ),
            (
                'WHILE',
                ('>=', ('IDENT', 'x', 3, 11), ('NUMBER', '100', 3, 16)),
                [('ASSIGN', ('IDENT', 'x', 3, 23),
                  ('+', ('IDENT', 'x', 3, 28), ('NUMBER', '1', 3, 32)))]
            )
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
