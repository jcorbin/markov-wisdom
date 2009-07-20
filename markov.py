import re
import random

class Parse(object):
    @classmethod
    def fileChunks(cls, f, size=1024):
        """
        Iterates a file in fixed-size chunks; the final chunk of coruse
        may, and most likely will be, be short.
        """
        while True:
            buf = f.read(size)
            if not len(buf):
                break
            yield buf

    _sentenceReCache = {}

    @classmethod
    def sentences(cls, iterable, endPunc=r"\.;"):
        """
        Iterates sentences in a source
        """
        if isinstance(iterable, file):
            iterable = Parse.fileChunks(iterable)
        if not endPunc in cls._sentenceReCache:
            cls._sentenceReCache[endPunc] = re.compile(
                r"(.+?)["+endPunc+r"](.*)", re.S
            )
        sen = cls._sentenceReCache[endPunc]
        if not '__ws' in cls._sentenceReCache:
            cls._sentenceReCache['__ws'] = re.compile(r"\s+")
        ws = cls._sentenceReCache['__ws']

        buf = ''
        for chunk in iterable:
            chunk = chunk.strip()
            while len(chunk):
                m = sen.match(chunk)
                if m:
                    (frag, rest) = m.groups()
                    buf += frag
                    yield ws.sub(' ', buf).strip()
                    buf = ''
                    chunk = rest
                else:
                    buf += chunk
                    break

    _phraseReCache = {}

    @classmethod
    def phrases(
        cls,
        sentence,
        wordChar=r"[\w\-']",
        size=3,
        trailing=(None, None)
    ):
        """
        Iterates phrases in a sentence

        Arguments
            wordChar: the character class to use in finding words
            size: how many words long should each phrase be
            trailing: how many words to yield with None padding elements
            at either end of the sentence; for example:
                    >>> s = 'alpha bravo charlie delta'
                    >>> pprint(list(
                    ...     phrases(s, size=3, trailing=(1, 1))
                    ... ))
                    [(None, None, 'alpha'),
                     (None, 'alpha', 'bravo'),
                     ('alpha', 'bravo', 'charlie'),
                     ('bravo', 'charlie', 'delta'),
                     ('charlie', 'delta', None),
                     ('delta', None, None)]
                    >>> pprint(list(
                    ...     phrases(s, size=3, trailing=(None, 2))
                    ... ))
                    [('alpha', 'bravo', 'charlie'),
                     ('bravo', 'charlie', 'delta'),
                     ('charlie', 'delta', None)]
        """
        if not wordChar in cls._phraseReCache:
            cls._phraseReCache[wordChar] = re.compile(
                r"\b("+wordChar+r"+)\b"
            )
        wordRe = cls._phraseReCache[wordChar]

        buf = [] if trailing[0] is None else [None] * (size-trailing[0])

        for word in wordRe.finditer(sentence):
            buf.append(word.group(0))
            if len(buf) > size:
                buf.pop(0)
            if len(buf) == size:
                yield tuple(buf)

        if trailing[1] is not None:
            for i in xrange(size-trailing[1]):
                buf.append(None)
                buf.pop(0)
                yield tuple(buf)

class Corpus(object):
    def __init__(self, source):
        self._source = source
        self._db = None

    @property
    def source(self):
        source = self._source
        if type(source) == str:
            source = open(source, 'r')
        return source

    def phrases(self, trailing=(None, None)):
        for sentence in Parse.sentences(self.source):
            sentence = sentence.lower()
            for phrase in Parse.phrases(sentence, trailing=trailing):
                yield phrase

    def buildDb(self):
        db = {}
        for phrase in self.phrases(trailing=(1, 2)):
            key = (phrase[0], phrase[1])
            if not key in db:
                db[key] = set()
            db[key].add(phrase[2])
        return db

    @property
    def db(self):
        if self._db is None:
            self._db = self.buildDb()
        return self._db

    def nextword(self, wordpair=None):
        if wordpair is None:
            wordpair = (None, None)
        if not wordpair in self.db:
            return None
        choices = list(self.db[wordpair])
        if len(choices) == 1:
            return choices[0]
        ret = None
        while ret is None:
            ret = random.choice(choices)
        return ret

    def canend(self, wordpair):
        if not wordpair in self.db:
            return True
        return None in self.db[wordpair]

    def words(self, min=5, max=50):
        buf = [None, None]
        pair = tuple(buf)
        count = 0
        while count < max and (count < min or not self.canend(pair)):
            next = self.nextword(pair)
            if next is None:
                break
            yield next
            buf.append(next)
            buf.pop(0)
            pair = tuple(buf)
            count += 1

    def sentence(self, min=5, max=50):
        words = self.words(min=min, max=max)
        return ' '.join(words).capitalize()+'.'

# vim:set ts=4 sw=4 expandtab:
