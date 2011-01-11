#!/usr/bin/python

import sys
import itertools

def iwords(stream):
    for line in stream:
        for word in line.split():
            yield word

def best_words(words):
    result = None
    min_start = None

    for i, word in enumerate(words):
        if min_start is None or word[0] < min_start:
            result = []
            min_start = word[0]

        if word[0] == min_start:
            result.append((word, i))

    return min_start, result

def studiousstudent(words):
    if not words:
        return ''

    ch, best = best_words(words)

    best_result = None

    for word, i in best:
        new_words = words[:]
        del new_words[i]
        word_result = word + studiousstudent(new_words)
        if best_result is None or word_result < best_result:
            best_result = word_result
    
    return best_result

def main(argv):
    for filename in argv[1:]:
        with open(filename) as f:
            words = iwords(f)
            n_lists = int(words.next())
            for _ in xrange(n_lists):
                n_words = int(words.next())
                word_list = list(itertools.islice(words, n_words))

                print studiousstudent(word_list)

if __name__ == '__main__':
    main(sys.argv)
