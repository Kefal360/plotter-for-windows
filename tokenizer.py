from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

from operation import functions, operators
from pars_types import Token, TokenType


@dataclass
class Tokenizer:
    """
    Implements an iterator that yields `Token`s one by one.
    It's grammatics is context-sensitive, but respects only a
    single previous token.
    """

    expression: str

    def __iter__(self) -> Generator[TokenType, None, None]:
        accumulator = ""
        prev = None

        for ch in self.expression:
            if (breaker_type := Tokenizer.is_breaker(ch)) is not None:
                if len(accumulator) > 0:
                    # ch is `(` after function name
                    if breaker_type == Token.LBrace and Tokenizer.is_function(
                        accumulator
                    ):
                        yield accumulator, Token.Function
                        prev = Token.Function
                        accumulator = ""
                    else:
                        value, token_type = Tokenizer.detect_number(accumulator)
                        yield value, token_type
                        prev = token_type
                        accumulator = ""

                        # `(` after variable or number
                        if breaker_type == Token.LBrace:
                            yield "*", Token.Operator
                            prev = Token.Operator

                # Unary minus case
                if ch == "-" and (prev == Token.LBrace or prev is None):
                    yield 0, Token.Number
                    prev = Token.Number

                # `(expr)(expr)` case
                if breaker_type == Token.LBrace and prev == Token.RBrace:
                    yield "*", Token.Operator
                    prev = Token.Operator

                if breaker_type != Token.Space:
                    yield ch, breaker_type
                    prev = breaker_type
            else:
                # Variable or function name after braced expr or variable and space
                if prev == Token.RBrace or prev == Token.Variable:
                    yield "*", Token.Operator
                    prev = Token.Operator

                # Floating point number
                if ch in ",.":
                    accumulator += "."
                    continue

                # Variable or function name after number
                if (
                    not ch.isdecimal()
                    and (num := Tokenizer.is_number(accumulator)) is not None
                ):
                    yield num, Token.Number
                    yield "*", Token.Operator
                    prev = Token.Operator
                    accumulator = ""

                accumulator += ch
        if len(accumulator) > 0:
            yield self.detect_number(accumulator)

    @staticmethod
    def is_breaker(character) -> Optional[Token]:
        if character in operators:
            return Token.Operator
        if character in "([{":
            return Token.LBrace
        if character in ")]}":
            return Token.RBrace
        if character == " ":
            return Token.Space

        return None

    @staticmethod
    def is_number(string) -> Optional[float]:
        try:
            return float(string)
        except ValueError:
            return None

    @staticmethod
    def detect_number(string) -> TokenType:
        if (num := Tokenizer.is_number(string)) is not None:
            return num, Token.Number
        else:
            return string, Token.Variable

    @staticmethod
    def is_function(lexeme: str) -> bool:
        if lexeme in functions:
            return True

        return False
