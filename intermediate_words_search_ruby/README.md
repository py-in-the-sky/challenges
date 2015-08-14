This is a solution to the problem described in the first paragraph of [this Quora discussion](http://www.quora.com/What-is-the-importance-of-this-algorithm).  I recommend viewing it in Firefox; for some reason, viewing the discussion in Firefox hides all mention of a solution under a "read more" link; I just found that this is not the case in some other browsers, at least on my computer.

The design in `graph_searcher.rb` is largely borrowed from Peter Norvig's excellent [Design of Computer Programs](https://www.udacity.com/course/design-of-computer-programs--cs212) course.

I have implemented a [Python version](https://github.com/py-in-the-sky/challenges/tree/master/intermediate_words_search_python) that runs roughly five times faster on most of the example cases used for benchmarking, which suggests there are some subtleties to Ruby performance that I don't understand.  Admittedly, I have a better grasp on Python than on Ruby.

The tests under `spec.rb` (run `bundle exec rspec spec.rb`) are somewhat interesting.  The benchmarking under `benchmarking.rb` (run `bundle exec ruby benchmarking.rb`) is far more interesting, showing how A* far outperforms BFS on this problem.

####The Solution

The solution uses [A* search](https://en.wikipedia.org/wiki/A*_search_algorithm), which is like [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) and [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) with one key difference: it uses a problem-specific heuristic function to nudge the search algorithm in the direction of the target destination (in this case to help nudge the searcher along the right set of words from the start word to the target word in the dictionary).

Here's a [visualization](https://en.wikipedia.org/wiki/A*_search_algorithm#/media/File:Astar_progress_animation.gif) of A* in action on another problem.

You can see this performance difference play out in the results from `benchmarking.rb`: BFS enqueues and searches many words before finding the target word whereas A* makes almost a direct path towards the target word.

The heuristic function I implemented in this case gives an underestimate of how far the searcher is from the target word at any step in the search process by returning a tight underestimate of the edit distance from the word the searcher is currently on to the target word.  In A*, as long as your heuristic doesn't overestimate the distance to the solution, the search will eventually find the right answer; if you implement a useful heuristic, then the search should outperform BFS and Dijkstra's algorithm.

The reason this heuristic is useful is because it's quick to run and because edit distance, which it approximates, is a decent measure of how many "words away" one word is from another.  For example, in the path `cat--> cot--> dot--> dog`, `dot` is only one edit away from `dog`.  Therefore, among all of `cot`'s neighbors, `dot` is interesting and should be prioritized for a visit; on the other hand, `cop` is less interesting than `dot` since it's "further" from `dog` (it's two edits away from `dog`).  And regarding the starting word, `cat`, `cot` is a more interesting nieghbor and should be prioritized over `at` since `cot` is only two edits away from `dog`.  BFS, on the other hand, has no notion of prioritizing neighboring words.
