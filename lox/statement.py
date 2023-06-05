from abc import ABC, abstractmethod
from typing import List
from lox.tokens import Token
from lox.expression import Expression, ExpressionVisitor


__all__ = [
    "StatementVisitor",
    "Statement",
    "Block"
    "Expression"
    "Print"
    "Var"
]

class StatementVisitor(ABC):
    @abstractmethod
    def visit_block_statement(self, statement: 'Expression'):
        pass

    @abstractmethod
    def visit_expression_statement(self, statement: 'Expression'):
        pass

    @abstractmethod
    def visit_print_statement(self, statement: 'Expression'):
        pass

    @abstractmethod
    def visit_var_statement(self, statement: 'Expression'):
        pass


class Statement(ABC):
    @abstractmethod
    def accept(self, visitor: StatementVisitor):
        pass


class Block(Statement):
    def __init__(self, statements: List[Statement]) -> None:
        self.statements = statements

    def accept(self, visitor: StatementVisitor) -> ExpressionVisitor:
        return visitor.visit_block_statement(self)


class Expression(Statement):
    def __init__(self, expression: Expression) -> None:
        self.expression = expression

    def accept(self, visitor: StatementVisitor) -> ExpressionVisitor:
        return visitor.visit_expression_statement(self)


class Print(Statement):
    def __init__(self, expression: Expression) -> None:
        self.expression = expression

    def accept(self, visitor: StatementVisitor) -> ExpressionVisitor:
        return visitor.visit_print_statement(self)


class Var(Statement):
    def __init__(self, name: Token, initializer: Expression) -> None:
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StatementVisitor) -> ExpressionVisitor:
        return visitor.visit_var_statement(self)
