from typing import List

from lox import expressions
from lox.tokens import Token, TokenType
from lox.errors import Error, ParseError


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> expressions.Expr:
        try:
            return self.expression()
        except Exception:
            # Error.parsing_error(self.tokens[self.current], "Error parsing.")
            return None

    def expression(self,) -> expressions.Expr:
        return self.equality()

    def equlity(self) -> expressions.Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def comparison(self) -> expressions.Expr:
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def term(self) -> expressions.Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def factor(self) -> expressions.Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def unary(self) -> expressions.Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            expr = expressions.Unary(operator, right)

        return self.primary()

    def primary(self) -> expressions.Expr:
        if self.match(TokenType.FALSE):
            return self.literal(False)
        elif self.match(TokenType.TRUE):
            return self.literal(True)
        elif self.match(TokenType.NIL):
            return self.literal(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return expressions.Literal(self.previous().literal)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expressions.Grouping(expr)
        
        raise Error.parsing_error(self.peek(), "Expect expression.")

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True

        return False

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()

        Error.parsing_error(self.peek(), message)

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False

        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def synchronize(self) -> None:
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in {
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            }:
                return None

            self.advance()
