def parse_even_faster(json_string):
    python_object, i = parse(json_string)

    j = consume_whitespace(json_string, i)
    assert j == len(json_string)

    return python_object


DIGITS = '1234567890'


def parse(s, i=0):
    i = consume_whitespace(s, i)
    char = s[i]

    if char == '{':
        return parse_object(s, i)
    elif char == '[':
        return parse_array(s, i)
    elif char == '"':
        return parse_string(s, i)
    elif char in DIGITS:
        return parse_integer(s, i)
    elif char == 't' and s[i:i+4] == 'true':
        return True, i+4
    elif char == 'f' and s[i:i+5] == 'false':
        return False, i+5
    elif char == 'n' and s[i:i+4] == 'null':
        return None, i+4

    assert False, 'Invalid JSON'


def parse_object(s, i):
    python_dict = {}
    j = consume_whitespace(s, i+1)

    while s[j] != '}':
        key_python_string, j2 = parse_string(s, j)
        j3 = consume_whitespace(s, j2)

        assert s[j3] == ':'

        j4 = consume_whitespace(s, j3+1)
        value_python_element, j5 = parse(s, j4)
        python_dict[key_python_string] = value_python_element
        j6 = consume_whitespace(s, j5)

        assert s[j6] in ',}'

        if s[j6] == ',':
            j6 = consume_whitespace(s, j6+1)

        j = j6

    return python_dict, j+1


def parse_array(s, i):
    python_list = []
    j = consume_whitespace(s, i+1)

    while s[j] != ']':
        python_element, j2 = parse(s, j)
        python_list.append(python_element)
        j3 = consume_whitespace(s, j2)

        assert s[j3] in ',]'

        if s[j3] == ',':
            j3 = consume_whitespace(s, j3+1)

        j = j3

    return python_list, j+1


def parse_string(s, i):
    j = i+1

    while s[j] != '"':
        j += (2 if s[j] == '\\' else 1)

    return unicode(s[i+1:j].decode("string-escape")), j+1


def parse_integer(s, i):
    len_s = len(s)
    j = next(j for j in xrange(i+1, len_s+1) if j == len_s or s[j] not in DIGITS)
    return int(s[i:j]), j


def consume_whitespace(s, i):
    len_s = len(s)
    return i if i == len_s else next((i for i in xrange(i, len_s) if s[i] is not ' '), len_s)
