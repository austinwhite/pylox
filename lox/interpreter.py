from typing import Any
from lox.tokens import Token, TokenType
from lox.expression import Expression, ExpressionVisitor, Literal, Grouping, Unary, Binary, Assign, Variable


class LoxRuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()


class Interpreter(Expression):
    def interpret(self, expr: Expression):
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except RuntimeError as error:
            raise LoxRuntimeError(error)

    def accept(self, visitor: ExpressionVisitor):
        return super().accept(visitor)

    def visit_literal_expression(self, expr: Literal) -> Any:
        return expr.value

    def visit_unary_expression(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                return float(right) * -1
            case TokenType.BANG:
                return not self.truthy(right)

        # Unreachable
        return None

    def visit_grouping_expression(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def visit_assign_expression(self, expr: Assign) -> Any:
        return None

    def visit_variable_expression(self, expr: Variable) -> Any:
        return None

    def visit_binary_expression(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return self.floaty(left) + self.floaty(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return self.is_string(left) + self.is_string(right)
                raise LoxRuntimeError(
                    expr.operator, 'Cannot add a number and a string.')
            case TokenType.MINUS:
                return self.floaty(left) - self.floaty(right)
            case TokenType.SLASH:
                return self.floaty(left) / self.floaty(right)
            case TokenType.STAR:
                return self.floaty(left) * self.floaty(right)
            case TokenType.GREATER:
                return self.floaty(left) > self.floaty(right)
            case TokenType.GREATER_EQUAL:
                return self.floaty(left) >= self.floaty(right)
            case TokenType.LESS:
                return self.floaty(left) < self.floaty(right)
            case TokenType.LESS_EQUAL:
                return self.floaty(left) <= self.floaty(right)
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right

        # Unreachable
        return None

    def evaluate(self, expr: Expression) -> Any:
        return expr.accept(self)

    def truthy(self, value: Any) -> bool:
        # false & nil are falsey, anything else is truthy
        if value is None or value is False:
            return False

    def floaty(self, value: Any) -> float:
        # lox only supports floating point numbers, implicitly any number
        #     must be a float
        if type(value) == float:
            return value

        raise TypeError

    def stringy(self, value: Any) -> str:
        if type(value) == str:
            return value

        raise TypeError

    def stringify(self, value):
        if value is None:
            return 'nil'
        text = str(value)
        if isinstance(value, float) and text.endswith('.0'):
            return text[:-2]
        if isinstance(value, bool):
            return text.lower()
        return text
