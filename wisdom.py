#!/usr/bin/python

import markov
import random

def wordwrap(source, width=40, sep=' '):
    """
    Yields lines of no more than width length built from joining words
    from the source.

    Yielded lines do not have a trailing newline.
    """
    words = (word
        for chunk in source
        for word in chunk.strip().split()
    )

    buf = []
    for word in words:
        buf.append(word)
        line = sep.join(buf)
        if len(line) > width:
            yield sep.join(buf[:-1])
            buf = buf[-1:]
    if len(buf):
        yield sep.join(buf)

class wisdom(object):
    def __init__(self, source):
        self.corpus = markov.Corpus(source)

    def verse(self, size=(1, 4), sentenceSize=(5, 20)):
        count = random.randint(*size)
        for i in xrange(count):
            yield self.corpus.sentence(*sentenceSize)

    def passage(self, size=(3, 6), wrap=40):
        for i in xrange(random.randint(3, 6)):
            lines = self.verse()
            if wrap > 0:
                lines = wordwrap(lines, wrap)
            for line in lines:
                yield line
            yield ''

w = wisdom('wisdom.txt')
for line in w.passage():
    print line

# vim:set expandtab ts=4 sw=4:
