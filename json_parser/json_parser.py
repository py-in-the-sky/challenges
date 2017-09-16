"""
Simplified JSON definition, adapted from http://www.json.org/

    object
        {}
        { members }
    members
        pair
        pair , members
    pair
        string : value
    array
        []
        [ elements ]
    elements
        value
        value , elements
    value
        string
        number
        object
        array
        true
        false
        null
    string
        ""
        " chars "
    chars
        char
        char chars
    char
        any unicode character except \"
"""


from lex import lex
from parse import parse
from load import load
from util import pipe_value


def load_string(json_string):
    return pipe_value(unicode(json_string), (lex, parse, load))
