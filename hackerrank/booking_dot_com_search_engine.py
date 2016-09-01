"""
Data Challenges:
    * What to do if a city does not have an endorsement for one of the queried
      passions?  E.g., Say 'Walking' and 'Skydiving' were queried; how should
      we handle a city that's the best in the world for walking but has no
      endorsements for skydiving?
        * ANSWER: Give a default low weight to the city's score for that (missing)
          passion, rather than ignore the city.


P(city | passion) is proportional to P(passion | city) * P(city)
"""


from __future__ import division
from operator import mul
from collections import defaultdict, namedtuple


### Search Engine ###

class SearchEngine:
    def __init__(self, index, response_size=10, missing_passion_weight=0.01):
        self.index = index
        self.response_size = response_size
        self.missing_passion_weight = missing_passion_weight

    def search(self, passions):
        "passions -> cities"
        cities = set(c for p in passions for c in self.index.cities_by_passion(p))
        cities_sorted = sorted(cities,
                               key=lambda city: self._P_city_given_passions(city, passions),
                               reverse=True)
        return cities_sorted[:self.response_size]

    def _P_city_given_passions(self, city, passions):
        P_city = self._P_city(city)
        product = lambda numbers: reduce(mul, numbers, 1)
        # return product((P_city * self._P_passion_given_city(p, city)) / self._P_passion(p) for p in passions)

        # This is technically not P(city | passions) since we do not divide by P(passion)
        # We choose not to divide by P(passion) since we want to weight all passions submitted
        # by the users equally.
        return product((P_city * self._P_passion_given_city(p, city)) for p in passions)

    def _P_passion_given_city(self, passion, city):
        num = self.index.passion_endorsements_by_city(passion, city)
        denom = self.index.total_endorsements_by_city(city=city)
        return self.missing_passion_weight if num is None else num / denom

    def _P_city(self, city):
        num = self.index.total_endorsements_by_city(city=city)
        denom = self.index.total_endorsements_by_city()
        return num / denom

    def _P_passion(self, passion):
        num = self.index.total_endorsements_by_passion(passion=passion)
        denom = self.index.total_endorsements_by_passion()
        return num / denom


### Data Indexes ###

class Index:
    def __init__(self, data):
        self._cities_by_passion = construct_cities_by_passion(data)
        self._passion_endorsements_by_city = construct_passion_endorsements_by_city(data)
        self._total_endorsements_by_city = construct_total_endorsements_by_city(data)
        self._total_endorsements_by_passion = construct_total_endorsements_by_passion(data)

    def cities_by_passion(self, passion):
        return self._cities_by_passion[passion]

    def passion_endorsements_by_city(self, passion, city):
        return self._passion_endorsements_by_city[city].get(passion)

    def total_endorsements_by_city(self, city=None):
        key = city or '__total__'
        return self._total_endorsements_by_city[key]

    def total_endorsements_by_passion(self, passion=None):
        key = passion or '__total__'
        return self._total_endorsements_by_passion[key]


def construct_cities_by_passion(data):
    index = defaultdict(set)

    for row in data:
        index[row.passion].add(row.city)

    return dict(index)


def construct_passion_endorsements_by_city(data):
    index = defaultdict(lambda: defaultdict(int))

    for row in data:
        index[row.city][row.passion] += row.endorsements

    return dict(index)


def construct_total_endorsements_by_city(data):
    index = defaultdict(int)
    total = 0

    for row in data:
        index[row.city] += row.endorsements
        total += row.endorsements

    index['__total__'] = total
    return dict(index)


def construct_total_endorsements_by_passion(data):
    index = defaultdict(int)
    total = 0

    for row in data:
        index[row.passion] += row.endorsements
        total += row.endorsements

    index['__total__'] = total
    return dict(index)


Row = namedtuple('Row', 'city passion endorsements')


### Helpers ###

def read_data(lines): return tuple(parse_line(l) for l in lines)


def parse_line(line):
    line = line.split()
    city, passion = line[:2]
    endorsements = int(line[2])
    return Row(city, passion, endorsements)


### Testing ###

# (city, passion, endorsement count) triples
DATA = """
Amsterdam Food 5000
Amsterdam Walking 4500
Amsterdam Hiking 500
Amsterdam Sports 900
Amsterdam Museums 4150
Amsterdam Nightlife 5550
Amsterdam PokemonGo 110
Amsterdam Music 4550
Portland Food 950
Portland Hiking 1100
Portland Walking 400
Portland Sports 300
Portland Museums 310
Portland Music 700
Portland Sharkdiving 8
Eugene Food 1245
Eugene Walking 1195
Eugene Sports 2700
Eugene Hiking 1200
"""


def tests():
    lines = (l.strip() for l in DATA.split('\n') if l.strip())
    data = read_data(lines)
    index = Index(data)
    search_engine = SearchEngine(index, response_size=2)

    test_passions = [
        'Sports Walking'.split(),
        'Sports Walking Hiking'.split(),
        'Food Museums'.split(),
        'Music Sharkdiving Nightlife Hiking'.split()
    ]

    print
    for passions in test_passions:
        print '{} -> {}'.format(passions, search_engine.search(passions))
        print


if __name__ == '__main__':
    tests()
