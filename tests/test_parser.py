# tests/test_parser.py

import unittest
from tokenizer import Tokenizer
from parser import Parser


class TestParser(unittest.TestCase):

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
        expected_result = (
            'PROGRAM',
            [('IDENT', 'x', 3, 13)],
            [
                ('ASSIGN', ('IDENT', 'x', 5, 17), ('CALL', ('IDENT', 'InputNum', 5, 25), [])),
                ('IF',
                 ('==', ('IDENT', 'x', 6, 12), ('NUMBER', '1', 6, 17)),
                 [('ASSIGN', ('IDENT', 'x', 7, 17), ('NUMBER', '1', 7, 23))],
                 [('ASSIGN', ('IDENT', 'x', 9, 17), ('NUMBER', '2', 9, 23))]
                 ),
                ('CALL', ('IDENT', 'OutputNum', 11, 13), [('IDENT', 'x', 11, 23)])
            ]
        )
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
