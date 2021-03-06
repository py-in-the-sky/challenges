"""
See: http://norvig.com/java-lisp.html
Problem statement: http://www.flownet.com/ron/papers/lisp-java/instructions.html
Other files: http://www.flownet.com/ron/papers/lisp-java/

Completed in six sessions, for a total of two hours and 58 minutes.

    Start: 10:50am
    End: 12:26pm

    Start: 1:20pm
    End: 1:42pm

    5 min

    Start: 2:30pm
    End: 2:55pm

    10 min

    20 min

Design notes:

    * In RAW_LETTER_TO_DIGIT_MAPPING, there's a one-to-one mapping between a
      letter's lower-case and upper-case forms. Therefore, we need only pay
      attention to one of the cases when searching for phone-number encodings.
      We will choose to pay attention to the lower-case letters. However, when
      we print a word, it must appear exactly as it does in the given dictionary.

Results:

    * Performed memory profiling with memory_profiler.
    * Using `python -m memory_profiler Prechelts_test_program.py`, found that
      37 MB were consumed when the `main` function was run. However, the delta
      between the beginning and end of running the `main` function was 26 MB.
    * Using `python -m cProfile Prechelts_test_program.py` on a Macbook pro with
      2.5 GHz Intel Core i5 processor and 8 GB 1600 MHz DDR3 memory, found the
      runtime to be 1.126 seconds.
"""


from collections import defaultdict


### Constants

PHONE_NUMBER_FILENAME = 'phonenumbers.txt'
DICTIONARY_FILENAME = 'dictionary.txt'
EXPECTED_OUTPUTS_FILE = 'outputs.txt'
SAMPLE_PHONE_NUMBER_FILENAME = 'sample-phonenumbers.txt'
SAMPLE_DICTIONARY_FILENAME = 'sample-dictionary.txt'
IGNORED_WORD_CHARACTERS = '-"'
IGNORED_PHONE_NUMBER_CHARACTERS = '-/'
RAW_LETTER_TO_DIGIT_MAPPING = """
E | J N Q | R W X | D S Y | F T | A M | C I V | B K U | L O P | G H Z
e | j n q | r w x | d s y | f t | a m | c i v | b k u | l o p | g h z
0 |   1   |   2   |   3   |  4  |  5  |   6   |   7   |   8   |   9
"""


### Top-level

# @profile
def main():
    for phone_number,encoding in all_encodings(file_lines(PHONE_NUMBER_FILENAME), file_lines(DICTIONARY_FILENAME)):
        print '{}: {}'.format(phone_number, encoding)


# @profile
def all_encodings(phone_numbers, dictionary_words):
    """
    Returns all pairings of phone number and valid encoding, given words in a dictionary. See problem statement
    for valid encoding rules.
    """
    digits_to_words = digits_to_words_mapping(dictionary_words)

    for phone_number in phone_numbers:
        simplified = ''.join(char for char in phone_number if char not in IGNORED_PHONE_NUMBER_CHARACTERS)

        for encoding in phone_encodings(simplified, digits_to_words):
            yield phone_number, ' '.join(encoding)


# @profile
def phone_encodings(phone_number, digits_to_words):
    """
    Returns all valid encodings of phone_number, given a mapping of digit sequences to words that
    encode the digit sequence (see RAW_LETTER_TO_DIGIT_MAPPING). See problem statement for valid
    encoding rules.
    """
    if not phone_number:
        return ()

    def _phone_encodings(phone_number, can_prepend_first_digit=True):
        if not phone_number:
            return [()]

        prefix_word_found = False
        result = []

        for prefix,suffix in partitions(phone_number):
            prefix_words = digits_to_words.get(prefix)

            # Key choice for performance. If the prefix maps to no words or suffix has no encoding,
            # then the whole word has no encoding. Because checking whether prefix maps to any words
            # (just a hash-table lookup) is cheaper than checking whether suffix has any encodings
            # (searching over all partitions of suffix), we choose to first check whether prefix maps
            # to any words and if not, then short-circuit the search for encodings.
            if prefix_words:
                prefix_word_found = True
                for suffix_encoding in _phone_encodings(suffix):
                    for word in prefix_words:
                        result.append((word,) + suffix_encoding)

        # Can prepend a digit if no word can be found for any prefix of phone_number and
        # a digit hasn't just been prepended.
        if prefix_word_found or not can_prepend_first_digit:
            return result
        else:
            first_digit, remaining_number = phone_number[0], phone_number[1:]
            return [(first_digit,) + encoding for encoding in _phone_encodings(remaining_number, False)]

    return _phone_encodings(phone_number)


### Ancillary

def partitions(string):
    """
    All partitions of a string into prefixes and suffixes such that the prefix has
    at least on character. E.g.:

    'abc' => (('a', 'bc'), ('ab', 'c'), ('abc', ''))
    """
    for i in xrange(1, len(string)+1):
        yield string[:i], string[i:]


def digits_to_words_mapping(dictionary_words):
    """
    Return mapping of digit sequences to dictionary words, based on RAW_LETTER_TO_DIGIT_MAPPING
    and IGNORED_WORD_CHARACTERS. E.g.:

    ['jemand', 'fort', 'Torf'] => {'105513': ['jemand'], '4824': ['fort', 'Torf']}
    """
    letter_to_digit = letter_to_digit_mapping()
    mapping = defaultdict(list)

    for word in dictionary_words:
        simplified_word = ''.join(letter_to_digit[char.lower()] for char in word if char not in IGNORED_WORD_CHARACTERS)
        mapping[simplified_word].append(word)

    return dict(mapping)


def letter_to_digit_mapping():
    """
    Parse RAW_LETTER_TO_DIGIT_MAPPING and return a Python dictionary with
    the mapping from lower-case letters to digits. E.g.:

    {
        'e': '0',
        ...
        'k': '7',
        'u': '7',
        ...
    }
    """
    # Only use line 2 below because we only need the mapping for lower-case letters.
    raw_mapping = RAW_LETTER_TO_DIGIT_MAPPING.splitlines()[2]
    return {letter: str(i)
            for i,group in enumerate(raw_mapping.split('|'))
            for letter in group.split()}


def file_lines(filename):
    "Lazily yield each line of a file, stripped of surrounding whitespace/newlines."
    with open(filename, 'rU') as f:
        for line in f:
            yield line.strip()


def test():
    expected_outputs = (line.split(':') for line in file_lines(EXPECTED_OUTPUTS_FILE))
    expected_outputs = set((phone_number.strip(), encoding.strip())
                           for phone_number,encoding in expected_outputs)

    actual_outputs = set(all_encodings(file_lines(PHONE_NUMBER_FILENAME), file_lines(DICTIONARY_FILENAME)))

    assert expected_outputs == actual_outputs

    print 'Test passes!'


if __name__ == '__main__':
    # main()
    test()
