# By Chengyuan Sha
# Reference: 3,000,000 Queens in less than one minute | ACM SIGART Bulletin. (1991)

import os
import os.path
import time
import numpy as np

# Strategy: The position for a new queen to be placed on the board is randomly generated from columns that
# are not occupied until a conflict free place is found for this queen.  After a certain number
# of queens have been placed in a conflict free manner the remaining queens are placed randomly on
# free columns regardless of conflicts on diagonal lines.
def initialization(n, m): # n is number of queens, m is number of queens without conflicts
    # queen = np.arange(n) # Initial order of queens, looks like python list is faster
    queen = list(range(n))
    row = np.zeros(2*n)
    col = np.zeros(2*n)
    diag_p = np.zeros(2*n, dtype=bool) # track diagonal lines negative slope
    diag_n = np.zeros(2*n, dtype=bool) # track diagonal lines positive slope
    queen, row, col, diag_p, diag_n = generate_conflict_free(queen, row, col, diag_p, diag_n, n, m)
    queen, row, col = generate_regardless_conflicts(queen, row, col, n, m)
    return queen, row, col

def generate_regardless_conflicts(queen, row, col, n, m):
    i = m
    last = n - m
    while i < n:
        ran_int = i + np.random.randint(0, last)
        queen[i], queen[ran_int] = queen[ran_int], queen[i]
        row[i-queen[i]+n-1] += 1
        col[i+queen[i]] += 1
        i += 1
        last -= 1
    return queen, row, col


def generate_conflict_free(queen, row, col, diag_p, diag_n, n, m):
    i = 0
    last = n
    while i < m:
        while True:
            ran_int = i + np.random.randint(0, last) # an random integer
            if not(diag_p[i-queen[ran_int]+n-1] or diag_n[i+queen[ran_int]]):
                break
        queen[i], queen[ran_int] = queen[ran_int], queen[i]
        row[i-queen[i]+n-1] += 1
        col[i+queen[i]] += 1
        diag_p[i-queen[i]+n-1] = True
        diag_n[i+queen[i]] = True
        i += 1
        last -= 1
    return queen, row, col, diag_p, diag_n

# Sum of number of conflicts
def conflict_sum(n, row, col):
    ans = 0
    for i in range(2*n):
        if row[i] > 1:
            ans += row[i] * (row[i]-1)/2
        if col[i] > 1:
            ans += col[i] * (col[i]-1)/2
    return ans

# The number of queens are placed randomly on free columns regardless of conflicts on diagonal lines.
def with_conflict(num, const_list):
    if num <= 10:
        if num > 8:
            return const_list[0]
        else:
            return num # Too small to change
    elif num < 100:
        return num
    elif num < 1000:
        return const_list[1]
    elif num < 10000:
        return const_list[2]
    elif num < 100000:
        return const_list[3]
    else:
        return const_list[4]

# delta to minimize conflict
def delta(i, j, row, col, queen, n): 
    ans = 0
    ans += (1 - row[i-queen[i]+n-1]) + (1 - col[i+queen[i]] ) + (1 - row[j-queen[j]+n-1]) + (1 - col[j+queen[j]])
    ans += (row[j-queen[i]+n-1]) + (col[j+queen[i]]) + (row[i-queen[j]+n-1]) + (col[i+queen[j]])
    if (i+queen[i]==j+queen[j]) or (i-queen[i]==j-queen[j]): # in the same diagonal
        ans += 2
    return ans

def update_values(row, col, queen, i, j, n):
    row[i - queen[i] + n - 1] -= 1  # Update values
    col[i + queen[i]] -= 1
    row[j - queen[j] + n - 1] -= 1
    col[j + queen[j]] -= 1
    queen[i], queen[j] = queen[j], queen[i]
    row[i - queen[i] + n - 1] += 1
    col[i + queen[i]] += 1
    row[j - queen[j] + n - 1] += 1
    col[j + queen[j]] += 1
    return row, col, queen

# n is the number of queens, m is the number of queens without conflicts
def min_conflict(n, m):
    queen, row, col = initialization(n, m)
    c_sum = conflict_sum(n, row, col) # sum of conflicts
    reset = 0
    step = 0
    start = time.perf_counter()
    while c_sum > 0:
        conflict = 0
        for i in range(m, n):
            if row[i-queen[i]+n-1]==1 and col[i+queen[i]]==1:
                if time.perf_counter()-start > 4: # Restart when > 4
                    reset += 1
                    queen, row, col = initialization(n, m)
                    c_sum = conflict_sum(n, row, col)
                    step = 0
                    start = time.perf_counter()
                continue
            else:
                for j in range(n): # Continue to check
                    if i != j:
                        conflict = delta(i, j, row, col, queen, n)
                        if conflict < 0:
                            break
                    if conflict < 0:
                        break
            if conflict < 0: # When there is solution
                step += 1
                row, col, queen = update_values(row, col, queen, i, j, n)
                c_sum += conflict
            else: # cannot handle conflicts
                reset += 1
                queen, row, col = initialization(n, m)
                c_sum = conflict_sum(n, row, col)
                step = 0
    print("Number of reset: ", reset)
    return queen, step

# Display in a chess board, 1 means queen
# used in debug purpose 
def visualize(sz, queen_loc):
    print("Show in a chess board: ")
    row = 0
    board = np.zeros((sz, sz), dtype=int)
    for i in queen_loc:
        board[row][i] = 1
        row += 1
    for i in range(sz):
        for j in range(sz):
            print(board[i][j], end=" ")
        print()

# read input and error checking
def read_txt(fname):
    with open(fname, "r") as f:
        num = f.read().split('\n')
    num = [s.strip() for s in num]
    num = [int(s) for s in num if s.isdigit()] # delete any possible non-digit character
    if not (False in list(map(lambda x: x > 3 and x <= 10000000, num))):
        return num
    else:
        raise ValueError("Each line of input should consist of a single integer value, n, where n > 3 and n <= 10,000,000")

# Write outputs
def write_output(solution, fname):
    print("Writing to txt...")
    with open(fname, "a") as f:
        f.write(str(solution)+"\n")
    print("Writing complete.")

# Assume `nqueens.txt` is in the same folder 
# The `nqueens_out.txt` file is generated as ans
def main():
    input_fname = "nqueens.txt"
    if os.path.isfile("nqueens_out.txt"):
        os.remove("nqueens_out.txt")
    num_of_queens = read_txt(input_fname)
    for n in num_of_queens:
        m = n - with_conflict(n, [ 8, 30, 50, 80, 100]) # m is the number of queens placed in a conflict free manner
        start = time.perf_counter()
        print("Number of queens: %d" % n)
        queen, step = min_conflict(n, m)
        end = time.perf_counter()
        print("Time elapsed (in seconds): %f" % (end-start))
        print("Steps in calculation: %d" % step)
        # visualize(n, queen)
        write_output(list(map(lambda x: x+1, queen)), "nqueens_out.txt") # +1 because require 1 based solution
        print("---------------------------------")

if __name__ == "__main__":
    main()
