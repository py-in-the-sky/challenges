import re
from collections import deque, namedtuple


def lex(json_string):
    assert isinstance(json_string, unicode)
    return deque(wrap_match(match.group()) for match in RE.finditer(json_string))


def wrap_match(s):
    assert isinstance(s, unicode)
    return LexItem(lex_tag_of_string(s), s)


def lex_tag_of_string(s):
    assert isinstance(s, unicode)
    lex_tag = TOKEN_TO_TAG.get(s, LITERAL_TO_TAG.get(s))

    if lex_tag is None:
        if RE_STRING.match(s):
            lex_tag = LexTags.STRING
        elif RE_NUMBER.match(s):
            lex_tag = LexTags.NUMBER

    assert lex_tag
    return lex_tag


def is_tagged(lex_item, lex_tag):
    return lex_item.tag is lex_tag


def tag(lex_item):
    return lex_item.tag


LexItem = namedtuple('LexItem', 'tag value')


class LexTags:
    OBJECT = "OBJECT"
    ARRAY = "ARRAY"
    STRING = "STRING"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    NUMBER = "NUMBER"
    LEFT_BRACKET = "LEFT_BRACKET"
    RIGHT_BRACKET = "RIGHT_BRACKET"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    COLON = "COLON"
    QUOTE = "QUOTE"


## Lexing tokens, literals, and patterns

# STRING_PATTERN = r'"[^"\\]*(?:\\.[^"\\]*)*"'  # see: https://stackoverflow.com/a/5696141
STRING_PATTERN = r'".*?(?<!\\)"'
NUMBER_PATTERN = r"\d+"
TRUE_LITERAL = r"true"
FALSE_LITERAL = r"false"
NULL_LITERAL = r"null"
LEFT_BRACKET_TOKEN = r"{"
RIGHT_BRACKET_TOKEN = r"}"
LEFT_BRACE_TOKEN = r"["
LEFT_BRACE_PATTERN = r"\["
RIGHT_BRACE_TOKEN = r"]"
RIGHT_BRACE_PATTERN = r"\]"
COMMA_TOKEN = r","
COLON_TOKEN = r":"


ATOMS_PATTERN = r"|".join([STRING_PATTERN, TRUE_LITERAL, FALSE_LITERAL, NULL_LITERAL, NUMBER_PATTERN])
TOKENS_PATTERN = r"|".join([LEFT_BRACKET_TOKEN, RIGHT_BRACKET_TOKEN, LEFT_BRACE_PATTERN, RIGHT_BRACE_PATTERN,
                            COMMA_TOKEN, COLON_TOKEN])
JSON_LEX_PATTERN = r"{}|{}".format(ATOMS_PATTERN, TOKENS_PATTERN)


RE = re.compile(JSON_LEX_PATTERN)
RE_STRING = re.compile(STRING_PATTERN)
RE_NUMBER = re.compile(NUMBER_PATTERN)


## Mappings from tokens and literals to their tags

TOKEN_TO_TAG = {
    LEFT_BRACE_TOKEN: LexTags.LEFT_BRACE,
    RIGHT_BRACE_TOKEN: LexTags.RIGHT_BRACE,
    LEFT_BRACKET_TOKEN: LexTags.LEFT_BRACKET,
    RIGHT_BRACKET_TOKEN: LexTags.RIGHT_BRACKET,
    COMMA_TOKEN: LexTags.COMMA,
    COLON_TOKEN: LexTags.COLON,
}


LITERAL_TO_TAG = {
    TRUE_LITERAL: LexTags.TRUE,
    FALSE_LITERAL: LexTags.FALSE,
    NULL_LITERAL: LexTags.NULL,
}
