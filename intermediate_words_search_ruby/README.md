I have implemented a [Python version](https://github.com/py-in-the-sky/challenges/tree/master/intermediate_words_search_python) that runs roughly five times faster on most of the example cases used for benchmarking, which suggests there are some subtleties to Ruby performance that I don't understand.  Admittedly, I have a better grasp on Python than on Ruby.

The tests under `spec.rb` (run `bundle exec rspec spec.rb`) are somewhat interesting.  The benchmarking under `benchmarking.rb` (run `bundle exec ruby benchmarking.rb`) is far more interesting, showing how A* far outperforms BFS on this problem.

####The Solution

The solution uses [A* search](https://en.wikipedia.org/wiki/A*_search_algorithm), which is like [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) and [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) with one key difference: it uses a problem-specific heuristic function to nudge the search algorithm in the direction of the target destination (in this case to help nudge the searcher along the right set of words from the start word to the target word in the dictionary).

Here's a [visualization](https://en.wikipedia.org/wiki/A*_search_algorithm#/media/File:Astar_progress_animation.gif) of A* in action on another problem.

You can see this performance difference play out in the results from `benchmarking.rb`: BFS enqueues and searches many words before finding the target word whereas A* makes almost a direct path towards the target word.

The heuristic function I implemented in this case gives an underestimate of how far the searcher is from the target word at any step in the search process by returning a tight underestimate of the edit distance from the word the searcher is currently on to the target word.  In A*, as long as your heuristic doesn't overestimate the distance to the solution, the search will eventually find the right answer.  If you implement a useful heuristic, then your A* search should outperform BFS and Dijkstra's algorithm.
