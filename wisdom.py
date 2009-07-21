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

class wisdom(markov.Corpus):
    def passage(self,
        size         = (3, 6),
        verseSize    = (1, 4),
        sentenceSize = (5, 20),
        wrap         = 40
    ):
        def verse(size, senSize):
            if type(size) is tuple:
                size = random.randint(*size)
            for i in xrange(size):
                yield self.sentence(
                    min=senSize[0],
                    max=senSize[1]
                )

        if type(size) is tuple:
            size = random.randint(*size)
        for i in xrange(size):
            lines = verse(verseSize, sentenceSize)
            if wrap > 0:
                lines = wordwrap(lines, wrap)
            for line in lines:
                yield line
            if i is not size-1:
                yield ''

if __name__ == '__main__':
    w = wisdom('wisdom.txt')
    for line in w.passage():
        print line

# vim:set expandtab ts=4 sw=4:
