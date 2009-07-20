#!/usr/bin/python

import markov
import random

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
            sentence = self.corpus.sentence(
                min=self.sentenceSize[0],
                max=self.sentenceSize[1]
            )
            for word in sentence.split():
                yield word

    def formattedLines(self, words):
        buf = []
        for word in words:
            buf.append(word)
            line = ' '.join(buf)
            if len(line) > self.lineLength:
                yield ' '.join(buf[:-1])
                buf = buf[-1:]
        if len(buf):
            yield ' '.join(buf)

    def passage(self, paragraphs, formatted=True):
        buf = ''
        for i in xrange(paragraphs):
            if formatted:
                for line in self.formattedLines(self.sens()):
                    buf += line+"\n"
                buf += "\n"
            else:
                buf += ' '.join(self.sens())+"\n\n"
        return buf.strip()

w = wisdom('wisdom.txt')
print w.passage(random.randint(3, 6))

# vim:set expandtab ts=4 sw=4:
