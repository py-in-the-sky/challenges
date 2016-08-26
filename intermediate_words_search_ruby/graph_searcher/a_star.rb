require_relative 'base'
require_relative '../data_structures/heap'


module GraphSearcher
  class AStarSearcher < Base
    def search_method_name
      'A*'
    end

    def default_queue
      Heap.new
    end

    def make_start_state(start_node)
      SearchState.new([ start_node ], 0)
    end

    def make_next_state(state, next_node, target_node)
      new_path = state.path + [ next_node ]
      a_star_estimate = search_helper.underestimate_distance(next_node, target_node)
      SearchState.new(new_path, new_path.length + a_star_estimate)
    end

    class SearchState
      attr_reader :path, :current_node, :priority

      def initialize(path, priority)
        @path = path
        @current_node = path.last
        @priority = priority
      end

      def <=> (other)
        priority <=> other.priority
      end
    end
  end
end
