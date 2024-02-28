import unittest
from sympy import symbols, diff, integrate, limit
from main import compare_latex_expressions

class TestExpressionComparison(unittest.TestCase):

    def test_derivative(self):
        x = symbols('x')
        expr1 = r"\frac{d}{dx}(x^2)"
        expr2 = r"2*x"
        self.assertTrue(compare_latex_expressions(expr1, expr2))
        
    def test_sum_subtraction(self):
        x, y = symbols('x y')
        expr1 = r"x + y - 1"
        expr2 = r"y + x - 1 + 2 - 2"
        self.assertTrue(compare_latex_expressions(expr1, expr2))
        
    def test_division(self):
        x = symbols('x')
        expr1 = r"\frac{x}{x}"
        expr2 = r"1"
        self.assertTrue(compare_latex_expressions(expr1, expr2))

    def test_integration(self):
        x = symbols('x')
        expr1 = r"\int x^2 \,dx"
        expr2 = r"\frac{x^3}{3}"
        self.assertTrue(compare_latex_expressions(expr1, expr2))

    def test_complex_expression(self):
        x = symbols('x')
        expr1 = r"\frac{d}{dx}(x^2 + 2*x) \times \int x \,dx"
        expr2 = r"x^3 + x^2"
        self.assertTrue(compare_latex_expressions(expr1, expr2))

    def test_limit_subtraction(self):
        x = symbols('x')
        expr1 = r"\lim_{x \to 0} (x - x^2)"
        expr2 = r"0"
        self.assertTrue(compare_latex_expressions(expr1, expr2))

    def test_derivative_division(self):
        x = symbols('x')
        expr1 = r"\frac{d}{dx}\left(\frac{x^2}{x}\right)"
        expr2 = r"1"
        self.assertTrue(compare_latex_expressions(expr1, expr2))

    def test_integration_limit(self):
        x = symbols('x')
        expr1 = r"\int_{0}^{1} x \,dx"
        expr2 = r"\frac{1}{2}"
        self.assertTrue(compare_latex_expressions(expr1, expr2))

    def test_complex_limit(self):
        x = symbols('x')
        expr1 = r"\lim_{x \to \infty} \frac{x^2 + 2x + 1}{x^2 - 1}"
        expr2 = r"1"
        self.assertTrue(compare_latex_expressions(expr1, expr2))

    def test_derivative_sum(self):
        x, y = symbols('x y')
        expr1 = r"\frac{d}{dx}(x + y)"
        expr2 = r"1"
        self.assertTrue(compare_latex_expressions(expr1, expr2))

if __name__ == '__main__':
    unittest.main()