import json
import copy
from typing import Tuple
import networkx as nx
import matplotlib.pyplot as plt
import random
import sympy as sp
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.readwrite import json_graph
import pandas as pd

import decimal

#util range func to generate decimals
def drange(x, y, jump):
  while x < y:
    yield float(x)
    x += decimal.Decimal(jump)


OPERATIONS = ["ADD", "MUL", "FUNC", "POW"] # TODO: remove sub and instead increase chances of negative 1 in literals
FUNCTIONS = ["SIN", "COS", "TAN", "EXP", "LOG", "f", "g", "h"] # TODO: if we want to deal with functions with multiple arguments we might aswell include basic operations..
ATOMICS = ["LITERAL", "VARIABLE"]
VARIABLE_ALPHABET = [chr(x) for x in range(ord("a"), ord("z")+1) if chr(x) not in ["f", "g", "h"]]
literal_atomics = [x for x in drange(-100,100, "0.2") if x != 0]
pow_range = literal_atomics = list(drange(-10,10, "0.5"))

# an expression is described by a node


# class Node:
#     type=""

def expand_expression(expr_root):
    op = random.choice(OPERATIONS)
    resulting_node = {}
    if op == "FUNC":
        resulting_node = {"type": "OPERATION", "subtype": "FUNC", "function": random.choice(FUNCTIONS), "argument": expr_root} # TODO: keep track of previously used literals and repeat them for higher prob
    elif op == "POW":
        resulting_node = {"type": "OPERATION", "subtype": "POW", "left": expr_root, "right": create_atomic("LITERAL",random.choice(pow_range))} # TODO: keep track of previously used literals and repeat them for higher prob
    else:
        expr_rhs_type = random.choice(ATOMICS)
        if expr_rhs_type == "VARIABLE":
            resulting_node = {"type": "OPERATION", "subtype": "ARITHMETIC", "op": op, "left":expr_root, "right": create_atomic("VARIABLE", random.choice(VARIABLE_ALPHABET))} # TODO: keep track of previously used literals and repeat them for higher prob
        else:
            resulting_node = {"type": "OPERATION", "subtype": "ARITHMETIC", "op": op, "left":expr_root,"right": create_atomic("LITERAL",random.choice(literal_atomics))} # TODO: keep track of previously used literals and repeat them for higher prob
            
    return resulting_node

def create_atomic(type, val):
    if type == "VARIABLE": 
        return {"type": "ATOMIC", "subtype":"VARIABLE", "val": val}
    else:
        return {"type": "ATOMIC", "subtype":"LITERAL", "val": val}

def create_expression(length: int):
    root_node = create_atomic("VARIABLE", random.choice(VARIABLE_ALPHABET))
    for i in range(length):
        root_node = expand_expression(root_node)
    return root_node


def expression_to_graph(expr, graph=None,  id=1):
    if graph is None:
        graph = nx.DiGraph()
    if expr['type'] == 'ATOMIC':
        graph.add_node(id, val=str(expr['val']))
    elif expr['type'] == 'OPERATION':
        op_type = expr['subtype']
        if op_type in ['ARITHMETIC', 'POW']:
            op = expr['op'] if op_type == 'ARITHMETIC' else op_type
            graph.add_node(id, val=op)
            graph.add_edge(id, 2*id+1 )
            expression_to_graph(expr['right'], graph, id=2*id+1)
            graph.add_edge(id, 2*id+2)
            expression_to_graph(expr['left'], graph, id=2*id+2)
        elif op_type == "FUNC":
            graph.add_node(id, val=expr["function"])
            graph.add_edge(id, 2*id+1)
            expression_to_graph(expr['argument'], graph, id=2*id+1)         
    return graph


def expression_to_sympy(expr, eval=False):
    if expr['type'] == 'ATOMIC':
        if expr["subtype"] == "VARIABLE":
            return sp.Symbol(expr['val'])
        else:
            return expr['val']
    elif expr['type'] == 'OPERATION':
        op_type = expr['subtype']
        if op_type in ['ARITHMETIC', 'POW']:
            op = expr['op'] if op_type == 'ARITHMETIC' else 'POW'
            left_expr = expression_to_sympy(expr['left'])
            right_expr = expression_to_sympy(expr['right'])
            if op == "ADD":
                return sp.Add(left_expr, right_expr, evaluate= eval)
            elif op == "MUL":
                return sp.Mul(left_expr, right_expr, evaluate= eval)
            elif op == "POW":
                return sp.Pow(left_expr, right_expr, evaluate= eval)
        elif op_type == "FUNC":
            func_name = expr["function"].lower()
            argument_expr = expression_to_sympy(expr['argument'])
            if func_name == 'sin':
                return sp.sin(argument_expr)
            elif func_name == 'cos':
                return sp.cos(argument_expr)
            elif func_name == 'tan':
                return sp.tan(argument_expr)
            elif func_name == 'exp':
                return sp.exp(argument_expr)
            elif func_name == 'log':
                return sp.log(argument_expr)
            elif func_name in ['f', 'g', 'h']:
                return sp.Function(func_name)(argument_expr)



def randomize_literals(expr, max_num_changes=4):
    curr_changes = 0
    def traverse_and_randomize(node):
        nonlocal curr_changes
        if curr_changes >= max_num_changes:
            return
        if node['type'] == 'ATOMIC' and node['subtype'] == 'LITERAL':
            node['val'] += random.uniform(-10, 10)
            curr_changes += 1
        elif node['type'] == 'OPERATION' and node["subtype"] in ["ARITHMETIC", "POW"]:
            if node['subtype'] == 'POW':
                traverse_and_randomize(node['left'])
            else:
                traverse_and_randomize(node['left'])
                traverse_and_randomize(node['right'])
        elif node['type'] == 'OPERATION' and node['subtype'] == 'FUNC':
            traverse_and_randomize(node['argument'])

    traverse_and_randomize(expr)


def flip_signs(expr, max_num_changes = 4):
    curr_changes = 0
    def traverse_and_randomize(node):
        nonlocal curr_changes
        if curr_changes >= max_num_changes:
            return node
        if node['type'] == 'ATOMIC' and node['subtype'] == 'LITERAL': # TODO: for variables change this into a multiplication node
            node['val'] = -node['val']
            curr_changes += 1
        elif node["type"] == "ATOMIC" and node["subtype"] == "VARIABLE": 
            original_value = node["val"]
            node = {"type": "OPERATION", "subtype": "ARITHMETIC", "op": "MUL", "left":create_atomic("LITERAL", -1), "right": create_atomic("VARIABLE", original_value)} # TODO: Do the same thing with a probability for divisions and with different proportions 
            curr_changes += 1
        elif node['type'] == 'OPERATION' and node["subtype"] in ["ARITHMETIC", "POW"]:
                node["left"] = traverse_and_randomize(node['left'])
                node["right"] = traverse_and_randomize(node['right'])
        elif node['type'] == 'OPERATION' and node['subtype'] == 'FUNC':
            node["argument"] = traverse_and_randomize(node['argument'])
        
        return node
    expr = traverse_and_randomize(expr)
    
def equivalent_literals(expr, max_num_changes = 2):
    curr_changes = 0
    def traverse_and_randomize(node):
        nonlocal curr_changes
        if curr_changes >= max_num_changes:
            return node
        if node['type'] == 'ATOMIC' and node['subtype'] == 'LITERAL':
            original_value = node['val']
            node = {"type": "OPERATION", "subtype": "ARITHMETIC", "op": "ADD", "left":create_atomic("LITERAL", original_value/2), "right": create_atomic("LITERAL", original_value/2)} # TODO: Do the same thing with a probability for divisions and with different proportions 
            curr_changes += 1
        elif node['type'] == 'OPERATION' and node["subtype"] in ["ARITHMETIC", "POW"]:
            if node['subtype'] == 'POW':
                node['left'] = traverse_and_randomize(node['left'])
            else:
                node['left'] = traverse_and_randomize(node['left'])
                node['right'] = traverse_and_randomize(node['right'])
        elif node['type'] == 'OPERATION' and node['subtype'] == 'FUNC':
            node['argument'] = traverse_and_randomize(node['argument'])
        return node
    traverse_and_randomize(expr)

"""
generate dataset either as csv if latex option or as an array of json objects {expr_l, expr_r, score}
    size: number of total samples / 4
    expr_len_range: Tuple[int,int] with min expr length and max expr length
    representation_type: Enum["Graph","Latex"], this also determines if we're saving an object array or csv
    filepath: str
"""
def generate_dataset(size,filepath, expr_len_range=(3,16), representation_type="Graph"): 
    output_data = []
    if representation_type=="Graph":
        for l in range(*expr_len_range):
            for _ in range(size//(expr_len_range[1] - expr_len_range[0])):
                expr = create_expression(l)
                for alt in expression_alterations:
                    alt_expr = copy.deepcopy(expr)
                    alt["func"](alt_expr)
                    output_data.append({"expr_l": json_graph.tree_data(expression_to_graph(expr), root=1), "expr_r": json_graph.tree_data(expression_to_graph(alt_expr), root=1), "score": alt["score"]})

        with open(filepath, "w") as f:
            json.dump(output_data, f, indent=4)
    else: #Latex
        for l in range(*expr_len_range):
            for _ in range(size//(expr_len_range[1] - expr_len_range[0])):
                expr = create_expression(l)
                for alt in expression_alterations:
                    alt_expr = copy.deepcopy(expr)
                    alt["func"](alt_expr)
                    # print("EXPRESSION : \n", expr, "\n----------------------------------------------\n")
                    # print("ALT EXPRESSION : \n", alt_expr, "\n----------------------------------------------\n")
                    output_data.append({"expr_l": sp.latex(expression_to_sympy(expr)), "expr_r":  sp.latex(expression_to_sympy(alt_expr)), "score": alt["score"]})
                output_data.append({"expr_l":  sp.latex(expression_to_sympy(expr)), "expr_r": sp.latex(expression_to_sympy(expr, eval=True)), "score": 0})

        gen_df = pd.DataFrame(output_data)
        gen_df.to_csv(filepath)
    

# Correct alterations always have a score of 0
expression_alterations = [{"func": flip_signs, "score": 8}, {"func": randomize_literals, "score":24}, {"func":equivalent_literals, "score":0}] # TODO: Make score dependent on the number of changes in the data alteration


"""
Perform a number of random alterations to an expression, the return the new expression alongside with a score for the distance dist(original, altered)
"""
def alter_expression(max_num_alterations = 3) -> Tuple[dict, int]: 
    return ({}, 0) 


def render_expression_repr_to_file(expr, filename):
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    graph = expression_to_graph(expr)
    pos = graphviz_layout(graph, prog="dot")
    # Draw the graph
    nx.draw(graph,pos=pos, with_labels=True, labels=nx.get_node_attributes(graph, "val"), font_weight='bold', node_size=900, node_color='black', font_color='white', font_size=10)
    plt.savefig(filename)
    plt.close(fig)
# Example usage:
# expression = create_expression(8)
# print(expression_to_sympy(expression))
# render_expression_repr_to_file(expression, "orig.png")
# equivalent_literals(expression)
# print(expression_to_sympy(expression))
# render_expression_repr_to_file(expression, "changed.png")

generate_dataset(130,"test_datagen.csv", representation_type="Latex")