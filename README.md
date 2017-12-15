# HMM_preparation

You are required to do your assignment of dynamic programming within this repository, and your
last commit before the deadline will be counted for grading unless you notify us of your late
submission. (Notice: you could keep pushing your code after the deadline)

## Requirements of the repository

**Please don't modify the existing files or relocate the directories.**

`/input` is a directory containing emission and transmission prior probability
matrix files, as well as two sequences files: one with a single sequence, the other with 200.
You also need to place the extra input files (e.g., from Question 4) into this directory. 

`MainProgram.py` is the main script that calls functions from the others, and you need to run it to get the results of your implemented algorithms. In this script, you need to get familiar with the parameters and understand how
this script works. You could change it, but please make sure the behaviours of this script stay the same (or else it will affect automated grading).

`BaumWelch.py` is the script where you have to insert your HMM code, the locations of which have been
indicated. However, you might have to make some coding
outside them to allow more than one iteration for training, once you move from question 3
 to question 4.
 
`Other scripts`: Please feel free to explore what the functions in the other Python
scripts do, but they are needed for the smooth work of this assignment, including
the automated grading. So please do not modify them, especially those functions
writing matrices to files. 

`student.id` is a text file to store your personal information to help us identify 
whose repository belongs to whom. In this file, you have found the student information
 of Cico Zhang, and you are required to change it to yours. 
 **The first line is your full name; second line, student ID; third line, VUnet ID.**

## Requirements of the script `MainProgram.py`

### Run this script

Usage: ` python3 MainProgram.py [-h] [-v] [-f] [-b] [-w] [-c] -am
                      transmission_matrix_file -em emission_matrix_file -s
                      sequence_file`

Please guarantee that the usage is maintained no matter how you customise the scripts. 

|optional arguments| explanation|
|:---------:|:----------:|
|`-h` or `--help`|             to show this help message and exit|
|`-v`|                    to run the Viterbi algorithm|
|`-f`|                    to run the Forward algorithm|
|`-b`|                    to run the Backward algorithm|
|`-w`|                    to run the Baum-Welch algorithm|
|`-c`|                    to reach convergence, leave empty (i.e., leave it out) for doing only one iteration|
|`-am`| to specify the transmission matrix file (required)|
|`-em`| to specify the emission matrix file (required)|
|`-s`|   to specify the sequence file (required)|

Command `-c` must be used when you need to train the algorithm. In this case, it is stored as True, and it is passed into function `baumWelch(setX, conv)` in `BaumWelch.py` as `conv`. It is your responsibility to use it correctly within the 
function to choose between one iteration or training. 

Example of correct input:
> python MainProgram.py -w -c -am input/TransPriorA1.txt -em input/EmissionPriorE1.txt -s input/sequences.txt


## The output format
TThis skeleton program ensures that the new matrices (Python dictionaries) are
outputted in `/output`, a directory created the first time `MainProgram.py` runs.
Matrices are written into tab-delimited files, the same way matrices in the input files
are formatted. Just do not modify the functions writing matrices to files and you will not
need to worry about the output format.

Some output derived from the matrices shows on screen, which is
not needed for automated grading, but you might have to include it in the report if the
question requires it. 
