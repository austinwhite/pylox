from sys import stderr
from typing import List, Any
from lox.tokens import Token, TokenType
from lox.expression import Expression as ExprExpression, Binary, Unary, Literal, Grouping
from lox.statement import Expression as StmtExpression, Statement, Print


class ParseError(RuntimeError):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message

    def error(self) -> None:
        if self.token == TokenType.EOF:
            self.report(f"{self.token.line} at end {self.message}")
        else:
            self.report(
                f"{self.token.line} at ' {self.token.lexeme} ' {self.message}")

    def report(self, message: str) -> None:
        stderr.write(message)


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> None:
        statements = []

        while not self.is_at_end():
            statements.append(self.statement())

        return statements

    def expression(self) -> ExprExpression:
        return self.equality()

    def statement(self) -> Statement:
        if self.match(TokenType.PRINT):
            return self.print_statement()

        return self.expression_statement()

    def print_statement(self) -> Any:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Statement:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return StmtExpression(expr)

    def equality(self) -> ExprExpression:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def match(self, *typs: TokenType) -> bool:
        for typ in typs:
            if self.check(typ):
                self.advance()
                return True

        return False

    def check(self, typ: TokenType) -> bool:
        if self.is_at_end():
            return False

        return self.peek().type == typ

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

    def comparison(self) -> ExprExpression:
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()

            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> ExprExpression:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> ExprExpression:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> ExprExpression:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> ExprExpression:
        if self.match(TokenType.FALSE):
            return Literal(False)
        elif self.match(TokenType.TRUE):
            return Literal(True)
        elif self.match(TokenType.NIL):
            return Literal(None)

        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def consume(self, typ: TokenType, message: str) -> Token:
        if self.check(typ):
            return self.advance()

        raise self.error(self.peek(), message)

    @staticmethod
    def error(token: Token, message: str) -> ParseError:
        err = ParseError(token, message)
        return err

    def synchronize(self) -> None:
        self.advance()

        while not self.is_at_end():
            if self.previous.type == TokenType.SEMICOLON:
                return

            if self.peek().type in (
                TokenType.CLASS,
                TokenType.FUNCTION,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ):
                return

            self.advance()
