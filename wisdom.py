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
    paragraphSize = (2, 5)
    sentenceSize = (5, 20)

    lineLength = 40

    def __init__(self, source):
        self.corpus = markov.Corpus(source)

    def sens(self):
        count = random.randint(
            self.paragraphSize[0],
            self.paragraphSize[1]
        )
        for i in xrange(count):
            yield self.corpus.sentence(
                min=self.sentenceSize[0],
                max=self.sentenceSize[1]
            )

    def passage(self, paragraphs, formatted=True):
        buf = ''
        for i in xrange(paragraphs):
            if formatted:
                for line in wordwrap(self.sens(), self.lineLength):
                    buf += line+"\n"
                buf += "\n"
            else:
                for sen in self.sens():
                    buf += sen+"\n\n"
        return buf.strip()

w = wisdom('wisdom.txt')
print w.passage(random.randint(3, 6))

# vim:set expandtab ts=4 sw=4:
