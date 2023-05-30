from lox.tokens import Token, TokenType, TokenType as ttype

from lox.errors import Error


class Scanner:
    keywords = {
        "and": ttype.AND,
        "class": ttype.CLASS,
        "else": ttype.ELSE,
        "false": ttype.FALSE,
        "for": ttype.FOR,
        "fun": ttype.FUN,
        "if": ttype.IF,
        "nil": ttype.NIL,
        "or": ttype.OR,
        "print": ttype.PRINT,
        "return": ttype.RETURN,
        "super": ttype.SUPER,
        "this": ttype.THIS,
        "true": ttype.TRUE,
        "var": ttype.VAR,
        "while": ttype.WHILE,
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.errors = []

        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(ttype.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c == "(":
            self.add_token(ttype.LEFT_PAREN)
        elif c == ")":
            self.add_token(ttype.RIGHT_PAREN)
        elif c == "{":
            self.add_token(ttype.LEFT_BRACE)
        elif c == "}":
            self.add_token(ttype.RIGHT_BRACE)
        elif c == ",":
            self.add_token(ttype.COMMA)
        elif c == ".":
            self.add_token(ttype.DOT)
        elif c == "-":
            self.add_token(ttype.MINUS)
        elif c == "+":
            self.add_token(ttype.PLUS)
        elif c == ";":
            self.add_token(ttype.SEMICOLON)
        elif c == "*":
            self.add_token(ttype.STAR)
        elif c == "!":
            if self.match("="):
                self.add_token(ttype.BANG_EQUAL)
            else:
                self.add_token(ttype.BANG)
        elif c == "=":
            if self.match("="):
                self.add_token(ttype.EQUAL_EQUAL)
            else:
                self.add_token(ttype.EQUAL)
        elif c == "<":
            if self.match("="):
                self.add_token(ttype.LESS_EQUAL)
            else:
                self.add_token(ttype.LESS)
        elif c == ">":
            if self.match("="):
                self.add_token(ttype.GREATER_EQUAL)
            else:
                self.add_token(ttype.GREATER)
        elif c == "/":
            if self.match("/"):
                # A comment goes until the end of the line
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(ttype.SLASH)
        elif c in (" ", "\r", "\t"):
            # Ignore whitespace
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.string()
        elif self.is_digit(c):
            self.number()
        elif self.is_alpha(c):
            self.identifier()
        else:
            self.error("Unexpected character.")

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Look for fractional part
        if self.peek() == "." and self.is_digit(self.peek_next()):
            # Consume the '.'
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(ttype.NUMBER, float(
            self.source[self.start: self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        # Unterminated string
        if self.is_at_end():
            self.error("Unterminated string.")
            return

        # The closing "
        self.advance()

        # Trim the surrounding quotes
        value = self.source[self.start + 1: self.current - 1]
        self.add_token(ttype.STRING, value)

    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()

        # See if the identifier is a reserved word
        text = self.source[self.start: self.current]
        type = self.keywords.get(text, ttype.IDENTIFIER)
        self.add_token(type)

    def match(self, expected: str):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.current >= len(self.source):
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_digit(self, c):
        return "0" <= c <= "9"

    def is_alpha(self, c):
        return "a" <= c <= "z" or "A" <= c <= "Z" or c == "_"

    def is_alphanumeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    def is_at_end(self):
        return bool(self.current >= len(self.source))

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal=None):
        text = self.source[self.start: self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def error(self, message):
        error = Error.error(self.line, message)
        self.errors.append(error)
