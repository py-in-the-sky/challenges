require_relative 'main'
require_relative 'spec'  # TEST_CASES
require 'algorithms'  # use `Containers::Queue` and `Containers::PriorityQueue`
require 'benchmark'


class Benchmarker < Solver
  include TrieUtilities

  def solve_and_show_stats(start_word, target_word)
    word_search_helper  # lazy init

    puts
    show_for_search_method('A*', a_star_searcher, start_word, target_word)
    show_for_search_method('BFS', bf_searcher, start_word, target_word)
    puts
  end

  def show_for_search_method(method_name, searcher, start_word, target_word)
    path = nil
    benchmark = Benchmark.measure do
      path = searcher.find_minimal_path(start_word, target_word)
    end

    path_len_message = path ? "  (#{path.length} words)" : ''

    puts method_name
    puts '  ' + (path ? path.join('--> ') : 'None') + path_len_message
    puts "  time: #{benchmark.real}"
    puts "  queue stats: #{searcher.queue.show_stats}"
  end

  def a_star_searcher
    opts = {
      queue: QueueStatsWrapper.new(Containers::PriorityQueue.new),
      search_helper: word_search_helper
    }
    AStarSearcher.new(opts)
  end

  def bf_searcher
    opts = {
      queue: QueueStatsWrapper.new(Containers::Queue.new),
      search_helper: word_search_helper
    }
    BreadthFirstSearcher.new(opts)
  end
end


class QueueStatsWrapper
  def initialize(queue)
    @queue    = queue
    @n_pops   = 0
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
  test_cases  = TEST_CASES.map { |test_case| test_case[0..1] }

  test_cases.each do |start_word, target_word|
    benchmarker.solve_and_show_stats(start_word, target_word)
  end

end

