import json

from json_parser import load_string, load_string_faster


def tests():
    s = r'{ "foo": "bar", "yo": [{ "hi": "there\"blah" }, 1000] }'
    s2 = r'{ "one": { "two": [{ "three": { "four": null }}, false ], "five": 5 }}'

    print
    print 'JSON:', s
    print 'PYTHON:', load_string_faster(s)
    assert json.loads(s) == load_string(s) == load_string_faster(s)

    print
    print 'JSON:', s2
    print 'PYTHON:', load_string_faster(s2)
    assert json.loads(s2) == load_string(s2) == load_string_faster(s2)

    print
    print 'Tests pass!'


if __name__ == '__main__':
    tests()
