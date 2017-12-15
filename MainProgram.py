#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The main program of HMM.

This script serves as the main program to implement HMM by calling other
modules.
"""

import BaumWelch
import Viterbi
import AEMatrices
import Sequences
import argparse
import sys
import os


def viterbiAlgorithm(seq, a, e):
	"""Run the Viterbi algorithm and saves the Viterbi Matrix and the Back Trace Matrix in an output folder.
	"""
	# Read the A and E matrices
	AEMatrices.init(e, a)

	# Read the input sequence(s) and store them into setX
	setX = Sequences.readSeq(seq, "X")

	# Perform the Viterbi algorithm on the first sequence of the set setX
	# and store the viterbi matrix in the variable vi and the back trace matrix in variable backTrace
	(vi, backTrace, probability) = Viterbi.viterbi(setX[0])

	# Print the output matrices of Viterbi algorithm
	Viterbi.writePathMatrix(vi, setX[0], "output/ViterbiMatrix.txt")
	Viterbi.writePathMatrix(backTrace, setX[0], "output/BackTraceMatrix.txt")

	# Print the most likely sequence path of x according to the viterbi algorithm
	print('Most likely state is {0}, with probability of {1}'.format(''.join(Viterbi.generateStateSeq
	                                                                         (backTrace, setX[0])), probability))

def viterbiTraining(seq, a, e):
	'''Run the Viterbi training and save new matrices in an output folder.
	'''
	# Read the A and E matrices
	AEMatrices.init(e, a)

	# Read the input sequences and store them into seqX.
	seqX = Sequences.readSeq(seq, "X")

	# Do Viterbi training using a training set of sequences.
	newA, newE, iteration = Viterbi.viterbi_training(seqX)
	# print new matrices in files.
	AEMatrices.writeEMatrix(newE, 'output/newE.txt')
	AEMatrices.writeAMatrix(newA, 'output/newA.txt')
	# print the iteration number
	print(iteration)


def forwardAlgorithm(seq, a, e):
	"""Prints the forward probability for a given sequence"""
	# Read the A and E matrices
	AEMatrices.init(e, a)

	# Read the input sequence(s) and store them into setX
	setX = Sequences.readSeq(seq, "X")

	# Obtain the forward matrix
	f = BaumWelch.forward(setX[0], len(setX[0]) - 2)
	AEMatrices.writeForwardMatrix(f, 'output/forward_matrix.txt')
	print('\nForward probability for sequence {0}:\n{1}'.format(''.join(setX[0]).strip(),
	                                                            BaumWelch.getProbabilityForwardX(f, len(setX[0]) - 2)))


def backwardAlgorithm(seq, a, e):
	"""Prints the backward probability for a given sequence"""
	# Read the A and E matrices
	AEMatrices.init(e, a)

	# Read the input sequence(s) and store them into setX
	setX = Sequences.readSeq(seq, "X")

	# Obtain the backward matrix
	b = BaumWelch.backward(setX[0], len(setX[0]) - 2)
	AEMatrices.writeBackwardMatrix(b, 'output/backward_matrix.txt')
	print('\nBackward probability for sequence {0}:\n{1}'.format(''.join(setX[0]).strip(), b['B'][0]))


def baum_welchAlgorithm(seq, a, e, convergence):
	"""Performe the Baum Welch algorithm. If convergence is true, then it should perform the training (for you to code)"""
	# Read the A and E matrices
	AEMatrices.init(e, a)

	# Read the input sequence(s) and store them into setX
	setX = Sequences.readSeq(seq, "X")

	newA, newE, iteration, delta_sumLL = BaumWelch.baumWelch(setX, convergence)
	# print new matrices in files.
	AEMatrices.writeEMatrix(newE, 'output/newE.txt')
	AEMatrices.writeAMatrix(newA, 'output/newA.txt')
	print(iteration, delta_sumLL)





def parser():
	"""Retrieves the arguments from the command line.
	"""

	parser = argparse.ArgumentParser(description='A program to run HMM algorithms.')

	parser.add_argument('-v', dest='viterbi', action='store_true', help='[-v] to run the Viterbi algorithm')
	parser.add_argument('-f', dest='forward', action='store_true', help='[-f] to run the Forward algorithm')
	parser.add_argument('-b', dest='backward', action='store_true', help='[-b] to run the Backward algorithm')
	parser.add_argument('-w', dest='baum_welch', action='store_true', help='[-w] to run the Baum-Welch algorithm')
	parser.add_argument('-c', dest='convergence', action='store_true',
						help='[-c] to reach convergence, leave empty for doing only 1 iteration', default=False)
	parser.add_argument('-am', required=True, metavar='transmission_matrix_file', dest='transitionMatrix',
						help='[-am] to select transmission matrix file')
	parser.add_argument('-em', required=True, metavar='emission_matrix_file', dest='emissionMatrix',
						help='[-em] to select emission matrixfile ')
	parser.add_argument('-s', required=True, metavar='sequence_file', dest='sequence',
						help='[-s] to select sequence file')
	parser.add_argument('-t', dest='viterbiTraining', action='store_true', help='[-t] to run the viterbi training')


	arguments = parser.parse_args()  # takes the arguments

	if arguments.viterbi == True:  # Do the Viterbi algorithm
		algorithm = 'viterbi'
	elif arguments.forward == True:  # Do the forward_backward algorithm
		algorithm = 'forward'
	elif arguments.backward == True:  # Do the forward_backward algorithm
		algorithm = 'backward'
	elif arguments.baum_welch == True:  # Do the Baum-Welch algorithm
		algorithm = 'baum_welch'
	elif arguments.viterbiTraining == True: # Do the Viterbi training
		algorithm = 'viterbiTraining'

	# Kept here just in case
	else:
		print('This shouldn\'t happen')
		sys.exit()

	return [algorithm, arguments]


def main():
	"""Main function. This function checks the chosen arguments and files and calls the right function.
	"""
	if not os.path.exists('output'):
		os.makedirs('output')

	cmd = parser()
	args = cmd[1]

	input_sequence = args.sequence
	a_matrix = args.transitionMatrix
	e_matrix = args.emissionMatrix

	algorithm = cmd[0]
	if algorithm == 'viterbi':
		viterbiAlgorithm(input_sequence, a_matrix, e_matrix)
	elif algorithm == 'forward':
		forwardAlgorithm(input_sequence, a_matrix, e_matrix)
	elif algorithm == 'backward':
		backwardAlgorithm(input_sequence, a_matrix, e_matrix)
	elif algorithm == 'baum_welch':
		baum_welchAlgorithm(input_sequence, a_matrix, e_matrix, args.convergence)
	elif algorithm == 'viterbiTraining':
		viterbiTraining(input_sequence, a_matrix, e_matrix)

if __name__ == "__main__":
	main()

print('\n"A hidden connection is stronger than an obvious one."\n-Heraclitus of Ephesus\n')
