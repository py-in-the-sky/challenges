from timeit import timeit


TEST1 = """
load_string(r'{ "one": { "two": [{ "three": { "four": null }}, false ], "five": 5 }}')
"""


TEST2 = """
load_string_faster(r'{ "one": { "two": [{ "three": { "four": null }}, false ], "five": 5 }}')
"""


TEST3 = """
json.loads(r'{ "one": { "two": [{ "three": { "four": null }}, false ], "five": 5 }}')
"""


def time():
    n = 50
    print "Timing on input:", r'{ "one": { "two": [{ "three": { "four": null }}, false ], "five": 5 }}'
    print 'load_string:       ', timeit(TEST1, "from json_parser import load_string", number=n)
    print 'load_string_faster:', timeit(TEST2, "from json_parser import load_string_faster", number=n)
    print 'json.loads:        ', timeit(TEST3, "import json", number=n)


if __name__ == '__main__':
    time()
