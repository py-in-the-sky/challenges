require_relative 'base'
require_relative '../data_structures/queue'


module GraphSearcher
  class BreadthFirstSearcher < Base
    def self.search_method_name
      'BFS'
    end

    def search_method_name
      self.class.search_method_name
    end

    def default_queue
      Queue.new
    end

    def make_start_state(start_node)
      [ start_node ]
    end

    def make_queue_entry(path, next_node, _)
      path + [ next_node ]
    end
  end
end
