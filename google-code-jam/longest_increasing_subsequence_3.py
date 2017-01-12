
'''
Solves large input in 0.692 seconds
runs O(n**2)
'''

def get_lis_complement(house_list): # lis = longest increasing subsequence
  # house_list is list of house heights, listed in order of distance of house from the lake
  num_houses = len(house_list)
  max_per_house = [1 for _ in xrange(num_houses)]
  for i in xrange(num_houses-2, -1, -1): # start at second-to-last house
    try:
      max_per_house[i] += max(max_per_house[j] for j in xrange(i+1, num_houses) 
                              if house_list[i] < house_list[j])
    except ValueError:
      pass # no need to increment up if no subsequent house is taller
  return num_houses - max(max_per_house)

if __name__ == '__main__':
  file = open('C-large-practice.in', 'r')
  file.readline()
  output = open('answer.out', 'w')
  case = 1
  while file.readline():
    houses = map(int, file.readline().strip().split())
    answer = get_lis_complement(houses)
    #print 'Case #{}: {}'.format(case, answer)
    output.write('Case #{}: {}'.format(case, answer) + '\n')
    case += 1
  output.close()
  file.close()
  print 'done!'

'''
practice input:
4
4
1 4 3 3
5
3 4 6 7 10
4
4 3 2 1
5
4 5 6 1 7

practice output:
Case #1: 2
Case #2: 0
Case #3: 3
Case #4: 1
'''