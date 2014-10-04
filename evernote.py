"""
challenge: https://www.hackerrank.com/contests/evernote-coding-challenge/challenges

The definition of tree is borrowed directly from Peter Norvig's Design of
Computer Programs course on udacity.com.

The design of the functions that operate on tries are influenced by Peter
Norvig's Common-Lisp trie code from Paradigms of Artificial Intelligence
Programming.

Architecture and design:
    The program is separated into four "modules," one for each of the
    following:
        * data storage and retrieval
        * helpers for parsing raw documents and queries
        * input/output helpers
        * the API

    Notes are parsed into: 1) a string field for the guid; 2) a set containing
    a single datetime object for the created date; 3) a set containing all
    unique tag terms; and 4) a set containing all unique content terms.  I
    chose to store the created date in a set so that all searchable fields
    could be treated uniformly by the create, update, and delete procedures:
    all searchable fields in a parsed note are treated as sets of terms.

    The indexes use a trie data structure for efficient querying.  Tries allow
    easy searching by full words and by prefixes.  They also support greater-
    than and less-than searches for lexicographic comparisons.  This is
    convenient for the 'created' queries since these queries require us to
    return all results created on or after a given date and the form of the ISO
    8601 timestamp means lexicographic comparisons of the timestamps return the
    same results as less-than/greater-than comparisons of the underlying dates.
"""

import re
from datetime import datetime
from collections import defaultdict
from itertools import takewhile


####### data models, storage, and helpers #######

# tree returns a Python dictionary, which will create, by default, another
# Python dictionary as the value for any key queried or inserted into the
# dictionary.  Hence, a tree is created by nesting dictionaries.
def tree(): return defaultdict(tree)

database = dict()
indexes = {
    'tag': tree(),
    'content': tree(),
    'created': tree()
}
NULL_GUIDS = set()

def trie_put(word, guid, trie):
    "put guid in the 'guid' field of word's node in the trie"
    # read 'node' in the doc string above as 'dictionary'
    t = find_trie(word, trie)
    if 'guid' in t:  t['guid'].add(guid)
    else:            t['guid'] = {guid}

def trie_delete(word, guid, trie):
    "delete guid from word's node in the trie if guid is in the 'guid' field"
    t = find_trie(word, trie)
    if 'guid' in t and guid in t['guid']:
        t['guid'].remove(guid)

def find_trie(word, trie):
    """str, trie -> trie
    return the trie rooted at word's node
    """
    for c,t in char_and_trie(word, trie):
        pass
    return t[c]
    # if not word:
    #     return trie
    # initial, rest = word[0], word[1:]
    # return find_trie(rest, trie[initial])

def char_and_trie(word, trie):
    """traverse word's path through trie, yielding each character and
    corresponding tree node along the way
    """
    t = trie
    for c in word:
        yield c, t
        t = t[c]

def get_word(word, trie):
    """str, trie -> set(str)
    return set of guids at word's node in the trie
    """
    return find_trie(word, trie).get('guid', NULL_GUIDS)

def get_prefix(word, trie):
    """str, trie -> set(str)
    return set of guids at or below word's node in the trie
    """
    trie2 = find_trie(word, trie)
    guids = trie2.get('guid', NULL_GUIDS)
    return guids.union(*(get_prefix(k, trie2) for k in trie2 if k != 'guid'))
    # in the base case of this recursion, trie2 will have no keys, so no
    # recursive calls to get_prefix will be made; guids will be unioned with
    # an empty collection of sets

def get_gte(word, trie):
    """str, trie -> set(str)
    return set of guids for word and all other words in trie that are
    lexicographically greater than word
    """
    return get_prefix(word, trie) | get_gt(word, trie)

def get_gt(word, trie):
    """str, trie -> set(str)
    return set of guids for all words in trie that are
    lexicographically greater than word
    """
    def _get_gt(char, trie):
        """str, trie -> set(str)
        return set of guids for all words in trie that are
        lexicographically greater than char
        """
        gt_sets = [get_prefix(c, trie) for c in trie
                   if c != 'guid' and c > char]
        return set.union(*(gt_sets or [NULL_GUIDS]))

    return set.union(*(_get_gt(c, t) for c,t in char_and_trie(word, trie)))

def search_intersection(queries):
    """[(str,str,bool)] -> set(str)
    return the set of guids found by every query in queries (i.e., return the
    intersection, or logical 'and', of all the individual query results)
    queries is a generator, or lazy list, that yields tuples of the form
    (query-term, query-type, is-prefix); together, these tuples represent
    multiple query terms whose results are combined with a logical 'and'
    """
    def _search(query):
        qterm, qtype, is_prefix = query
        trie = indexes[qtype]
        if qtype == 'created':  return get_gte(qterm, trie)
        if is_prefix:           return get_prefix(qterm, trie)
        else:                   return get_word(qterm, trie)

    return set.intersection(*(_search(q) for q in queries))


####### parsing helpers #######

TEMPLATE = r'<{0}>(?P<{0}>.+?)</{0}>'
PATTERN = '|'.join(TEMPLATE.format(a)
                   for a in 'guid created tag content'.split())
NOTE_ASPECT_REGEX = re.compile(PATTERN, flags=re.DOTALL)
VALID_WORD_REGEX = re.compile(r"[\w']+", flags=re.DOTALL)
UTC_DELTA = datetime.now() - datetime.utcnow()

def parse_note(note_string):
    """str -> dict
    return a dictionary with a key four keys: guid, created, tag, content
    'guid' stores the note's guid as a string
    'created' stores a datetime object in a set
    'tag' stores all unique words in the note's tags in a set
    'content' stores all unique words in the note's content in a set
    """
    note = defaultdict(set)
    aspects = NOTE_ASPECT_REGEX.finditer(note_string)
    # build the parsed note by looping through the aspects of the note
    for match in aspects:
        aspect_matches = ((a,v) for (a,v) in match.groupdict().iteritems()
                          if v is not None)
        # only one aspect of the note has a match that is not None in each loop
        aspect, value = next(aspect_matches)

        if aspect == 'guid':
            note[aspect] = value
        elif aspect == 'created':
            note[aspect].add(to_local_datetime(value))
        else:
            # normalize tags and content to lower-case
            words = VALID_WORD_REGEX.findall(value.lower())
            note[aspect].update(words)
    return note

def to_local_datetime(dt):
    """str -> datetime
    returns a datetime object representing dt converted to local time
    dt is an ISO 8601 timestamp in the format yyyy-MM-ddThh:mm:ssZ where 'Z'
    indicates absolute UTC time
    """
    # strip time zone info off the end of timestamp for convenience since my
    # system doesn't seem to support parsing that aspect of the timestamp
    utc_time = datetime.strptime(dt[:-1], "%Y-%m-%dT%H:%M:%S")
    return utc_time + UTC_DELTA

def parse_query(query_string):
    """str -> (str,str,bool)
    returns (query-term, query-type, is-prefix) tuple
    """
    # all of these conditionals aren't scalable; find better design pattern
    if query_string.startswith('created:'):
        return (query_string.replace('created:', ''), 'created', False)

    # normalize tags and content to lower-case
    qs, is_prefix = query_prefix_transform(query_string.lower())

    if qs.startswith('tag:'): return (qs.replace('tag:', ''), 'tag', is_prefix)
    else:                     return (qs, 'content', is_prefix)

def query_prefix_transform(query_term):
    """str -> (str, bool)
    return (query-term, is-prefix) tuple
    """
    is_prefix = query_term.endswith('*')
    query_term = query_term[:-1] if is_prefix else query_term
    return (query_term, is_prefix)


####### IO helpers #######

def read_std_input():
    "read STDIN, line by line, and yield each line as a str"
    while True:
        yield raw_input()

STDIN = read_std_input()

def read_note():
    """read in note from <note> to </note>
    return the full note as a string with each newline replaced by a space
    """
    not_end_of_note = lambda s: s.strip() != '</note>'
    lines = takewhile(not_end_of_note, STDIN)
    return ' '.join(lines) + ' </note>'


####### API #######

def create(note):
    "create note in database and index it in indexes"
    database[note['guid']] = note
    apply_to_indexes(trie_put, note)

def update(note):
    "update note in database and indexes"
    # right now, I just completely delete the note and then create it again
    # TODO: perhaps it'd be more efficient to diff the new/old notes, take the
    # words revealed in the diff, and just add/delete the guid from these
    # specific words in the tries
    delete(note['guid'])
    create(note)

def delete(guid_string):
    "delete note from database and all indexes"
    note = database.pop(guid_string, None)
    apply_to_indexes(trie_delete, note)

def apply_to_indexes(trie_fn, note):
    "apply trie_fn to note and every trie in indexes"
    for note_aspect,trie in indexes.iteritems():
        for word in note[note_aspect]:
            if note_aspect=='created':
                # normalize datetimes to the string format of 'created' queries
                word = word.strftime('%Y%m%d')
            trie_fn(word, note['guid'], trie)

def search(queries_string):
    """find the guid of each note that matches the query
    print comma-separated list of guids, ordered by date created
    """
    def _by_date(guid):
        # need to use next on an iterator expression to deal with the design
        # choice of holding the 'created' date in a singleton set
        return next(iter(database[guid]['created']))

    queries = (parse_query(q) for q in queries_string.split())
    guids = search_intersection(queries)
    print ','.join(sorted(guids, key=_by_date))

def main():
    "read lines from standard input, calling appropriate API functions"
    while True:
        try:
            command = next(STDIN)
            api_procedure, input_procedure = API[command]
            api_procedure(input_procedure())
        except (EOFError, KeyError) as e:
            # print e
            break

API = {
    # command: (api_procedure, input_procedure)
    'CREATE': (create, lambda: parse_note(read_note())),
    'UPDATE': (update, lambda: parse_note(read_note())),
    'DELETE': (delete, lambda: next(STDIN)),
    'SEARCH': (search, lambda: next(STDIN))
}


if __name__ == '__main__':
    main()
