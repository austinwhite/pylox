from lox.expression import Expression, Assign, Binary, Grouping, Literal, Unary, Variable


class AstPrinter:
    def print(self, expression: Expression):
        return expression.accept(self)

    def visit_binary_expression(self, expression: Binary):
        return self.parenthesize(expression.operator.lexeme, expression.left, expression.right)

    def visit_grouping_expression(self, expression: Grouping):
        return self.parenthesize('group', expression.expression)

    def visit_literal_expression(self, expression: Literal):
        return str(expression.value)

    def visit_unary_expression(self, expression: Unary):
        return self.parenthesize(expression.operator.lexeme, expression.right)

    def parenthesize(self, name, *expressions):
        fragments = []
        fragments.append('(')
        fragments.append(name)

        for expression in expressions:
            fragments.append(' ')
            fragments.append(expression.accept(self))
            
        fragments.append(')')

        return ''.join(fragments)
