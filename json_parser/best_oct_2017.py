"""
JSON definition: http://www.json.org/
JSON-Python type mapping: https://github.com/simplejson/simplejson/blob/db2a216a858e8fd2cbfd53ac52c7972e5d3b3c5a/simplejson/decoder.py#L278
"""

def parse_json(s):
    # For simplicity, not handling whitespace between lexical elements
    # of the JSON string. TODO: consume/ignore whitespace between elements.
    i = skip_leading_whitespace(s, 0)
    assert i < len(s), 'string cannot be emtpy or blank'

    try:
        python_element, i = _parse_json(s, i)
        validate_json(s, i, condition=(i == len(s)))
        return python_element
    except IndexError:
        raise_invalid_json_error('Unexpected end of string:', s, len(s))


def _parse_json(s, i):
    first_char = s[i]

    if first_char == '{':
        return parse_object(s, i)
    elif first_char == '[':
        return parse_array(s, i)
    elif first_char == '"':
        return parse_string(s, i)
    elif first_char == 'n':
        return parse_null(s, i)
    elif first_char == 't':
        return parse_true(s, i)
    elif first_char == 'f':
        return parse_false(s, i)
    else:
        return parse_number(s, i)


def parse_object(s, i):
    validate_json(s, i, expected='{')

    i = skip_trailing_whitespace(s, i+1)
    python_dict = {}

    while s[i] != '}':
        key, i = parse_string(s, i)
        validate_json(s, i, expected=':')
        value, i = _parse_json(s, skip_trailing_whitespace(s, i+1))

        python_dict[key] = value

        if s[i] == ',':
            i = skip_trailing_whitespace(s, i+1)
            validate_json(s, i, not_expected='}')
        else:
            validate_json(s, i, expected='}')

    return python_dict, skip_trailing_whitespace(s, i+1)


def parse_array(s, i):
    validate_json(s, i, expected='[')

    i = skip_trailing_whitespace(s, i+1)
    python_list = []

    while s[i] != ']':
        python_element, i = _parse_json(s, i)
        python_list.append(python_element)

        if s[i] == ',':
            i = skip_trailing_whitespace(s, i+1)
            validate_json(s, i, not_expected=']')
        else:
            validate_json(s, i, expected=']')

    return python_list, skip_trailing_whitespace(s, i+1)


def parse_string(s, i):
    validate_json(s, i, expected='"')

    i += 1
    i0 = i

    while s[i] != '"':
        if s[i] == '\\':
            i += 2  # Escaped character takes up two spaces.
        else:
            i += 1

    python_string = s[i0:i].decode('string-escape')
    return python_string, skip_trailing_whitespace(s, i+1)


def parse_null(s, i):
    validate_json(s, i, condition=(s[i:i+4] == 'null'))
    return None, skip_trailing_whitespace(s, i+4)

def parse_true(s, i):
    validate_json(s, i, condition=(s[i:i+4] == 'true'))
    return True, skip_trailing_whitespace(s, i+4)


def parse_false(s, i):
    validate_json(s, i, condition=(s[i:i+5] == 'false'))
    return False, skip_trailing_whitespace(s, i+5)


def parse_number(s, i):
    # For simplicity, handling just integers for now. TODO: handle all
    # number types in the JSON specification.
    validate_json(s, i, condition=('0' <= s[i] <= '9'))
    j = next((j for j in xrange(i, len(s)) if not '0' <= s[j] <= '9'), None)

    if j is None:
        return int(s[i:]), len(s)
    else:
        return int(s[i:j]), skip_trailing_whitespace(s, j)


### Skipping Whitespace between JSON Elements

import re

_whitespace_matcher = re.compile(r'\s*')
skip_trailing_whitespace = skip_leading_whitespace = lambda s, i: _whitespace_matcher.match(s, i).end()


### Input Validation

def validate_json(s, i, expected=None, not_expected=None, condition=None):
    assert expected is not None or not_expected is not None or condition is not None,\
        'expected, not_expected, or condition must be declared'

    expected is not None and s[i] == expected or \
    not_expected is not None and s[i] != not_expected or \
    condition is True or \
    raise_invalid_json_error('Unexpected token:', s, i)


def raise_invalid_json_error(message, s, i):
    err_message = JSON_VALIDATION_ERROR_MESSAGE_TEMPLATE.format(
        message=message,
        json=s,
        caret=caret(i)
    )
    raise JsonValidationError(err_message)


def caret(i):
    return ' ' * i + '^'


class JsonValidationError(StandardError):
    pass


JSON_VALIDATION_ERROR_MESSAGE_TEMPLATE = """{message}
{json}
{caret}"""


### Testing and Performance Measurement

def tests():
    import json

    test1 = {
        'hi"': "there'",
        "foo": {
            "bar": 'baz',
            'blah': [
                {'foo':'bar', '   ': 40}
            ]
        }
    }
    test2 = 'null'
    test3 = '"hi \"asdf\""'

    for t in (test1, test2, test3):
        s = json.dumps(t)
        assert parse_json(s) == json.loads(s), s

    print 'Tests pass!'


def timeit():
    import json
    from timeit import timeit

    test_json = json.dumps({
        'hi\\"': "there",
        "foo": {
            "bar": 'baz',
            'blah': [
                {'foo':'bar', '   ': 40}
            ]
        }
    })
    test_json = r'{"one":{"two":[{"three":{"four":null}},false],"five":5}}'
    test1 = "parse_json('{}')".format(test_json)
    test2 = "json.loads('{}')".format(test_json)

    n = 1000
    print "Timing on input:", test_json
    print 'parse_json:', timeit(test1, "from __main__ import parse_json", number=n)
    print 'json.loads:', timeit(test2, "import json", number=n)


if __name__ == '__main__':
    tests()
    timeit()
