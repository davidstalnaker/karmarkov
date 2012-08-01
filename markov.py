from collections import Counter, defaultdict
from random import randint
import re

START = '^'
END = '$'

class MarkovChain(object):
    def __init__(self, comments):
        self.words = defaultdict(lambda: defaultdict(int))
        self.update(comments)

    def update(self, comments):
        for c in comments:
            karma = c[1]
            sents = re.split(r'[\.!\?]', c[0])
            for sent in sents:
                words = sent.split()
                if len(words) > 0:
                    for first, second in zip(words, words[1:]):
                        self.words[first][second] += karma
                    self.words[START][words[0]] += karma
                    self.words[words[-1]][END] += karma

    def generate_next(self, word):
        candidates = self.words[word]
        total_karma = sum(candidates.values())
        r = randint(0, total_karma)
        for w, k in candidates.items():
            if r < k:
                return w
            else:
                r -= k

    def generate_sent(self, start=None, max_length=20):
        words = []
        prev = start if start else START
        for i in range(max_length):
            prev = self.generate_next(prev)
            if prev == END:
                break
            else:
                words.append(prev)
        return ' '.join(words)

    def __repr__(self):
        return {k: dict(v) for k, v in dict(self.words).items()}.__repr__()
