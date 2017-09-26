# First iteration. Slower and not entirely correct.

from operator import add, mul, div, sub


OPERATIONS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': div
}


def eval_expression(expression):
    return eval_tree(parse_expression(expression))


def eval_tree(node):
    if isinstance(node, NumberNode):
        return node.value
    else:  # isintance(node, OperationNode)
        left_value = eval_tree(node.left)
        right_value = eval_tree(node.right)
        return node.operation(left_value, right_value)


def parse_expression(expression):
    operator_index = (first_top_level_index(expression, '+-') or
                      first_top_level_index(expression, '*/'))

    if operator_index:
        # TODO: instead of slicing strings, which is expensive for large strings
        # due to the allocation of a new character array, come up with a way
        # to pass substring bounds.
        left_child = parse_expression(expression[:operator_index])
        right_child = parse_expression(expression[operator_index+1:])
        operator_character = expression[operator_index]
        operator = OPERATIONS[operator_character]
        return OperationNode(operator, left_child, right_child)
    elif '(' == expression[0]:  # expression is "(arithmetic)"
        return parse_expression(expression[1:-1])
    else:  # expression is an integer
        return NumberNode(int(expression))


def first_top_level_index(string, chars):
    stack = []

    for i,c in enumerate(string):
        if c in chars and not stack:
            # `not stack` means we're not inside a nested expression (not within parentheses)
            return i
        elif c == '(':
            stack.append(c)
        elif c == ')':
            stack.pop()


class NumberNode:
    def __init__(self, value):
        self.value = value


class OperationNode:
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right
