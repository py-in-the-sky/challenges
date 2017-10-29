# from __future__ import division
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
    '/': ('*', 1, '/')
}


def parse(tokens, i=0):
    i, left_term = parse_term(tokens, i)

    if i == len(tokens):
        return i, left_term

    assert tokens[i] == '+'

    i, remaining_expression = parse(tokens, i+1)
    return i, (left_term, '+', remaining_expression)


def parse_term(tokens, i=0):
    left_expression = tokens[i]
    i += 1

    if i < len(tokens) and tokens[i] == '/':
        i += 1
        left_expression = (left_expression, '/', tokens[i])
        i += 1

    if i == len(tokens) or tokens[i] == '+':
        return i, left_expression

    assert tokens[i] == '*'

    i, remaining_term = parse_term(tokens, i+1)
    return i, (left_expression, '*', remaining_term)


def evaluate(arithmetic_tree):
    assert isinstance(arithmetic_tree, int) or (isinstance(arithmetic_tree, tuple) and len(arithmetic_tree) in (1, 3)), arithmetic_tree

    if isinstance(arithmetic_tree, int):
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
    '*': op.sub,
    '/': op.div
}


### Testing

def tests():
    case = '4 / 2 * 3 + 4 - 6'
    print case
    assert evaluate_arithmetic(case) == eval(case)

    print 'Tests pass!'


if __name__ == '__main__':
    tests()
