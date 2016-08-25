class Trie
  class WordEndToken; end

  def self.tree
    Hash.new { |hash, key| hash[key] = self.tree }
  end

  def self.from_words(words)
    instance = new
    words.each { |word| instance.put(word) }
    instance
  end

  def initialize(tree = nil)
    @tree = tree || self.class.tree
  end

  def include?(word)
    t = get(word)
    !t.nil? && t.has_key?(WordEndToken)
  end

  def get(prefix)
    t = prefix.each_char.reduce(@tree) { |t, char| t ? t.fetch(char, nil) : nil }
    t && self.class.new(t)
  end

  def put(word)
    t = word.each_char.reduce(@tree) { |t, char| t[char] }
    t[WordEndToken] = WordEndToken
    self
  end

  def entries
    @tree
      .reject { |char, _| char == WordEndToken }
      .map { |char, tree| [char, self.class.new(tree)]}
  end

  def has_key?(key)
    @tree.has_key?(key)
  end
end
