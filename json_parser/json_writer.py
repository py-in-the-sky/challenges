from itertools import chain


def to_json(python_element):
    return ''.join(_to_json(python_element))


def _to_json(python_element):
    converter = TYPE_TO_CONVERTER[type(python_element)]
    return converter(python_element)


def dict_to_json(d):
    def _substrings():
        yield '{'

        for i,(k,v) in enumerate(d.iteritems()):
            if i > 0:
                yield ', '

            yield str_to_json(k)
            yield ': '
            yield _to_json(v)

        yield '}'

    return chain(*_substrings())


def list_to_json(l):
    def _substrings():
        yield '['

        for i,e in enumerate(l):
            if i > 0:
                yield ', '

            yield _to_json(e)

        yield ']'

    return chain(*_substrings())


ESCAPE_DCT = {  # copied from https://github.com/simplejson/simplejson/blob/master/simplejson/encoder.py
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}


def str_to_json(s):
    yield '"'

    for char in s:
        yield ESCAPE_DCT.get(char, char)

    yield '"'


def int_to_json(n):
    return str(n)


def bool_to_json(b):
    return 'true' if b else 'false'


def none_to_json(_):
    return 'null'


TYPE_TO_CONVERTER = {
    dict: dict_to_json,
    list: list_to_json,
    str:  str_to_json,
    int:  int_to_json,
    bool: bool_to_json,
    type(None): none_to_json,
}


def tests():
    import json

    py = 'hi\"'
    assert to_json(py) == json.dumps(py)

    py = { "hi": { "you" : [1, True, None, { "one": True}]}, "two": "fo\"o\n"}
    assert to_json(py) == json.dumps(py)

    print 'Tests pass!'


def time():
    from timeit import timeit

    n = 1000
    setup = 'from __main__ import to_json; import json; py = { "hi": { "you" : [1, True, None, { "one": True}]}, "two": "foo"}'
    test1 = 'to_json(py)'
    test2 = 'json.dumps(py)'
    print 'to_json:   ', timeit(test1, setup, number=n)
    print 'json.dumps:', timeit(test2, setup, number=n)


if __name__ == '__main__':
    time()
    tests()
    time()
