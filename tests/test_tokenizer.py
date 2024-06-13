import unittest
from tokenizer import Tokenizer, Token


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_tokenize(self):
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
        expected_tokens = [
            Token('KEYWORD', 'main', 2, 8),
            Token('KEYWORD', 'var', 3, 8),
            Token('IDENT', 'x', 3, 12),
            Token('SEMICOLON', ';', 3, 13),
            Token('LBRACE', '{', 3, 15),
            Token('KEYWORD', 'let', 4, 12),
            Token('IDENT', 'x', 4, 16),
            Token('ASSIGN', '<-', 4, 18),
            Token('KEYWORD', 'call', 4, 21),
            Token('IDENT', 'InputNum', 4, 26),
            Token('LPAREN', '(', 4, 34),
            Token('RPAREN', ')', 4, 35),
            Token('SEMICOLON', ';', 4, 36),
            Token('KEYWORD', 'if', 5, 12),
            Token('IDENT', 'x', 5, 15),
            Token('REL_OP', '==', 5, 17),
            Token('NUMBER', 1, 5, 20),
            Token('KEYWORD', 'then', 5, 22),
            Token('KEYWORD', 'let', 6, 16),
            Token('IDENT', 'x', 6, 20),
            Token('ASSIGN', '<-', 6, 22),
            Token('NUMBER', 1, 6, 25),
            Token('KEYWORD', 'else', 7, 12),
            Token('KEYWORD', 'let', 8, 16),
            Token('IDENT', 'x', 8, 20),
            Token('ASSIGN', '<-', 8, 22),
            Token('NUMBER', 2, 8, 25),
            Token('KEYWORD', 'fi', 9, 12),
            Token('SEMICOLON', ';', 9, 14),
            Token('KEYWORD', 'call', 10, 12),
            Token('IDENT', 'OutputNum', 10, 17),
            Token('LPAREN', '(', 10, 26),
            Token('IDENT', 'x', 10, 27),
            Token('RPAREN', ')', 10, 28),
            Token('RBRACE', '}', 11, 8),
            Token('END', '.', 11, 9)
        ]
        expected_tuples = [(token.type, token.value, token.line, token.column) for token in
                           expected_tokens]
        actual_tuples = [(token.type, token.value, token.line, token.column) for token in tokens]
        self.assertEqual(actual_tuples, expected_tuples)


if __name__ == '__main__':
    unittest.main()



