# imports from solution
from main import solution, LOCAL_DICTIONARY
from utils import show_path, QueueStatsWrapper
from trie_utils import make_trie


# 3rd-party imports
from Queue import Queue, PriorityQueue
from timeit import timeit


SEARCH_METHODS = (
    ('A*',  PriorityQueue),
    ('BFS', Queue)
)


CASES = (
    ('cat',       'dog'),
    ('cat',       'mistrial'),
    ('strong',    'weak'),
    ('hot',       'cold'),
    ('up',        'down'),
    ('left',      'right'),
    ('light',     'heavy'),
    ('computer',  'virus'),
    ('strike',    'freeze'),
    ('fan',       'for'),
    ('duck',      'dusty'),
    ('rue',       'be'),
    ('rue',       'defuse'),
    ('rue',       'bend'),
    ('zoologist', 'zoology')
)


BENCHMARK_SETUP_STATEMENT = """
from __main__ import solution, make_trie, CASES, LOCAL_DICTIONARY, \
                     PriorityQueue, Queue

make_trie(LOCAL_DICTIONARY)
"""


BENCHMARK_STATEMENT_TEMPLATE = """
opts = dict(
    search_method='{search_method_name}',
    queue={queue_class_name}(),
    dictionary_filename=LOCAL_DICTIONARY
)

solution('{start_word}', '{target_word}', opts)
"""


def show_queue_stats_comparisons():
    for start_word,target_word in CASES:
        print

        for search_method_name,queue_type in SEARCH_METHODS:
            opts = {
                'search_method': search_method_name,
                'queue': QueueStatsWrapper(queue_type()),
                'dictionary_filename': LOCAL_DICTIONARY
            }

            maybe_path = solution(start_word, target_word, opts)
            q = opts['queue']

            formatted_path = show_path(maybe_path) if maybe_path else 'None'
            node_count = '({} nodes)'.format(len(maybe_path)) if maybe_path else ''

            queue_class_name = 'Queue' if queue_type == Queue else 'PriorityQueue'

            benchmark_config = dict(search_method_name=search_method_name,
                                    queue_class_name=queue_class_name,
                                    start_word=start_word,
                                    target_word=target_word)

            time = timeit(BENCHMARK_STATEMENT_TEMPLATE.format(**benchmark_config),
                          BENCHMARK_SETUP_STATEMENT,
                          number=1)

            print search_method_name
            print '  Time:', time
            print '  Shortest path:', formatted_path, node_count
            print '  Queue stats:  ', q.show_stats()

        print


if __name__ == '__main__':
    show_queue_stats_comparisons()
