"""
Very Simple Integer-arithmetic Evaluator


This code is an exercise in parsing arithmetic into a binary expression tree
(https://en.wikipedia.org/wiki/Binary_expression_tree) and then recursively
evaluating that tree. In the evaluation of the tree, this code hands off each
binary arithmetic operation to the built-in operators (+, -, *, and /) in Python.
If you're looking for how to implement the binary operators, you won't find the
answer in this code. If you're curious about binary expression trees and parsing
context-free languages, then hopefully this will be useful.

Also see a very simple JSON parser: https://gist.github.com/py-in-the-sky/02d18c427c07658adf0261a572e442d9


Grammar of Integer Arithmetic:

    integer-arithmetic:  term | term plus-or-minus integer-arithmetic
    term:                factor | factor times-or-divide term
    factor:              integer | ( integer-arithmetic ) | unary-operator factor
    unary-operator:      plus-or-minus
    plus-or-minus:       + | -
    times-or-divide:     * | /
    integer:             \d+


Two simplifications in this arithmetic: integers are the only type of number, and
the exponent operator is not supported.


Exercises for the reader:

1. Change the code to handle floats, in addition to integers.
2. Change the code to handle the exponent '**' binary operator.
3. Read the code and convince yourself that it operates on binary expressions
from left to right while obeying PEMDAS (https://en.wikipedia.org/wiki/Order_of_operations#Mnemonics).
    E.g.: 1 + 2 * 3 + 4 => 1 + 6 + 4 => 7 + 4 => 11
    E.g.: 2 * 3 + 1 * 1 + 5 * (9 + 2 * 5) => 6 + 1 * 1 + 5 * (9 + 2 * 5) => 6 + 1 + 5 * (9 + 2 * 5)
            => 7 + 5 * (9 + 2 * 5) => 7 + 5 * (9 + 10) => 7 + 5 * 19 => 7 + 95 => 102
4. Develop nice validation/error messages, like those in
https://gist.github.com/py-in-the-sky/02d18c427c07658adf0261a572e442d9
5. Debugging tool: develop a `pretty_print` function to print a binary expression tree. E.g.:

    pretty_print(parse('(1 + 2) * 3 + 4'))

                        +
                    /       \
                    *       4
                /       \
                +       3
            /       \
            1       2
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
    if left_expression is None:  # very beginning of integer-arithmetic expression
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
    if left_expression is None:  # very beginning of term
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
    if tokens[i] == '+':  # '+' as unary operator
        return parse_factor(tokens, i+1, positive)
    elif tokens[i] == '-':  # '-' as unary operator
        return parse_factor(tokens, i+1, not positive)
    elif isinstance(tokens[i], int):
        return i+1, tokens[i] if positive else -tokens[i]
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


def evaluate(binary_expression_tree):
    if isinstance(binary_expression_tree, int):
        return binary_expression_tree

    assert isinstance(binary_expression_tree, tuple) and len(binary_expression_tree) in (1, 3)

    if len(binary_expression_tree) == 1:
        return evaluate(binary_expression_tree[0])
    else:
        left_expression = evaluate(binary_expression_tree[0])
        operation = OPERATIONS[binary_expression_tree[1]]
        right_expression = evaluate(binary_expression_tree[2])
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
