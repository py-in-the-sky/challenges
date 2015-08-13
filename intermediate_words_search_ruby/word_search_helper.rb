require_relative 'trie_utilities'


class WordSearchHelper
  include TrieUtilities

  attr_accessor :trie

  def initialize(opts)
    @trie = opts.fetch(:trie)
  end

  def underestimate_distance(current_word, target_word)
    # return value that is less than or equal to edit distanqce
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
    all_neighbors = [
      neighbors_by_addition(word),
      neighbors_by_subtraction(word),
      neighbors_by_transformation(word)
    ]

    all_neighbors.lazy.flat_map { |word2| word2 }
  end

  def neighbors_by_addition(word)
    word_partitions_with_trie(word)
      .flat_map do |prefix, suffix, trie_under_prefix|
        trie_items(trie_under_prefix)
          .select { |_, trie_under_char| trie_contains?(trie_under_char, suffix) }
          .map    { |char, _|            prefix + char + suffix }
      end
  end

  def neighbors_by_subtraction(word)
    word_partitions_around_chars_with_trie(word)
      .select do |_, _, suffix, trie_under_prefix|
        trie_contains?(trie_under_prefix, suffix)
      end
      .map { |prefix, _, suffix, _| prefix + suffix }
  end

  def neighbors_by_transformation(word)
    word_partitions_around_chars_with_trie(word)
      .flat_map do |prefix, char, suffix, trie_under_prefix|
        trie_items(trie_under_prefix)
          .reject { |char2, _|            char2 == char }
          .select { |_, trie_under_char2| trie_contains?(trie_under_char2, suffix) }
          .map    { |char2, _|            prefix + char2 + suffix }
      end
  end

  def word_partitions_with_trie(word)
    t = trie
    word_len = word.length

    (0..word_len)
      .lazy
      .map do |i|
        prefix, suffix = word[0...i].to_s, word[i...word_len].to_s
        partition_with_trie = [prefix, suffix, t]
        t = trie_get(t, suffix[0])
        partition_with_trie
      end
  end

  def word_partitions_around_chars_with_trie(word)
    t = trie
    word_len = word.length

    word
      .each_char
      .lazy
      .each_with_index
      .map do |char, i|
        prefix, suffix = word[0...i].to_s, word[(i+1)...word_len].to_s
        partition_with_trie = [prefix, char, suffix, t]
        t = trie_get(t, char)
        partition_with_trie
      end
  end
end
