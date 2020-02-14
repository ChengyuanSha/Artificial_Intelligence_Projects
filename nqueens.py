# By Chengyuan Sha
# Reference: 3,000,000 Queens in less than one minute | ACM SIGART Bulletin. (1991)

import os
import os.path
import time
import numpy as np

# The number of queens are placed randomly on free columns regardless of conflicts on diagonal lines.
def conflict(num):
    if num <= 10: # Pre-set to increase the efficiency
        return 8 if num > 8 else num # Too small to change
    elif num < 100:
        return num
    elif num < 1000:
        return 30
    elif num < 10000:
        return 50
    elif num < 100000:
        return 80
    else:
        return 100

# Strategy: The position for a new queen to be placed on the board is randomly generated from columns that
# are not occupied until a conflict free place is found for this queen.  After a certain number
# of queens have been placed in a conflict free manner the remaining queens are placed randomly on
# free columns regardless of conflicts on diagonal lines.
def initialization(n, m): # n is number of queens, m is number of queens without conflicts
    # queen = np.arange(n) # Initial order of queens, looks like python list is faster
    queen = list(range(n))
    row = np.zeros(2*n)
    d = np.zeros(2*n) # maintain the conflicts on the diagonal lines
    col = np.zeros(2*n)
    dd = np.zeros(2*n) # maintain the conflicts on the diagonal lines
    i = 0
    last = n
    while i < m:
        while True:
            ran_int = i + np.random.randint(0, last) # an random integer
            if not(d[i-queen[ran_int]+n-1] or dd[i+queen[ran_int]]):
                break
        queen[i], queen[ran_int] = queen[ran_int], queen[i]
        row[i-queen[i]+n-1] += 1
        col[i+queen[i]] += 1
        d[i-queen[i]+n-1] = 1
        dd[i+queen[i]] = 1
        i += 1
        last -= 1
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

# n is number of queens, row and col are the maintaining lists
def conflict_sum(n, row, col): # Get sum of number of conflicts from row and col
    result = 0
    for i in range(2*n):
        if row[i] > 1:
            result += row[i] * (row[i]-1)/2
        if col[i] > 1:
            result += col[i] * (col[i]-1)/2
    return result

# i, j are counters based on m, n respectively, row and col are the maintaining lists
# queen is the list for queens' arrangement, n is the number of queens
def conflict_change(i, j, row, col, queen, n): # change of conflicts
    result = 0
    result += 1 - row[i-queen[i]+n-1] # The following are calculating the status based on row and col
    result += 1 - col[i+queen[i]] # Accumulate conflicts
    result += 1 - row[j-queen[j]+n-1]
    result += 1 - col[j+queen[j]]

    result += row[j-queen[i]+n-1]
    result += col[j+queen[i]]
    result += row[i-queen[j]+n-1]
    result += col[i+queen[j]]

    if i+queen[i]==j+queen[j] or i-queen[i]==j-queen[j]: # Check for conflict
        result += 2
    return result

# n is the number of queens, m is the number of queens without conflicts
def min_conflict(n, m):
    queen, row, col = initialization(n, m) # Get the initial queens' arrangement
    t = conflict_sum(n, row, col) # Get sum of number of conflicts from row and col
    reset = 0
    reset_timeout = 0
    step = 0 # The step used in calculation
    start = time.perf_counter()
    while t > 0:
        conflict = 0 #Store value of changing of conflicts
        for i in range(m, n):
            if row[i-queen[i]+n-1]==1 and col[i+queen[i]]==1: 
                if time.perf_counter()-start > 3: # # Restart when takes too long 
                    reset_timeout += 1
                    queen, row, col = initialization(n, m)
                    t = conflict_sum(n, row, col)
                    step = 0
                    start = time.perf_counter()
                continue
            else:
                for j in range(n): # Continue to check
                    if i != j:
                        conflict = conflict_change(i, j, row, col, queen, n)
                        if conflict < 0:
                            break
                    if conflict < 0:
                        break
            if conflict < 0: # When there is solution
                step += 1
                row[i-queen[i]+n-1] -= 1 # Update values
                col[i+queen[i]] -= 1
                row[j-queen[j]+n-1] -= 1
                col[j+queen[j]] -= 1
                queen[i], queen[j] = queen[j], queen[i] # Swap position
                row[i-queen[i]+n-1] += 1
                col[i+queen[i]] += 1
                row[j-queen[j]+n-1] += 1
                col[j+queen[j]] += 1
                t += conflict
            else: # Restart when cannot handle conflicts
                reset += 1
                queen, row, col = initialization(n, m)
                t = conflict_sum(n, row, col)
                step = 0
    print("The numbers of reset (dead end): ", reset)
    print("The numbers of reset (timeout): ", reset_timeout)
    return queen, step

# show in a chess board, 1 mean queen
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
def write_output(queens, fname):
    # queens is the solution list
    print("Saving file...")
    with open(fname, "a") as f:
        f.write(str(queens)+"\n")
    print("Saving complete.")

# Assume `nqueens.txt` is in the same folder 
# The `nqueens_out.txt` file is generated as result
def main():
    input_fname = "nqueens.txt"
    if os.path.isfile(input_fname):
        os.remove("nqueens_out.txt")
    num_of_queens = read_txt(input_fname)
    for n in num_of_queens:
        m = n - conflict(n) # The number of queens placed in a conflict free manner
        start = time.perf_counter()
        print("Number of queens: %d" % n)
        queen, step = min_conflict(n, m)
        end = time.perf_counter()
        print("Time elapsed (in seconds): %f" % (end-start))
        print("Steps in calculation: %d" % step)
        # visualize(n, queen)
        write_output(list(map(lambda x: x+1, queen)), "nqueens_out.txt") # +1 because require 1 based solution
        print("")

if __name__ == "__main__":
    main()
