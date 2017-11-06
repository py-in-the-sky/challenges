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
    * comment on how parsing results in a binary arithmetic tree that leads to
      left-to-right evaluation of the terms/factors
    * post as a gist
"""


from __future__ import division  # Also works when this import is commented out.
import operator as op
import re


### Top-level
# For readability of this file, we define `evaluate_arithmetic` at the top of the file,
# but doing so requires us to dynamically create `compose(evaluate, parse, tokenize)`
# every time `evaluate_arithmetic` is called. We could define `evaluate_arithmetic` at the
# bottom of the file by simply doing: `evaluate_arithmetic = compose(tokenize, parse, evaluate)`.

def evaluate_arithmetic(arithmetic_expression):
    return compose(tokenize, parse, evaluate)(arithmetic_expression)


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


def parse_integer_arithmetic(tokens, i=0, left_expression=None):
    if left_expression is None:  # very beginning
        i, int_arithmetic = parse_term(tokens, i)
        return parse_integer_arithmetic(tokens, i, int_arithmetic)
    elif i == len(tokens) or tokens[i] == ')':  # very end
        return i, left_expression
    else:  # middle
        assert tokens[i] in '+-'
        operator = tokens[i]
        i, next_term = parse_term(tokens, i+1)
        int_arithmetic = (left_expression, operator, next_term)
        return parse_integer_arithmetic(tokens, i, int_arithmetic)


def parse_term(tokens, i=0, left_expression=None):
    if left_expression is None:  # very beginning
        i, term = parse_factor(tokens, i)
        return parse_term(tokens, i, term)
    elif i == len(tokens) or tokens[i] in '+-)':  # very end
        return i, left_expression
    else:  # middle
        assert tokens[i] in '*/' and left_expression is not None
        operator = tokens[i]
        i, next_factor = parse_factor(tokens, i+1)
        term = (left_expression, operator, next_factor)
        return parse_term(tokens, i, term)


def parse_factor(tokens, i=0, positive=True):
    if isinstance(tokens[i], int):
        return i+1, tokens[i] if positive else -tokens[i]
    elif tokens[i] == '+':  # '+' as unary operator
        return parse_factor(tokens, i+1, positive)
    elif tokens[i] == '-':  # '-' as unary operator
        return parse_factor(tokens, i+1, not positive)
    else:
        assert tokens[i] == '('
        i, factor = parse_integer_arithmetic(tokens, i+1)
        assert tokens[i] == ')'
        return i+1, factor if positive else (-1, '*', factor)


### Evaluate

OPERATIONS = {
    '+': op.add,
    '-': op.sub,
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
coin_flip = lambda: random.choice(COIN)

BINARY_OPERATORS = '+-*/'
UNARY_OPERATORS = '+-'
EXPRESSION_TYPES = INT, PARENTHETIC, UNARY = (1, 2, 3)


def generate_integer_arithmetic(recursion_depth=0):
    factor = generate_factor(recursion_depth+1)

    # We don't need separate functions for generating terms and factors,
    # so just choose any binary operator; no need to limit the choice to
    # just '+-' or '*/'.

    if recursion_depth < 10 and coin_flip() is HEADS:
        binary_operator = random.choice(BINARY_OPERATORS)
        int_arithmetic = generate_integer_arithmetic(recursion_depth+1)
        return ' '.join([factor, binary_operator, int_arithmetic])
    else:
        return factor


def generate_factor(recursion_depth):
    expression_type = random.choice(EXPRESSION_TYPES)

    if expression_type is INT or recursion_depth > 9:
        return generate_integer()
    elif expression_type is PARENTHETIC:
        return '(' + generate_integer_arithmetic(recursion_depth+1) + ')'
    else:  # UNARY
        return random.choice(UNARY_OPERATORS) + generate_factor(recursion_depth+1)


def generate_integer():
    first_digit = random.choice('123456789')
    random_digit = lambda: random.choice('0123456789')
    return first_digit + ''.join(random_digit() for _ in xrange(random.randint(0, 9)))


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
        '4*3-1*5*5/5',
        '4032 / 7040083',
    ]

    for case in random_cases + hard_coded_cases:
        try:
            print
            actual_eval = evaluate_arithmetic(case)
            expected_eval = eval(case)
            print case, '=', actual_eval, '(actual)', '=', expected_eval, '(expected)'
            assert actual_eval == expected_eval
        except ZeroDivisionError:
            print 'Division by zero in random case: {}'.format(case)

    print
    print 'Tests pass!'


if __name__ == '__main__':
    tests()
