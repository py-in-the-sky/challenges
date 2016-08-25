class WordSearchHelper
  attr_accessor :trie

  def initialize(opts)
    @trie = opts.fetch(:trie)
  end

  def underestimate_distance(current_word, target_word)
    # return value that is less than or equal to edit distance
    # this is a cheap way to get a tight underestimate of the edit distance:
    # underestimate steps to transform shorter word into longer word
    shorter_word, longer_word = [current_word, target_word].sort_by(&:length)
    n_additions  = longer_word.length - shorter_word.length
    n_transforms = shorter_word
      .each_char
      .reject { |char| longer_word.include?(char) }
      .length

    n_additions  + n_transforms
  end

  def neighboring_nodes(word)
    [
      neighbors_by_addition(word),
      neighbors_by_subtraction(word),
      neighbors_by_transformation(word)
    ].flatten
  end

  private

  def neighbors_by_addition(word)
    word_partitions_with_trie(word).flat_map do |prefix, suffix, trie_under_prefix|
      trie_under_prefix
        .entries  # characters
        .select { |_, trie_under_char| trie_under_char.include?(suffix) }
        .map { |char, _| prefix + char + suffix }
    end
  end

  def neighbors_by_subtraction(word)
    result = word_partitions_around_chars_with_trie(word)

    result = result.select do |_, _, suffix, trie_under_prefix|
      trie_under_prefix.include?(suffix)
    end

    result.map { |prefix, _, suffix, _| prefix + suffix }
  end

  def neighbors_by_transformation(word)
    result = word_partitions_around_chars_with_trie(word)
    result.flat_map do |prefix, char, suffix, trie_under_prefix|
      trie_under_prefix
        .entries
        .reject { |char2, _| char2 == char }
        .select { |_, trie_under_char2| trie_under_char2.include?(suffix) }
        .map { |char2, _| prefix + char2 + suffix }
    end
  end

  def word_partitions_with_trie(word)
    t = trie
    result = []

    (0..word.length).each do |i|
      prefix, suffix = word[0...i].to_s, word[i...word.length].to_s
      result << [prefix, suffix, t]
      t = suffix.empty? ? nil : t.get(suffix[0])
    end

    result
  end

  def word_partitions_around_chars_with_trie(word)
    t = trie
    result = []

    word.each_char.each_with_index.each do |char, i|
      prefix, suffix = word[0...i].to_s, word[(i+1)...word.length].to_s
      result << [prefix, char, suffix, t]
      t = t.get(char)
    end

    result
  end
end
