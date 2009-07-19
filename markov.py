import re

def sentences(iterable, endPunc=r"\.;"):
    "Iterates sentences in a source"
    if not endPunc in sentences._reCache:
        sentences._reCache[endPunc] = re.compile(r"(.+)["+endPunc+r"]\s*(.*)")
    sen = sentences._reCache[endPunc]

    buf = []
    for line in iterable:
        line = line.strip()
        while len(line):
            m = sen.match(line)
            if m:
                (frag, rest) = m.groups()
                if len(buf):
                    buf.append(frag)
                    yield ' '.join(buf)
                    buf = []
                else:
                    yield frag
                line = rest
            else:
                buf.append(line)
                line = ''

sentences._reCache = {}

def phrases(sentence, wordChar=r"[\w\-']", size=3, trailing=(None, None)):
    """
    Iterates phrases in a sentence

    Arguments
        wordChar: the character class to use in finding words
        size: how many words long should each phrase be
        trailing: how many words to yield with None padding elements at
            either end of the sentence; for example:
                >>> s = 'alpha bravo charlie delta'
                >>> pprint(list(phrases(s, size=3, trailing=(1, 1))))
                [(None, None, 'alpha'),
                 (None, 'alpha', 'bravo'),
                 ('alpha', 'bravo', 'charlie'),
                 ('bravo', 'charlie', 'delta'),
                 ('charlie', 'delta', None),
                 ('delta', None, None)]
                >>> pprint(list(phrases(s, size=3, trailing=(None, 2))))
                [('alpha', 'bravo', 'charlie'),
                 ('bravo', 'charlie', 'delta'),
                 ('charlie', 'delta', None)]
    """
    if not wordChar in phrases._reCache:
        phrases._reCache[wordChar] = re.compile(r"\b("+wordChar+r"+)\b")
    wordRe = phrases._reCache[wordChar]

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

phrases._reCache = {}

# vim:set ts=4 sw=4 expandtab:
