import json

from json_parser import load_string, load_string_faster


def tests():
    test_cases = [
        r'{ "foo": "bar", "yo": [{ "hi": "there\"blah" }, 1000] }',
        r'{ "one": { "two": [{ "three": { "four": null }}, false ], "five": 5 }}',
        r'{ "foo": "bar", "baz": null }',
    ]

    for json_string in test_cases:
        print
        print 'JSON:', json_string
        print 'PYTHON:', load_string_faster(json_string)
        assert json.loads(json_string) == load_string(json_string) == load_string_faster(json_string)

    print
    print 'Tests pass!'


if __name__ == '__main__':
    tests()
