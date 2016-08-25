# A linked list
# A linked list is in a valid state after a method exits if:
#  - its length is <= 1 and @front == @back
#  - its length is 0 and @front == nil
#  - its length is > 1
class Queue
  def initialize
    @front = @back = nil
  end

  def empty?
    @front.nil?
  end

  def top
    fail if empty?
    @front.value
  end

  def push(value)
    new_node = Node.new(value)

    if empty?
      @front = @back = new_node
    else
      @back = @back.child = new_node
    end

    nil
  end

  def pop
    fail if empty?  # length == 0

    old_top = top

    if @front == @back  # length == 1
      @front = @back = nil
    else  # length > 1
      @front = @front.child
    end

    old_top
  end

  class Node
    attr_reader :value
    attr_accessor :child

    def initialize(value)
      @value = value
      @child = nil
    end
  end
end
