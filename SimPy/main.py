from sympy import simplify, srepr, Eq
from latex2sympy2 import latex2sympy, latex2latex
from difflib import SequenceMatcher


def simplify_latex_expression(latex_expr):
    return latex2sympy(latex2latex(latex_expr))

def simplify_sympy_expression(sympy_expr):
    return simplify(sympy_expr.doit().doit())


def compare_latex_expressions(latex_expr1, latex_expr2):
    
    # Convert and simplify expressions
    expr1, expr2 = simplify_latex_expression(latex_expr1), simplify_latex_expression(latex_expr2)

    # Check if the expressions are equal
    equations_are_equal = Eq(expr1, expr2) == True

    return equations_are_equal

def compare_sympy_expressions(sympy_expr1, sympy_expr2):
    
    # Simplify expressions
    expr1, expr2 = simplify_sympy_expression(sympy_expr1), simplify_sympy_expression(sympy_expr2)

    # Check if the expressions are equal
    equations_are_equal = Eq(expr1, expr2) == True

    return equations_are_equal


def simpy_to_tree(sympy_expr):
    return srepr(simplify_sympy_expression(sympy_expr))

def latex_to_tree(latex_expr):
    return srepr(simplify_latex_expression(latex_expr))

def expression_tree_similarity(expr1, expr2):
    # Create trees
    tree1 = srepr(simplify_latex_expression(expr1))
    tree2 = srepr(simplify_latex_expression(expr2))

    # Calculate similarity ratio
    matcher = SequenceMatcher(None, tree1, tree2)
    similarity_ratio = matcher.ratio()

    return similarity_ratio