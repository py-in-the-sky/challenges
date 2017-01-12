
def memo(f):
    """Borrowed from Peter Norvig's Design of Computer Programs course
    on Udacity.com:
    Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

@memo
def count_longest_incr_subseq(index):
    if index == nhouses - 1: return 1
    lengths = [0] + [count_longest_incr_subseq(ind)
                     for ind in xrange(index+1, nhouses)
                     if houses[index] < houses[ind]]
    #print nhouses, max(lengths)
    return 1 + max(lengths)


if __name__ == '__main__':
    file = open('C-small-practice.in', 'r')
    file.readline()
    output = open('answer.out', 'w')
    case = 1
    while file.readline():
        houses = map(int, file.readline().strip().split())
        nhouses = len(houses)
        lengths = []
        for i in xrange(nhouses):
            length = count_longest_incr_subseq(i)
            lengths.append(length)
        print nhouses, max(lengths)
        answer = nhouses - max(lengths)
        output.write('Case #{}: {}'.format(case, answer) + '\n')
        case += 1
    
    output.close()
    file.close()
    print 'done!'