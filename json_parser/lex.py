import re
from collections import deque, namedtuple


def lex(json_string):
    return deque(wrap_match(match.group()) for match in RE.finditer(json_string))


def wrap_match(s):
    assert isinstance(s, unicode)
    return LexItem(lex_type(s), s)


def lex_type(s):
    assert isinstance(s, unicode)
    _lex_type = TOKEN_TO_TYPE.get(s, LITERAL_TO_TYPE.get(s))

    if _lex_type is None:
        if RE_STRING.match(s):
            _lex_type = LexTypes.STRING
        elif RE_NUMBER.match(s):
            _lex_type = LexTypes.NUMBER

    assert _lex_type
    return _lex_type


LexItem = namedtuple('LexItem', 'type value')


class LexTypes:
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


## Mappings from tokens and literals to their types

TOKEN_TO_TYPE = {
    LEFT_BRACE_TOKEN: LexTypes.LEFT_BRACE,
    RIGHT_BRACE_TOKEN: LexTypes.RIGHT_BRACE,
    LEFT_BRACKET_TOKEN: LexTypes.LEFT_BRACKET,
    RIGHT_BRACKET_TOKEN: LexTypes.RIGHT_BRACKET,
    COMMA_TOKEN: LexTypes.COMMA,
    COLON_TOKEN: LexTypes.COLON,
}


LITERAL_TO_TYPE = {
    TRUE_LITERAL: LexTypes.TRUE,
    FALSE_LITERAL: LexTypes.FALSE,
    NULL_LITERAL: LexTypes.NULL,
}
