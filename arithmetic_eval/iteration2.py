"""
1*2/3*4+5-6+8 = 1*2*(1/3)*4+5+(-1*6)+8
4-6+8         = 4+(-1*6)+8
4-6*8+2       = 4+(-1*6*8)+2
4-(6*8+2)+100 = 4+(-1*(6*8+2))+100
-1*(1+2)

Turn division into multiplication by a ratio, and turn subtraction into
addition of a negatively valued term.

Inspired by json_parser/parse_even_faster.py.
"""


from __future__ import division
from operator import mul
from timeit import timeit


DIGITS = '1234567890'


product = lambda numbers: reduce(mul, numbers, 1)


def eval_expression(arithmetic_string):
    addition_node, i = parse(arithmetic_string, 0)

    assert i == len(arithmetic_string)  # Whole string has been parsed.
    assert isinstance(addition_node, AdditionNode)

    return addition_node.calculate()


def parse(s, i):
    "Parses the string from i and returns an AdditionNode."
    assert i < len(s), 'String or substring must not be empty'

    addition_node = AdditionNode()

    while i < len(s) and s[i] != ')':
        node, i = parse_term(s, i)
        addition_node.add_term(node)

    assert i == len(s) or s[i] == ')'

    return addition_node, (i if i == len(s) else i+1)


def parse_term(s, i):
    first_char = s[i]

    if first_char == '-':
        node, i = parse_term(s, i+1)
        return MultiplicationNode(NumberNode(-1), node), i
    elif first_char == '+':
        return parse_term(s, i+1)

    assert first_char in DIGITS+'('

    multiplication_node = MultiplicationNode()

    while i < len(s) and s[i] not in '+-)':
        node, i = parse_factor(s, i)
        multiplication_node.add_factor(node)

    return multiplication_node, i


def parse_factor(s, i):
    first_char = s[i]

    if first_char == '(':
        assert s[i+1] in DIGITS+'-('
        return parse(s, i+1)
    elif first_char == '*':
        assert s[i+1] in DIGITS+'-('
        return parse_factor(s, i+1)
    elif first_char == '/':
        assert s[i+1] in DIGITS+'-('
        node, i = parse_factor(s, i+1)
        return DivisionNode(NumberNode(1), node), i
    elif first_char == '-':
        node, i = parse_factor(s, i+1)
        return MultiplicationNode(NumberNode(-1), node), i
    elif first_char in DIGITS:
        return parse_integer(s, i)
    else:
        assert False, 'Invalid arithmetic'


def parse_integer(s, i):
    j = i

    while j < len(s) and s[j] in DIGITS:
        j += 1

    return NumberNode(int(s[i:j])), j


class AdditionNode:
    def __init__(self, *terms):
        self.terms = list(terms)

    def add_term(self, node):
        self.terms.append(node)

    def calculate(self):
        return sum(n.calculate() for n in self.terms)


class MultiplicationNode:
    def __init__(self, *factors):
        self.factors = list(factors)

    def add_factor(self, node):
        self.factors.append(node)

    def calculate(self):
        return product(n.calculate() for n in self.factors)


class DivisionNode:
    def __init__(self, numerator_node, denominator_node):
        self.numerator_node = numerator_node
        self.denominator_node = denominator_node

    def calculate(self):
        return self.numerator_node.calculate() / self.denominator_node.calculate()


class NumberNode:
    def __init__(self, number):
        self.number = number

    def calculate(self):
        return self.number


CASES = """
    1*2/3*4+5-6+8
    4-6+8
    4-6*8+2
    1*1
    1*2*3/4+5
    -1*2
    -1+2
    405
    4-(6*8+2)+100
    -1*(1+2)*3
    (1+1)
    2/(1-1*-1)+3
    2/(-1-1)
    (1+(3*-(4+20)*-19999)+305*-100000)
    ((1+(3*-(4+2)+3)-(-1*8))/(4+5*7))
    (((1))*((((2)))))
    1*-2+3
"""


PARSED_CASES = (s.strip() for s in CASES.split('\n') if s.strip())


def tests():
    for case in PARSED_CASES:
        actual = eval_expression(case)
        expected = eval(case)
        assert actual == expected, 'case: {}; actual: {}; expected: {}'.format(case, actual, expected)

    print 'Tests pass!'


def timing():
    n = 1000000
    timing_template = 'for case in PARSED_CASES: {}(case)'
    setup = 'from __main__ import PARSED_CASES, eval_expression'
    print 'eval_expression:', timeit(timing_template.format('eval_expression'), setup=setup, number=n)
    print 'eval:           ', timeit(timing_template.format('eval'), setup=setup, number=n)


if __name__ == '__main__':
    timing()
    tests()
    timing()
