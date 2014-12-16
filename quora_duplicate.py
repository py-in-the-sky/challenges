"""
see: https://www.hackerrank.com/contests/quora-haqathon/challenges/duplicate
"""

import re
from json import loads
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.ensemble import BaggingClassifier
from nltk.stem.lancaster import LancasterStemmer

WORD_RE = re.compile(r'\w+')
STEMMER = LancasterStemmer()
STOP_WORDS = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
    'll', 're', 'm', 've'
]

def parse_t(test_string):
    return test_string.split()

def parse_d(training_string):
    key1, key2, score = training_string.split()
    return [key1, key2, -1 if score == '0' else 1]

def parse_topic(question_topic):
    return question_topic['name'] if question_topic else ''

def stem(word):
    return STEMMER.stem(word)

def parse_text(question_text):
    return set(stem(w) for w in WORD_RE.findall(question_text.lower())
               if w not in STOP_WORDS)

def parse_q(question_json):
    q = loads(question_json)
    q_body = {
        'question_text': parse_text(q['question_text']),
        'context_topic': parse_topic(q['context_topic']),
        'topics': [parse_topic(t) for t in q['topics']],
        'view_count': q['view_count'],
        'follow_count': q['follow_count'],
        'age': int(q['age'])
    }
    return (q['question_key'], q_body)

def score_context(q1, q2):
    context1, topics1 = q1['context_topic'], q1['topics']
    context2, topics2 = q2['context_topic'], q2['topics']
    s1 = (context1 in topics2) if context1 else False
    s2 = (context2 in topics1) if context2 else False
    s3 = (context1 == context2) if context1 and context2 else False
    return int(s3), (s1 + s2)

def score_topics(q1, q2):
    return len(set(q1['topics']) & set(q2['topics']))

def generic_score(q1, q2, field_name):
    diff = float(abs(q1[field_name] - q2[field_name]))
    max_quant = max(q1[field_name], q2[field_name])
    if max_quant:
        return int(100 * diff / max_quant)
    else:
        return 0

def reduce_pair(key1, key2):
    q1, q2 = questions[key1], questions[key2]
    t1, t2 = q1['question_text'], q2['question_text']
    n_words_matched = len(t1 & t2)
    n_words = len(t1 | t2)
    percent_words_matched = int(100* float(n_words_matched) / n_words) if n_words else 0
    context_score1, context_score2 = score_context(q1, q2)
    topic_score = score_topics(q1, q2)
    view_score = generic_score(q1, q2, 'view_count')
    follow_score = generic_score(q1, q2, 'follow_count')
    age_score = generic_score(q1, q2, 'age')
    return [n_words_matched, percent_words_matched, context_score1,
            context_score2, topic_score, view_score, follow_score, age_score]

def predict(key1, key2, clf):
    if key1 == key2:
        return 1
    data = reduce_pair(key1, key2)
    prediction_score = clf.predict([data])[0]
    return 0 if prediction_score < 1 else 1

## get data

Q = int(raw_input())
questions = dict(parse_q(raw_input()) for _ in xrange(Q))

## train here

D = int(raw_input())
training = (parse_d(raw_input()) for _ in xrange(D))

X, Y = zip(*((reduce_pair(k1, k2), -1 if score < 1 else 1) for k1,k2,score in training))
base_clf = RandomForestClassifier(n_estimators=7, min_samples_leaf=4) 

clf = Pipeline([
    ('classification', BaggingClassifier(base_estimator=base_clf, random_state=1, n_estimators=16))
]).fit(X, Y)

## predict here

N = int(raw_input())
testing = (parse_t(raw_input()) for _ in xrange(N))

for key1, key2 in testing:
    print key1, key2, predict(key1, key2, clf)
