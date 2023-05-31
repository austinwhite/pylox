from sys import stderr

from lox.tokens import Token, TokenType

class ParseError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message

    def report(self):
        if self.token.type == TokenType.EOF:
            return f'[line {self.token.line}] Error at end: {self.message}'
        else:
            where = self.token.lexeme
            return f"[line {self.token.line}] Error at '{where}': {self.message}"

class Error:
    errors = []
    had_error = False

    @staticmethod
    def error(line_number: int, message: str) -> None:
        Error.report(line_number, "", message)

    @staticmethod
    def report(line_number: int, where: str, message: str) -> None:
        print("[line " + str(line_number) + "] Error" +
              where + ": " + message, file=stderr)
        
    @classmethod
    def parsing_error(cls, token: Token, message: str) -> ParseError:
        err = ParseError(token, message)
        cls.errors.append(err)
        return err
