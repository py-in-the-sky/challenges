# 3rd-party imports
from itertools import chain


def memo(f):
    """memoization decorator, taken from Peter Norvig's Design of Computer
    Programs course on Udacity.com"""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            result = cache[args] = f(*args)
            return result
        except TypeError:  # unhashable argument
            return f(*args)
    return _f


def read_dictionary(filename=None):
    stub = stub_dictionary()

    if filename is None:
        return stub
    else:
        return chain(stub, read_dictionary_file(filename))


def read_dictionary_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip().lower()


def stub_dictionary():
    dictionary = """
        cat cot dot dog mat car cap can kit cow cap cop dip dim
        fan fit fin fir for fun fog log lag
        fawn found first foremost
        duck ducks ducky ducked ducking
        dusk dust dusty dusts duster dusted dusting
        rue run runt runts bunt bunts bunted bend bends bended bent beet bee be
        rub ruse reuse refuse refused defused defuse
        recuse recluse
        fifty
        play
        dirt dirty
        captain caption cast cannister
        place places
    """

    lines = (line.strip() for line in  dictionary.splitlines())
    words = (word for line in lines for word in line.split())
    return words


def string_partitions(string):
    for i,char in enumerate(string):
        prefix, suffix = string[:i], string[i+1:]
        yield prefix, char, suffix


def show_path(path): return '--> '.join(path)


def underestimate_edit_distance_fn_factory(word):
    def underestimate_edit_distance(word_2):
        shorter, longer  = sorted((word, word_2), key=lambda string: len(string))
        n_character_diff = len(longer) - len(shorter)
        n_tranform_diff  = sum(char not in longer for char in shorter)
        return n_character_diff + n_tranform_diff

    return underestimate_edit_distance


class QueueStatsWrapper:
    def __init__(self, queue):
        self.get_counts = 0
        self.put_counts = 0
        self.queue      = queue

    def get(self):
        self.get_counts += 1
        return self.queue.get()

    def put(self, item):
        self.put_counts += 1
        self.queue.put(item)

    def empty(self):
        return self.queue.empty()

    def show_stats(self):
        return '{} gets and {} puts'.format(self.get_counts, self.put_counts)
