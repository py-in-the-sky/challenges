from __future__ import division
import re
import operator as op


### Top-level

def evaluate_arithmetic(arithmetic_expression):
    return evaluate(parse(rewrite(tokenize(arithmetic_expression)))[1])


### Ancillary

integer_pattern = r'-?\d+'
arithmetic_tokens = r'[()*/+-]'
token_re = re.compile(r'(^{integer_pattern}|(?<=\D){integer_pattern}|{arithmetic_tokens})'.format(
    integer_pattern=integer_pattern,
    arithmetic_tokens=arithmetic_tokens
))


def tokenize(arithmetic_expression):
    return (atom(s) for s in token_re.findall(arithmetic_expression))


def atom(string):
    try:
        return int(string)
    except ValueError:
        return string


def rewrite(tokens):
    return tuple(t2 for t in tokens for t2 in rewrite_rules.get(t, (t,)))


rewrite_rules = {
    '-': ('+', -1, '*'),
    '/': ('*', 1.0, '/')
}


def parse(tokens, i=0):
    i, left_term = parse_term(tokens, i)

    if i == len(tokens) or tokens[i] == ')':
        return i, left_term

    assert tokens[i] == '+'

    i, remaining_expression = parse(tokens, i+1)
    return i, (left_term, '+', remaining_expression)


def parse_term(tokens, i=0):
    i, left_expression = parse_factor(tokens, i)

    if i < len(tokens) and tokens[i] == '/':
        i, denominator_expression = parse_factor(tokens, i+1)
        left_expression = (left_expression, '/', denominator_expression)

    if i == len(tokens) or tokens[i] in '+)':
        return i, left_expression

    assert tokens[i] == '*'

    i, remaining_term = parse_term(tokens, i+1)
    return i, (left_expression, '*', remaining_term)


def parse_factor(tokens, i=0):
    if tokens[i] == '(':
        i, factor = parse(tokens, i+1)
        assert tokens[i] == ')'
        return i+1, factor
    else:
        return i+1, tokens[i]


def evaluate(arithmetic_tree):
    assert isinstance(arithmetic_tree, (int, float)) or (isinstance(arithmetic_tree, tuple) and len(arithmetic_tree) in (1, 3)), arithmetic_tree

    if isinstance(arithmetic_tree, (int, float)):
        return arithmetic_tree
    elif len(arithmetic_tree) == 1:
        return evaluate(arithmetic_tree[0])
    else:
        left_expression = evaluate(arithmetic_tree[0])
        operation = arithmetic_tree[1]
        right_expression = evaluate(arithmetic_tree[2])
        return operations[operation](left_expression, right_expression)


operations = {
    '+': op.add,
    '*': op.mul,
    '/': op.div
}


### Testing

def tests():
    cases = [
        '4 / 2 * 3 + 4 - 6',
        '2-2',
        '4 / 2 * (3 + 4) - 6',
        '-23 / ((4 - 6) * (20 + 202 - 8) / 4) * 34 - 908',
        '(2)',
    ]

    for case in cases:
        print case
        # rw = rewrite(tokenize(case))
        # print rw
        # print parse(rw)[1]
        # print eval(case)
        # print
        assert evaluate_arithmetic(case) == eval(case)

    print
    print 'Tests pass!'


if __name__ == '__main__':
    tests()
