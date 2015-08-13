# imports from solution
from utils import underestimate_edit_distance_fn_factory


# 3rd-party imports
from Queue import Queue, PriorityQueue


def shortest_path_bfs(word1, word2, neighbors_fn, queue=None):
    visited_words = set()
    start_state = ( word1, )
    q = Queue() if queue is None else queue
    q.put(start_state)

    while not q.empty():
        path = q.get()
        last_word = path[-1]

        if last_word == word2:
            return path

        if last_word not in visited_words:
            visited_words.add(last_word)

            for neighbor_word in neighbors_fn(last_word):
                if neighbor_word not in visited_words:
                    q.put(path + ( neighbor_word, ))


def shortest_path_A_star(word1, word2, neighbors_fn, queue=None):
    underestimate_edit_distance = underestimate_edit_distance_fn_factory(word2)

    visited_words = set()
    start_state = (1 + underestimate_edit_distance(word1), ( word1, ))
    q = PriorityQueue() if queue is None else queue
    q.put(start_state)

    while not q.empty():
        _, path = q.get()
        last_word = path[-1]

        if last_word == word2:
            return path

        if last_word not in visited_words:
            visited_words.add(last_word)

            for neighbor_word in neighbors_fn(last_word):
                if neighbor_word not in visited_words:
                    new_path  = path + ( neighbor_word, )
                    underestimated_distance_to_target = underestimate_edit_distance(neighbor_word)
                    underestimated_total_path_length  = underestimated_distance_to_target + len(new_path)
                    new_state = (underestimated_total_path_length, new_path)
                    q.put(new_state)
