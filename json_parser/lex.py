import re
from collections import deque, namedtuple

from util import *


RE = re.compile(JSON_LEX_PATTERN)
RE_STRING = re.compile(STRING_PATTERN)
RE_NUMBER = re.compile(NUMBER_PATTERN)


LexItem = namedtuple('LexItem', 'type value')


def lex(json_string):
    return deque(wrap_match(match.group()) for match in RE.finditer(json_string))


def wrap_match(s):
    lex_type = TOKENS.get(s, LITERAL_VALUES.get(s))

    if not lex_type:
        if RE_STRING.match(s):
            lex_type = STRING
            s = unicode(s[1:-1].decode("string-escape"))  # remove end quotes and escape characters
        elif RE_NUMBER.match(s):
            lex_type = NUMBER

    assert lex_type
    return LexItem(lex_type, s)
