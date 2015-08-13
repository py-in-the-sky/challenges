require_relative 'trie_utilities'
require_relative 'word_search_helper'
require_relative 'graph_searcher'


class Solver
  include TrieUtilities

  WORDS_FILENAME = '/usr/share/dict/words'
  SEARCH_METHOD  = 'A*'

  def initialize(opts = {})
    @words_filename = opts.fetch(:words_filename, WORDS_FILENAME)
    @search_method  = opts.fetch(:search_method,  SEARCH_METHOD)
  end

  def solve(start_word, target_word)
    graph_searcher.find_minimal_path(start_word, target_word)
  end

  def graph_searcher
    opts = {
      search_method: @search_method,
      search_helper: word_search_helper
    }
    GraphSearcher.make_graph_searcher(opts)
  end

  def word_search_helper
    @word_search_helper ||= begin
      trie = make_trie_from_words_file(@words_filename)
      WordSearchHelper.new(trie: trie)
    end
  end
end


if __FILE__ == $0
  solver = Solver.new
  puts solver.solve(ARGV[0].strip.downcase, ARGV[1].strip.downcase).join('--> ')
end
