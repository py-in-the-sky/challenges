from types import GeneratorType

from lex import LexTags, tag, value, is_tagged, LexItem


def debug_generator(gen):
    l = list(gen)

    print 'Lex Generator:', l

    return (e for e in l)


def debug_item(i):
    print i
    return i


def parse_faster(lex_generator):
    first_lex_item = next(lex_generator)

    python_element, rest_lex_generator = parse(first_lex_item, lex_generator)

    assert len(list(rest_lex_generator)) == 0

    return python_element


def parse(first_lex_item, rest_lex_generator):
    assert isinstance(rest_lex_generator, GeneratorType) and isinstance(first_lex_item, LexItem)

    parse_fn = LEX_TAG_TO_PARSE_FUNCTION[tag(first_lex_item)]
    return parse_fn(first_lex_item, rest_lex_generator)


def parse_object(first_lex_item, rest_lex_generator):
    assert (isinstance(first_lex_item, LexItem) and
            isinstance(rest_lex_generator, GeneratorType) and
            is_tagged(first_lex_item, LexTags.LEFT_BRACKET))

    lex_item = next(rest_lex_generator)
    python_dict = {}

    while not is_tagged(lex_item, LexTags.RIGHT_BRACKET):
        assert is_tagged(lex_item, LexTags.STRING)

        # get the key of the key-value pair
        key_python_string, rest_lex_generator = parse_string(lex_item, rest_lex_generator)

        # remove the colon of the key-value pair
        lex_item = next(rest_lex_generator)
        assert is_tagged(lex_item, LexTags.COLON)

        # get the value of the key-value pair
        lex_item = next(rest_lex_generator)
        value_python_element, rest_lex_generator = parse(lex_item, rest_lex_generator)

        # insert parsed key-value pair into python_dict
        python_dict[key_python_string] = value_python_element

        # handle trailing ',' or '}'
        lex_item = next(rest_lex_generator)
        assert is_tagged(lex_item, LexTags.COMMA) or is_tagged(lex_item, LexTags.RIGHT_BRACKET)
        if is_tagged(lex_item, LexTags.COMMA):
            lex_item = next(rest_lex_generator)

    return python_dict, rest_lex_generator


def parse_array(first_lex_item, rest_lex_generator):
    assert (isinstance(first_lex_item, LexItem) and
            isinstance(rest_lex_generator, GeneratorType) and
            is_tagged(first_lex_item, LexTags.LEFT_BRACE))

    lex_item = next(rest_lex_generator)
    python_list = []

    while not is_tagged(lex_item, LexTags.RIGHT_BRACE):
        assert not is_tagged(lex_item, LexTags.COMMA)

        # get value of next array element and append to python_list
        python_element, rest_lex_generator = parse(lex_item, rest_lex_generator)
        python_list.append(python_element)

        # handle trailing ',' or ']'
        lex_item = next(rest_lex_generator)
        assert is_tagged(lex_item, LexTags.COMMA) or is_tagged(lex_item, LexTags.RIGHT_BRACE)
        if is_tagged(lex_item, LexTags.COMMA):
            lex_item = next(rest_lex_generator)

    return python_list, rest_lex_generator


def parse_string(first_lex_item, rest_lex_generator):
    assert (isinstance(first_lex_item, LexItem) and
            isinstance(rest_lex_generator, GeneratorType) and
            is_tagged(first_lex_item, LexTags.STRING))

    # remove end quotes and escape characters from the JSON string
    python_string = unicode(value(first_lex_item)[1:-1].decode("string-escape"))
    return python_string, rest_lex_generator


def parse_number(first_lex_item, rest_lex_generator):
    assert (isinstance(first_lex_item, LexItem) and
            isinstance(rest_lex_generator, GeneratorType) and
            is_tagged(first_lex_item, LexTags.NUMBER))

    return int(value(first_lex_item)), rest_lex_generator


def parse_true(first_lex_item, rest_lex_generator):
    assert (isinstance(first_lex_item, LexItem) and
            isinstance(rest_lex_generator, GeneratorType) and
            is_tagged(first_lex_item, LexTags.TRUE))

    return True, rest_lex_generator


def parse_false(first_lex_item, rest_lex_generator):
    assert (isinstance(first_lex_item, LexItem) and
            isinstance(rest_lex_generator, GeneratorType) and
            is_tagged(first_lex_item, LexTags.FALSE))

    return False, rest_lex_generator


def parse_null(first_lex_item, rest_lex_generator):
    assert (isinstance(first_lex_item, LexItem) and
            isinstance(rest_lex_generator, GeneratorType) and
            is_tagged(first_lex_item, LexTags.NULL))

    return None, rest_lex_generator


LEX_TAG_TO_PARSE_FUNCTION = {
    LexTags.LEFT_BRACKET: parse_object,
    LexTags.LEFT_BRACE: parse_array,
    LexTags.STRING: parse_string,
    LexTags.TRUE: parse_true,
    LexTags.FALSE: parse_false,
    LexTags.NULL: parse_null,
    LexTags.NUMBER: parse_number,
}
