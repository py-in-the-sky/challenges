"""
Very Simple Integer-arithmetic Evaluator

Two simplifications: integers are the only type of number in the inputs,
and the exponential operation is not supported. It is left as an exercise
to the reader to add support for floats and the exponential operation.

Grammar

    integer-arithmetic:  term | term plus-or-minus integer-arithmetic
    term:                factor | factor times-or-divide term
    factor:              integer | ( integer-arithmetic ) | unary-operator factor
    unary-operator:      plus-or-minus
    plus-or-minus:       + | -
    times-or-divide:     * | /
    integer:             \d+

TODOs:
    * nice invalid-expression error/message, as in the very simple JSON parser
    * post as a gist
"""


from __future__ import division
import operator as op
import re


### Top-level

def evaluate_arithmetic(arithmetic_expression):
    return compose(tokenize, parse, evaluate)(arithmetic_expression)
    # For readability of this file, we define `evaluate_arithmetic` at the top of the file,
    # but doing so requires us to dynamically create `compose(evaluate, parse, tokenize)`
    # every time `evaluate_arithmetic` is called. We could define `evaluate_arithmetic` at the
    # bottom of the file by simply doing:
    # `evaluate_arithmetic = compose(tokenize, parse, evaluate)`.


### Util

def compose(*functions_from_innermost_to_outermost):
    def _f(x):
        return reduce(lambda val,f: f(val), functions_from_innermost_to_outermost, x)

    return _f


### Tokenize

INTEGER_PATTERN = r'\d+'
OPERATOR_TOKENS = r'[*/+-]'
PARENTHESES_TOKENS = r'[()]'
TOKENS_PATTERN = r'({integer_pattern}|{operator_tokens}|{parentheses_tokens})'.format(
    integer_pattern=INTEGER_PATTERN,
    operator_tokens=OPERATOR_TOKENS,
    parentheses_tokens=PARENTHESES_TOKENS
)
TOKEN_RE = re.compile(TOKENS_PATTERN)


def tokenize(arithmetic_expression):
    return tuple(atom(s) for s in TOKEN_RE.findall(arithmetic_expression))


def atom(string):
    try:
        return int(string)
    except ValueError:
        return string


### Parse

def parse(tokens):
    return parse_integer_arithmetic(tokens)[1]


def parse_integer_arithmetic(tokens, i=0, negate_first_term=False):
    i, left_term = parse_term(tokens, i)

    if negate_first_term:
        left_term = (-1, '*', left_term)

    if i == len(tokens) or tokens[i] == ')':
        return i, left_term

    assert tokens[i] in '+-'

    i, remaining_expression = parse_integer_arithmetic(tokens, i+1, tokens[i] == '-')
    return i, (left_term, '+', remaining_expression)


def parse_term(tokens, i=0, take_reciprocal_of_first_factor=False):
    i, left_term = parse_factor(tokens, i)

    if take_reciprocal_of_first_factor:
        left_term = (1, '/', left_term)

    if i == len(tokens) or tokens[i] in '+-)':
        return i, left_term

    assert tokens[i] in '*/'

    i, remaining_term = parse_term(tokens, i+1, tokens[i] == '/')
    return i, (left_term, '*', remaining_term)


def parse_factor(tokens, i=0):
    if tokens[i] in tuple('+-'):
        t = tokens[i]
        i, factor = parse_factor(tokens, i+1)
        return i, (1 if t == '+' else -1, '*', factor)
    elif tokens[i] == '(':
        i, factor = parse_integer_arithmetic(tokens, i+1)
        assert tokens[i] == ')'
        return i+1, factor
    else:
        assert isinstance(tokens[i], int)
        return i+1, tokens[i]


### Evaluate

OPERATIONS = {
    '+': op.add,
    '*': op.mul,
    '/': lambda a,b: a / b  # `op.div` is not influenced by `from __future__ import division`
}


def evaluate(arithmetic_tree):
    if isinstance(arithmetic_tree, int):
        return arithmetic_tree

    assert isinstance(arithmetic_tree, tuple) and len(arithmetic_tree) in (1, 3)

    if len(arithmetic_tree) == 1:
        return evaluate(arithmetic_tree[0])
    else:
        left_expression = evaluate(arithmetic_tree[0])
        operation = OPERATIONS[arithmetic_tree[1]]
        right_expression = evaluate(arithmetic_tree[2])
        return operation(left_expression, right_expression)


### Test

import random


COIN = HEADS, TAILS = True, False
BINARY_OPERATORS = '+-*/'
UNARY_OPERATORS = '+-'
EXPRESSION_TYPES = INT, PARENTHETIC, UNARY = ('int', 'parenthetic', 'unary')


def generate_integer_arithmetic(recursion_depth=0):
    expr1 = generate_expression(recursion_depth+1)

    if recursion_depth < 10 and flip_coin() is HEADS:
        binary_operator = random.choice(BINARY_OPERATORS)
        expr2 = generate_integer_arithmetic(recursion_depth+1)
        return ' '.join([expr1, binary_operator, expr2])
    else:
        return expr1


def generate_expression(recursion_depth):
    expression_type = random.choice(EXPRESSION_TYPES)

    if expression_type is INT:
        return generate_int()
    elif expression_type is PARENTHETIC:
        return '(' + generate_integer_arithmetic(recursion_depth+1) + ')'
    else:
        return random.choice(UNARY_OPERATORS) + generate_expression(recursion_depth+1)


def generate_int():
    first_digit = random.choice('123456789')
    random_digit = lambda: random.choice('0123456789')
    return first_digit + ''.join(random_digit() for _ in xrange(random.randint(0, 5)))


def flip_coin():
    return random.choice(COIN)


def tests():
    random_cases = [generate_integer_arithmetic() for _ in xrange(1000)]
    hard_coded_cases = [
        '4 / 2 * 3 + 4 - 6',
        '2 * -2',
        '2 - 2',
        '4 / 2 * (3 + 4) - 6',
        '-23 / ((4 - 6) * (20 + 202 - 8) / 4) / 3 * 3405 * 3 / 5 / 6 / -7 - 908',
        '-23 / ((4 - 6) * (20 + 202 - 8) / 4) / 3 * 3405 * 3 / 5 / -(-(3 + 3)) / -(3 + 4 + -10/-10) - 908',
        '(2)',
        '1/2/2',
        '-2 + -2',
        '(-2 + -2)',
        '-(-2 + -2)',
        '-(1 + 1) + -(1 + 1)',
        '1 -1',
        '1-1',
        '4*3-1*5*5/5'
    ]

    for case in random_cases + hard_coded_cases:
        try:
            # print
            # Why use `str` for the actual and expected evaluations? Due to rounding errors,
            # my evaluator's answers diverge from Python's with very large and very small
            # numbers. `str` rounds both large and small numbers, using scientific notation.
            # We use `str` as a sort of rounding function.
            actual_eval = str(evaluate_arithmetic(case))
            expected_eval = str(eval(case))
            # print case, '=', actual_eval, '(actual)', '=', expected_eval, '(expected)'
            assert actual_eval == expected_eval
        except ZeroDivisionError:
            pass

    print
    print 'Tests pass!'


if __name__ == '__main__':
    tests()
