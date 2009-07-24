import re
import random

sentenceReCache = {}
phraseReCache = {}

def sentences(source, endPunc=r"\.:;\?!"):
    """
    Iterates sentences in a source
    """
    if not endPunc in sentenceReCache:
        sentenceReCache[endPunc] = re.compile(
            r"(.+?)["+endPunc+r"](.*)", re.S
        )
    sen = sentenceReCache[endPunc]
    ws = re.compile(r"\s+")

    buf = ''
    for chunk in source:
        chunk = chunk.strip()
        while len(chunk):
            m = sen.match(chunk)
            if m:
                (frag, rest) = m.groups()
                buf += ' '+frag
                yield ws.sub(' ', buf).strip()
                buf = ''
                chunk = rest
            else:
                buf += ' '+chunk
                break

def phrases(
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
    if not wordChar in phraseReCache:
        phraseReCache[wordChar] = re.compile(
            r"\b("+wordChar+r"+)\b"
        )
    wordRe = phraseReCache[wordChar]

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

class SentenceOverrun(Exception):
    pass

class Corpus(object):
    def __init__(self, source):
        self._source = source
        self._links = None
        self._form = None

    @property
    def source(self):
        """
        The source material.
        """
        source = self._source
        if type(source) == str:
            source = open(source, 'r')
        return source

    def phrases(self, trailing=(1, 2)):
        """
        Yields phrases from each sentence in the source.
        """
        for sentence in sentences(self.source):
            for phrase in phrases(sentence, trailing=trailing):
                yield phrase

    def _build(self):
        """
        Builds the phrase and form database.
        """
        links = {}
        form = {}
        for phrase in self.phrases():
            if phrase[1] is not None and phrase[2] is not None:
                (a, b) = (phrase[2].lower(), phrase[2])
                if a != b:
                    form[a] = b
            phrase = tuple(
                None if s is None else s.lower() for s in phrase
            )
            key = (phrase[0], phrase[1])
            if not key in links:
                links[key] = set()
            links[key].add(phrase[2])
        self._links = links
        self._form = form

    @property
    def links(self):
        """
        The phrase database, a mapping of word pairs to list of
        possibile following words.
        """
        if self._links is None:
            self._build()
        return self._links

    @property
    def form(self):
        if self._form is None:
            self._build()
        return self._form

    def nextword(self, wordpair=None):
        """
        Returns a randomly chosen word following a given pair.

        It is possible that the only possibilyt for the pair is to end
        a sentence, in which case None is returned.
        """
        if wordpair is None:
            wordpair = (None, None)
        if not wordpair in self.links:
            return None
        choices = list(self.links[wordpair])
        if len(choices) == 1:
            return choices[0]
        ret = None
        while ret is None:
            ret = random.choice(choices)
        return ret

    def formatword(self, word):
        """
        Returns the formatted form of the word, i.e. how it originally
        appeared in the source; the input word is in normalized form as
        contained in links.
        """
        if word is None:
            return word
        return self.form[word] if word in self.form else word

    def canend(self, wordpair):
        """
        Test whether the wordpair can end a sentence.
        """
        if not wordpair in self.links:
            return True
        return None in self.links[wordpair]

    def words(self, min=5, max=50, strict=False):
        """
        Yields a sequence of words between min and max words long by
        repeatedly calling nextword.

        When max is hit, the sequence will end even if canend says the
        current pair cannot end a sentence; this can be mitigated by
        setting struct to True, in which case a SentenceOverrun
        exception is raised.
        """
        buf = [None, None]
        pair = tuple(buf)
        count = 0
        while count < min or not self.canend(pair):
            if count > max:
                if strict:
                    raise SentenceOverrun
                else:
                    break
            next = self.nextword(pair)
            if next is None:
                if count < min and strict:
                    raise SentenceOverrun
                else:
                    break
            yield next
            buf.append(next)
            buf.pop(0)
            pair = tuple(buf)
            count += 1

    def sentence(self, min=5, max=50):
        """
        Returns a sentence between min and max words long, the sentence
        will end in a valid-ending word pair.
        """
        while True:
            try:
                words = self.words(min, max, strict=True)
                return ' '.join(words).capitalize()+'.'
            except SentenceOverrun:
                pass

# vim:set ts=4 sw=4 expandtab:
