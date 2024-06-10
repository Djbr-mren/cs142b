# tests/test_tokenizer.py

import unittest
from src.tokenizer import Tokenizer, Token


class TestTokenizer(unittest.TestCase):

    def test_tokenize(self):
        code = "let x <- 5 + 3;"
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        expected_tokens = [
            Token('KEYWORD', 'let', 1, 1),
            Token('IDENT', 'x', 1, 5),
            Token('ASSIGN', '<-', 1, 7),
            Token('NUMBER', '5', 1, 10),
            Token('OP', '+', 1, 12),
            Token('NUMBER', '3', 1, 14),
            Token('SEMICOLON', ';', 1, 15),
        ]
        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
