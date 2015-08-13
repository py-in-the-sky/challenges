module TrieUtilities

  WORD_END_TOKEN = nil

  def tree
    Hash.new { |hash, key| hash[key] = tree }
  end

  def make_trie_from_words_file(filename)
    trie = tree
    file_lines(filename) { |word| trie_put(trie, word.strip.downcase) }
    trie
  end

  def make_trie_from_words(words)
    words.reduce(tree) { |trie, word| trie_put(trie, word.strip.downcase) }
  end

  def trie_put(trie, word)
    return trie unless word
    t = word.each_char.reduce(trie) { |t, char| t[char] }
    t[WORD_END_TOKEN] = WORD_END_TOKEN
    trie
  end

  def trie_get(trie, word)
    return nil unless word
    word
      .each_char
      .reduce(trie) { |trie, char| trie ? trie.fetch(char, nil) : nil }
  end

  def trie_contains?(trie, word)
    t = trie_get(trie, word)
    t && t.has_key?(WORD_END_TOKEN)
  end

  def trie_items(trie)
    trie.lazy.reject { |char, _| char == WORD_END_TOKEN }
  end

  def file_lines(filename)
    File.open(filename) { |f| f.each_line { |line| yield line } }
  end
end
