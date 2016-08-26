# A priority queue
# A priority queue is in a valid state after a method exits if:
#  - The heap and all subheaps respect the parent-child ordering (i.e., the
#    root is the minimum element -- or maximum if `min_top` is false)
class Heap
  def initialize(min_top: true)
    @array = []
    @min_top = min_top
  end

  def empty?
    @array.empty?
  end

  def top
    fail if empty?
    @array[0]
  end

  def push(item)
    # Append item to end and then reestablish the parent-child ordering in the
    # heap before exiting.
    @array << item
    bubble_up
    nil
  end

  def pop
    fail if empty?
    return @array.pop if @array.length == 1

    # Replace value at top of heap with value at the bottom and then reestablish
    # the parent-child ordering in the heap before returning the old top value.
    old_top = @array[0]
    bottom = @array.pop
    @array[0] = bottom
    bubble_down
    old_top
  end

  private

  def bubble_up
    j = @array.length - 1
    parent_idx = parent_index(j)

    until parent_idx.nil? || parent_child_ordering?(parent_idx, j)
      @array[j], @array[parent_idx] = @array[parent_idx], @array[j]
      j = parent_idx
      parent_idx = parent_index(j)
    end
  end

  def bubble_down
    fail if empty?
    i = 0
    child_idx = target_child_index(i)

    while child_idx && !parent_child_ordering?(i, child_idx)
      @array[i], @array[child_idx] = @array[child_idx], @array[i]
      i = child_idx
      child_idx = target_child_index(i)
    end
  end

  def child_indices(idx)
    [idx*2+1, idx*2+2]
  end

  def parent_index(idx)
    return nil if idx <= 0
    idx%2==0 ? (idx-2)/2 : (idx-1)/2
  end

  def parent_child_ordering?(parent_idx, child_idx)
    fail unless parent_idx < child_idx && child_idx < @array.length
    p, c = @array[parent_idx], @array[child_idx]
    comp = p <=> c
    @min_top ? comp <= 0 : comp >= 0
  end

  def target_child_index(idx)
    i, j = child_indices(idx)

    if i >= @array.length
      nil
    elsif j >= @array.length
      i
    elsif @min_top  # return index of smallest child
      comp = @array[i] <=> @array[j]
      comp <= 0 ? i : j
    else  # return index of largest child
      comp = @array[i] <=> @array[j]
      comp <= 0 ? j : i
    end
  end
end


def tests
  a = [4, 7, 2, 3, 9, 0, 10]
  b = []
  c = []
  h1 = Heap.new
  h2 = Heap.new(min_top: false)

  a.each do |n|
    h1.push(n)
    h2.push(n)
  end

  until h1.empty?
    b << h1.pop
  end

  until h2.empty?
    c << h2.pop
  end

  fail unless b == a.sort
  fail unless c == a.sort.reverse

  puts 'tests pass!'
end


if __FILE__ == $0
  tests
end
