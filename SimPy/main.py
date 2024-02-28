from sympy import simplify, Eq
from latex2sympy2 import latex2sympy, latex2latex


def simplify_latex_expression(latex_expr):

    return latex2sympy(latex2latex(latex_expr))


def simplify_sympy_expression(sympy_expr):
    
    return simplify(sympy_expr.doit().doit())


def compare_latex_expressions(latex_expr1, latex_expr2):
    
    # Convert and simplify expressions
    expr1, expr2 = simplify_latex_expression(latex_expr1), simplify_latex_expression(latex_expr2)

    # Check if the expressions are equal
    equations_are_equal = Eq(expr1, expr2)

    return equations_are_equal


def compare_sympy_expressions(sympy_expr1, sympy_expr2):
    
    # Simplify expressions
    expr1, expr2 = simplify_sympy_expression(sympy_expr1), simplify_sympy_expression(sympy_expr2)

    # Check if the expressions are equal
    equations_are_equal = Eq(expr1, expr2)

    return equations_are_equal