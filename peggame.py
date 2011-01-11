#!/usr/bin/python

import sys
import itertools

def iwords(stream):
    for line in stream:
        for word in line.split():
            yield word

def inumbers(stream):
    return (int(word) for word in iwords(stream))

def ipairs(numbers):
    while True:
        yield (numbers.next(), numbers.next())

def odd(n):
    return n % 2 != 0

def even(n):
    return not odd(n)

class Board(object):
    def __init__(self, n_rows, n_cols, holes, target_col):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.holes = set(holes)
        self.target_col = target_col

    def hole(self, row, col):
        return (row, col) in self.holes

    def right_edge(self, row, col):
        return even(row) and col == self.n_cols - 1 or \
                odd(row) and col == self.n_cols - 2

    def left_edge(self, row, col):
        return col == 0


    def prob_left(self, row, col):
        if self.hole(row, col):
            return 0.0

        if self.right_edge(row, col):
            return 1.0
        
        if self.left_edge(row, col):
            return 0.0

        return 0.5

    def prob_right(self, row, col):
        if self.hole(row, col):
            return 0.0

        if self.right_edge(row, col):
            return 0.0

        if self.left_edge(row, col):
            return 1.0

        return 0.5

    def prob_down(self, row, col):
        if self.hole(row, col):
            return 1.0

        return 0.0

    def col_left(self, row, col):
        if even(row):
            return col - 1
        else:
            return col

    def col_right(self, row, col):
        if even(row):
            return col
        else:
            return col + 1

    def prob_win(self, start_col):
        # skip first row
        row_probs = [0.0] * (self.n_cols - 1)
        row_probs[start_col] = 1.0

        next_probs = [0.0] * self.n_cols

        for row in xrange(1, self.n_rows):
#            import pdb; pdb.set_trace()
            next_next_probs = [0.0] * len(row_probs)
            for col, col_prob in enumerate(row_probs):
                if col_prob == 0.0:
                    continue

                prob_left = self.prob_left(row, col)

                if prob_left > 0.0:
                    col_left = self.col_left(row, col)
                    next_probs[col_left] += prob_left * col_prob

                prob_right = self.prob_right(row, col)

                if prob_right > 0.0:
                    col_right = self.col_right(row, col)
                    next_probs[col_right] += prob_right * col_prob

                prob_down = self.prob_down(row, col)
                if prob_down > 0.0:
                    col_down = col
                    next_next_probs[col_down] += prob_down * col_prob

            row_probs = next_probs
            next_probs = next_next_probs

        #print row_probs
        return row_probs[self.target_col]

    def __str__(self):
        result = []
        for row in xrange(self.n_rows):
            if even(row):
                cols = self.n_cols
                line = ''
            else:
                cols = self.n_cols - 1
                line = ' '

            line += '.'.join(
                [('x', '.')[self.hole(row, col)]
                 for col in xrange(cols)])

            result.append(line)

        result.append(' %sG' % ('  ' * self.target_col))

        return '\n'.join(result)
             

def peggame(n_rows, n_cols, target_col, holes):
    best_prob = 0.0
    best_start_col = None

    board = Board(n_rows, n_cols, holes, target_col)
    #print board

    for start_col in xrange(n_cols - 1):
        prob = board.prob_win(start_col)
        if prob > best_prob:
            best_prob = prob
            best_start_col = start_col

    return best_start_col, best_prob

    

    
    return n_rows, n_cols, target_col, holes

def main(argv):
    for filename in argv[1:]:
        with open(filename) as f:
            numbers = inumbers(f)
            pairs = ipairs(numbers)

            n_boards = numbers.next()

            for _ in xrange(n_boards):
                n_rows = numbers.next()
                n_cols = numbers.next()
                target_col = numbers.next()
                n_holes = numbers.next()
                holes = list(itertools.islice(pairs, n_holes))
                
                col, prob = peggame(n_rows, n_cols, target_col, holes)

                print "%d %8.6f" % (col, prob)
    
if __name__ == '__main__':
    main(sys.argv)

