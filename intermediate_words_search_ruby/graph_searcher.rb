require 'algorithms'  # use `Containers::Queue` and `Containers::PriorityQueue`
require 'set'


class GraphSearcher
  attr_accessor :queue, :search_helper

  def self.make_graph_searcher(opts)
    search_helper = opts.fetch(:search_helper)
    search_method = opts.fetch(:search_method)
    searcher      = searcher_types.fetch(search_method)
    searcher.new(search_helper: search_helper)
  end

  def self.searcher_types
    { 'A*' => AStarSearcher, 'BFS' => BreadthFirstSearcher }
  end

  def initialize(opts)
    @search_helper = opts.fetch(:search_helper)
  end

  def find_minimal_path(start_node, target_node)
    # TODO: in general, our target could be any one of a collection of
    # nodes, potentially an infinitely large collection.  In the general
    # case, then, we don't want just `current_node == target_node`; we
    # want a general function that tests whether `current_node` is in a
    # collection of nodes or has all the properties of a target node.

    visited_nodes = Set.new
    queue.push(*make_start_state(start_node))

    until queue.empty?
      path         = queue.pop
      current_node = path.last

      return path if current_node == target_node

      unless visited_nodes.include?(current_node)  # unless already visited...
        visited_nodes.add(current_node)
        neighboring_nodes(current_node).each do |neighbor_node|
          unless visited_nodes.include?(neighbor_node)
            queue.push(*make_queue_entry(path, neighbor_node, target_node))
          end
        end
      end
    end
  end

  def neighboring_nodes(node)
    search_helper.neighboring_nodes(node)
  end
end


class AStarSearcher < GraphSearcher
  def initialize(opts)
    @queue = opts.fetch(:queue, Containers::PriorityQueue.new)
    super
  end

  def make_start_state(start_node)
    path     = [ start_node ]
    priority = 0
    [ path, priority ]
  end

  def make_queue_entry(path, next_node, target_node)
    new_path = path + [ next_node ]
    a_star_estimate = search_helper.underestimate_distance(next_node, target_node)
    priority = -1 * (new_path.length + a_star_estimate)
    [ new_path, priority ]
  end
end


class BreadthFirstSearcher < GraphSearcher
  def initialize(opts)
    @queue = opts.fetch(:queue, Containers::Queue.new)
    super
  end

  def make_start_state(start_node)
    path = [ start_node ]
    [ path ]
  end

  def make_queue_entry(path, next_node, _)
    new_path = path + [ next_node ]
    [ new_path ]
  end
end
