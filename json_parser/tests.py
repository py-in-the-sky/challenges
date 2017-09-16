import json

from json_parser import load_string


def tests():
    s = r'{ "foo": "bar", "yo": [{ "hi": "there\"blah" }, 1000] }'
    s2 = r'{ "one": { "two": [{ "three": { "four": null }}, false ], "five": 5 }}'

    assert json.loads(s) == load_string(s)
    assert json.loads(s2) == load_string(s2)

    print 'Tests pass!'


if __name__ == '__main__':
    tests()
