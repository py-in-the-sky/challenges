"""
Simplification: all subtraction operations are converted to addition of
a negated term (e.g., `1-2*2+3` becomes `1+(-1)*(2*2)+3`). Therefore, we
have no subtraction operations in our binary expression tree. Similarly,
all division operations are converted to multiplication of the reciprocal
of the factor (e.g., `1/2*3` becomes `1*(1/2)*3`). Therefore, we have no
division nodes in our binary expression tree.

See futher discussion of binary expression trees in the docstring for
`parse_expression`.
"""


from __future__ import division
from operator import add, mul
from timeit import timeit


DIGITS = '1234567890'


def eval_arithmetic_expression(arithmetic_expression_string):
    arithmetic_node, i = parse_expression(arithmetic_expression_string)
    assert i == len(arithmetic_expression_string), invalid_arithmetic_expression(s, i)  # Whole string has been parsed.
    return arithmetic_node.calculate()


def parse_expression(s, i=0, negative_first_term=False):
    """Returns a binary expression tree created from the arithmetic expression
    encoded in the string s. The leaf nodes of the tree are integers, and all
    other nodes are arithmetic operations.

    See: https://en.wikipedia.org/wiki/Binary_expression_tree
    """
    left_node, i = parse_term(s, i)

    if negative_first_term:
        left_node = negate(left_node)

    assert i == len(s) or s[i] in '+-)', invalid_arithmetic_expression(s, i)

    if i == len(s) or s[i] == ')':
        return left_node, i
    elif s[i] in '+-':
        right_node, i = parse_expression(s, i+1, s[i] == '-')
        return AdditionNode(left_node, right_node), i


def parse_term(s, i, take_reciprocal_of_first_factor=False):
    left_node, i = parse_factor(s, i)

    if take_reciprocal_of_first_factor:
        left_node = ReciprocalNode(left_node)

    assert i == len(s) or s[i] in '+-*/)', invalid_arithmetic_expression(s, i)

    if i == len(s) or s[i] in '+-)':
        return left_node, i
    elif s[i] in '*/':
        right_node, i = parse_term(s, i+1, s[i] == '/')
        return MultiplicationNode(left_node, right_node), i


def parse_factor(s, i):
    # All possible fators: positive and negated integers, and
    # positive and negated parenthetic expressions.

    assert s[i] in DIGITS+'-(', invalid_arithmetic_expression(s, i)

    if s[i] == '-':
        assert s[i+1] in DIGITS+'(', invalid_arithmetic_expression(s, i+1)
        node, i = parse_factor(s, i+1)
        return negate(node), i
    elif s[i] in DIGITS:
        return parse_integer(s, i)
    else:  # s[i] == '('
        node, i = parse_expression(s, i+1)
        assert s[i] == ')', 'Invalid arithmetic expression'
        return node, i+1


def parse_integer(s, i):
    j = next((j for j in xrange(i+1, len(s)) if s[j] not in DIGITS), len(s))
    return NumberNode(int(s[i:j])), j


def negate(node):
    return MultiplicationNode(NumberNode(-1), node)


class OperationNode:
    def __init__(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node

    def calculate(self):
        return self.operation(self.left_node.calculate(), self.right_node.calculate())


class AdditionNode(OperationNode):
    operation = add


class MultiplicationNode(OperationNode):
    operation = mul


class ReciprocalNode:
    def __init__(self, denominator_node):
        self.denominator_node = denominator_node

    def calculate(self):
        return 1 / self.denominator_node.calculate()


class NumberNode:
    def __init__(self, number):
        self.number = number

    def calculate(self):
        return self.number


def invalid_arithmetic_expression(s, i):
    assertion_error_length = len('AssertionError: ')
    caret = ' ' * (i + assertion_error_length) + '^'
    message_line_1 = 'Invalid arithmetic expression. Unexpected token found: {}'.format(s)
    message_line_2 = '                                                       {}'.format(caret)
    return '{}\n{}'.format(message_line_1, message_line_2)


CASES = """
    4-(6*8+2)+100
    -1*(1+2)*3
    (1+1)
    2/(1-1*-1)+3
    2/(-1-1)
    (1+(3*-(4+20)*-19999)+305*-100000)
    ((1+(3*-(4+2)+3)-(-1*8))/(4+5*7))
    (((1))*((((2)))))
    (1)
    -(1)
    1*2/3*4+5-6+8
    4-6+8
    4-6*8+2
    1*1
    1*2*3/4+5
    -1*2
    -1+2
    405
    1*-2+3
"""


PARSED_CASES = (s.strip() for s in CASES.split('\n') if s.strip())


def tests():
    for case in PARSED_CASES:
        actual = eval_arithmetic_expression(case)
        expected = eval(case)
        assert actual == expected, 'case: {}; actual: {}; expected: {}'.format(case, actual, expected)

    print 'Tests pass!'


def timing():
    n = 1000000
    timing_template = 'for case in PARSED_CASES: {}(case)'
    setup = 'from __main__ import PARSED_CASES, eval_arithmetic_expression; from iteration2 import eval_expression'
    print 'eval_arithmetic_expression:', timeit(timing_template.format('eval_arithmetic_expression'), setup=setup, number=n)
    print 'eval_expression:           ', timeit(timing_template.format('eval_expression'), setup=setup, number=n)
    print 'eval:                      ', timeit(timing_template.format('eval'), setup=setup, number=n)


if __name__ == '__main__':
    timing()
    tests()
    timing()
