require_relative '../data_structures/trie'
require_relative '../graph_searcher/a_star'
require_relative '../graph_searcher/breadth_first'
require_relative '../helpers/word_search_helper'


module Utilities
  BFS = 'BFS'.freeze
  A_STAR = 'A*'.freeze

  def make_graph_searcher(search_helper, search_method, queue = nil)
    searcher_type = searcher_types.fetch(search_method)
    searcher_type.new(search_helper: search_helper, queue: queue)
  end

  def searcher_types
    {
      A_STAR => GraphSearcher::AStarSearcher,
      BFS => GraphSearcher::BreadthFirstSearcher
    }
  end

  def word_search_helper
    @word_search_helper ||= WordSearchHelper.new({
      trie: make_trie_from_dictionary_file
    })
  end

  def make_trie_from_dictionary_file
    @trie ||= begin
      trie = Trie.new

      File.open(@dictionary_filename) do |f|
        f.each_line { |word| trie.put(word.strip.downcase) }
      end

      trie
    end
  end
end
