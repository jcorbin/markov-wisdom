import re

class Parse(object):
    _sentenceReCache = {}

    @classmethod
    def sentences(cls, iterable, endPunc=r"\.;"):
        """
        Iterates sentences in a source
        """
        if not endPunc in cls._sentenceReCache:
            cls._sentenceReCache[endPunc] = re.compile(
                r"(.+)["+endPunc+r"]\s*(.*)"
            )
        sen = cls._sentenceReCache[endPunc]

        buf = []
        for chunk in iterable:
            chunk = chunk.strip()
            while len(chunk):
                m = sen.match(chunk)
                if m:
                    (frag, rest) = m.groups()
                    if len(buf):
                        buf.append(frag)
                        yield ' '.join(buf)
                        buf = []
                    else:
                        yield frag
                    chunk = rest
                else:
                    buf.append(chunk)
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


# vim:set ts=4 sw=4 expandtab:
