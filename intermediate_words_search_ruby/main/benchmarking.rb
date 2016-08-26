require 'benchmark'

require_relative 'utilities'
require_relative 'spec'  # TEST_CASES
require_relative '../data_structures/heap'
require_relative '../data_structures/queue'


class Benchmarker
  include Utilities

  def initialize(dictionary_filename: '/usr/share/dict/words')
    @dictionary_filename = dictionary_filename
  end

  def solve_and_show_stats(start_word, target_word)
    puts
    puts "start word:  '#{start_word}'"
    puts "target word: '#{target_word}'"
    show_for_search_method(a_star_searcher, start_word, target_word)
    show_for_search_method(bf_searcher, start_word, target_word)
    puts
  end

  private

  def show_for_search_method(graph_searcher, start_word, target_word)
    path = nil
    benchmark = Benchmark.measure do
      path = graph_searcher.find_minimal_path(start_word, target_word)
    end
    path_len_message = path ? "(#{path.length} words)" : ''

    puts '  ' + graph_searcher.search_method_name
    puts '    ' + (path ? path.join('--> ') : 'None') + '  ' + path_len_message
    puts "    time: #{benchmark.real}"
    puts "    queue stats: #{graph_searcher.queue.show_stats}"
  end

  def a_star_searcher
    make_graph_searcher(word_search_helper, 'A*', QueueStatsWrapper.new(Heap.new))
  end

  def bf_searcher
    make_graph_searcher(word_search_helper, 'BFS', QueueStatsWrapper.new(Queue.new))
  end
end


class QueueStatsWrapper
  def initialize(queue)
    @queue = queue
    @n_pops = 0
    @n_pushes = 0
  end

  def show_stats
    "#{@n_pops} pops off the queue and #{@n_pushes} pushes onto the queue"
  end

  def empty?
    @queue.empty?
  end

  def pop
    @n_pops += 1
    @queue.pop
  end

  def push(*args)
    @n_pushes += 1
    @queue.push(*args)
  end
end


if __FILE__ == $0
  benchmarker = Benchmarker.new
  TEST_CASES.each do |start_word, target_word, _|
    benchmarker.solve_and_show_stats(start_word, target_word)
  end
end
