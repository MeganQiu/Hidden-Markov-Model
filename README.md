# HMM_preparation

You are required to do your assignment of dynamic programming within this repository, and your
last commit before the deadline will be counted for grading unless you notify us of your late
submission. (Notice: you could keep pushing your code after the deadline)

## Requirements of the repository

**Please don't modify the existing files or relocate the directories.**

`/input` is a directory containing emission and transmission prior probability
matrix files, as well as two sequences files: one with a single sequence, the other with 200.

`MainProgram.py` is the main script that calls functions from the others.

## Requirements of the script `MainProgram.py`

### Run this script

Note: I use a maximal iterated number - the length of setX and a threshold of variation in the sum of log probabilities instead of [-c] argument.
Usage: ` python3 MainProgram.py [-h] [-v] [-f] [-b] [-w] -am
                      transmission_matrix_file -em emission_matrix_file -s
                      sequence_file`

