require_relative 'base'
require_relative '../data_structures/heap'


module GraphSearcher
  class AStarSearcher < Base
    def self.search_method_name
      'A*'
    end

    def search_method_name
      self.class.search_method_name
    end

    def default_queue
      Heap.new
    end

    def make_start_state(start_node)
      priority = 0
      path = [ start_node ]
      [ priority, path ]
    end

    def make_queue_entry(path, next_node, target_node)
      new_path = path + [ next_node ]
      a_star_estimate = search_helper.underestimate_distance(next_node, target_node)
      priority = new_path.length + a_star_estimate
      [ priority, new_path ]
    end

    def extract_path(priority_and_path)
      priority_and_path.last
    end
  end
end
