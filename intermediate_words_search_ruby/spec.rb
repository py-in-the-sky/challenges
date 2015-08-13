require_relative 'main'
require 'rspec'


TEST_CASES = [
  # start word, target word, minimal path length
  [ 'cat',       'dog',      4   ],
  [ 'cat',       'mistrial', 9   ],
  [ 'strong',    'weak',     7   ],
  [ 'hot',       'cold',     4   ],
  [ 'up',        'down',     5   ],
  [ 'left',      'right',    7   ],
  [ 'light',     'heavy',    10  ],
  [ 'computer',  'virus',    12  ],
  [ 'strike',    'freeze',   6   ],
  [ 'fan',       'for',      3   ],
  [ 'duck',      'dusty',    4   ],
  [ 'rue',       'be',       3   ],
  [ 'rue',       'defuse',   5   ],
  [ 'rue',       'bend',     5   ],
  [ 'zoologist', 'zoology',  nil ]  # no path; these two words are disjoint
]


solver = Solver.new


RSpec.describe 'solver' do
  TEST_CASES.each do |start_word, target_word, minimal_path_length|
    it 'finds the shortest path from start to target word' do
      path = solver.solve(start_word, target_word)
      # puts (path ? "#{path.join('--> ')}" : 'None')
      path_length = path.nil? ? nil : path.length
      expect(path_length).to eq(minimal_path_length)
    end
  end
end
