from sympy.core.basic import Basic
from sympy import simplify, srepr, Eq
from latex2sympy2 import latex2sympy, latex2latex

from difflib import SequenceMatcher

import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity


class TreeNode:

    def __init__(self, label):
        if isinstance(label, Basic):
            self.label = label._class.name_
        else:
            self.label = label
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def build_tree(expr, parent=None):

    if isinstance(expr, Basic):
        if expr.is_Atom:
            node = TreeNode(str(expr))
        else:
            node = TreeNode(expr.func)  
            for arg in expr.args:
                child_node = build_tree(arg, node)
                node.add_child(child_node)
    else:
        node = TreeNode(str(expr))

    return node


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

def get_tree_sequence_similarity(tree1, tree2):
    matcher = SequenceMatcher(None, tree1, tree2)
    return matcher.ratio()


def get_bert_embeddings(expr, model, tokenizer):
    tokens = tokenizer(expr, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**tokens)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings

def get_text_similarity(embeddings1, embeddings2):
    return cosine_similarity([embeddings1], [embeddings2])[0][0]