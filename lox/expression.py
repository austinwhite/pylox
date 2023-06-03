from abc import ABC, abstractmethod
from lox.tokens import Token
from typing import Any


__all__ = [
    "ExpressionVisitor",
    "Expression",
    "Assign"
    "Binary"
    "Grouping"
    "Literal"
    "Unary"
    "Variable"
]

class ExpressionVisitor(ABC):
    @abstractmethod
    def visit_assign_expression(self, expression: 'Expression'):
        pass

    @abstractmethod
    def visit_binary_expression(self, expression: 'Expression'):
        pass

    @abstractmethod
    def visit_grouping_expression(self, expression: 'Expression'):
        pass

    @abstractmethod
    def visit_literal_expression(self, expression: 'Expression'):
        pass

    @abstractmethod
    def visit_unary_expression(self, expression: 'Expression'):
        pass

    @abstractmethod
    def visit_variable_expression(self, expression: 'Expression'):
        pass


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor: ExpressionVisitor):
        pass


class Assign(Expression):
    def __init__(self, name: Token, value: Expression) -> None:
        self.name = name
        self.value = value

    def accept(self, visitor: ExpressionVisitor) -> ExpressionVisitor:
        return visitor.visit_assign_expression(self)


class Binary(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExpressionVisitor) -> ExpressionVisitor:
        return visitor.visit_binary_expression(self)


class Grouping(Expression):
    def __init__(self, expression: Expression) -> None:
        self.expression = expression

    def accept(self, visitor: ExpressionVisitor) -> ExpressionVisitor:
        return visitor.visit_grouping_expression(self)


class Literal(Expression):
    def __init__(self, value: Any) -> None:
        self.value = value

    def accept(self, visitor: ExpressionVisitor) -> ExpressionVisitor:
        return visitor.visit_literal_expression(self)


class Unary(Expression):
    def __init__(self, operator: Token, right: Expression) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExpressionVisitor) -> ExpressionVisitor:
        return visitor.visit_unary_expression(self)


class Variable(Expression):
    def __init__(self, name: Token) -> None:
        self.name = name

    def accept(self, visitor: ExpressionVisitor) -> ExpressionVisitor:
        return visitor.visit_variable_expression(self)
