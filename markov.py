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

# vim:set ts=4 sw=4 expandtab:
