from lox import expressions
from lox.tokens import Token, TokenType


class AstPrinter(expressions.ExprVisitor):
    def print(self, expr: expressions.Expr):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: expressions.Expr) -> str:
        content = ' '.join(expr.accept(self) for expr in exprs)

        return f'({name} {content})'

    def visit_binary_expr(self, expr: expressions.Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: expressions.Grouping) -> str:
        return self.parenthesize('group', expr.expression)

    def visit_literal_expr(self, expr: expressions.Literal) -> str:
        return str(expr.value)

    def visit_unary_expr(self, expr: expressions.Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)
