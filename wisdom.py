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
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-l', '--length', dest='length', default='40',
        help='Line length to wrap to, zero for no wrapping'
    )
    parser.add_option('-w', '--words', dest='words',
        default='5,20', metavar='MIN,MAX',
        help='How many words per sentence.'
    )
    parser.add_option('-s', '--sentences', dest='sentences',
        default='1,4', metavar='MIN,MAX',
        help='How many sentences per verse.'
    )
    parser.add_option('-v', '--verses', dest='verses',
        default='3,6', metavar='MIN,MAX',
        help='How many verses per passage.'
    )
    (options, args) = parser.parse_args()

    try:
        options.length = int(options.length)
    except ValueError:
        parser.error('invalid length value')

    def rangeVal(name, val):
        val = val.split(',', 2) if ',' in val else [val]
        try:
            val = [int(s) for s in val]
        except ValueError:
            parser.error('invalid '+name+' value')
        if len(val) == 1:
            return val[0]
        else:
            return tuple(val)

    options.words = rangeVal('words', options.words)
    options.sentences = rangeVal('sentences', options.sentences)
    options.verses = rangeVal('verses', options.verses)

    if type(options.words) is not tuple:
        parser.error('invalid words value')

    w = wisdom('wisdom.txt')
    passage = w.passage(
        size         = options.verses,
        verseSize    = options.sentences,
        sentenceSize = options.words,
        wrap         = options.length
    )
    for line in passage:
        print line

# vim:set expandtab ts=4 sw=4:
