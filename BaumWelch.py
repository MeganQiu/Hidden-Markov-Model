#s!/usr/bin/python
# -*- coding: utf-8 -*-

import AEMatrices
from AEMatrices import A, E, allStates, emittingStates, emissionSymbols
import math

# Forward algorithm, takes a sequence X and the nr. of symbols in of the sequence (L) as inputs
# It uses  A, E, allStates, emittingStates, emissionSymbols from AEMatrices
# Output: forward matrix (in form of dictionary)
# usage example: f = forward(sequence, L)
# f[k][i], forward of state k, at sequence position i
# note that we count from 0,1,2...,L,L+1
# where 0 indicates the begin state and L+1 the end state
def forward(X, L):
	f = dict()

	# initialise f to '0'
	for k in allStates:
		f[k] = [0] * (L + 2)

	# initialise begin state
	f["B"][0] = 1

	# iterate over sequence
	for i in range(1, L + 1):

		for l in emittingStates:
			result = 0

			for k in allStates:
				result += A[k][l] * f[k][i - 1]

			f[l][i] = result * E[l][X[i]]
	# in emittingState
	# calculate f for End state at position L-1

	for k in emittingStates:
		f["E"][L + 1] += f[k][L] * A[k]["E"]
	# return forward matrix
	return f


# Backward algorithm, takes a sequence X and the nr. of symbols in of the sequence (L) as inputs
# It uses  A, E, allStates, emittingStates, emissionSymbols from AEMatrices
# Output: backward matrix (in form of dictionary)
# usage example: b = backward(sequence, L)
# b[k][i], backward of state k, at sequence position i
# note that we count from L+1,L,....,2,1,0  
# where 0 indicates the begin state and L+1 the end state

def backward(X, L):
	b= dict()
	# initialise b to '0'
	for k in allStates:
		b[k] = [0] * (L + 2)

	# initialise end state
	for k in allStates:
		b[k][L] = A[k]['E']

	# iterate over sequence
	for i in range(L - 1, -1, -1):

		for k in emittingStates:

			for l in allStates:
				b[k][i] += A[k][l] * E[k][X[i + 1]] * b[l][i + 1]

	# calculate probability
	for l in emittingStates:
		b["B"][0] += b[l][1] * A["B"][l]

	# return backward matrix
	return b

#Calculate the transition probability from state k to state l given the training sequence X and forward and backward matrix of this sequence.
#Output: Transition probability matrix (in form of dictionary)
def transitionP(f,b,X,L):
	aP=dict()

	# initialise aP
	for k in AEMatrices.allStates:
		aP[k] = dict()
		for l in allStates:
			aP[k][l]=0

	# iterate over sequence
	for k in AEMatrices.allStates:
		for l in AEMatrices.emittingStates:

			# calculate probability of transition k->l at position i
			z = 0
			for i in range(0,L):
				z += f[k][i]*A[k][l]*E[l][X[i+1]]*b[l][i+1]
			aP[k][l] = z

	# add transition to end state
	for k in AEMatrices.allStates:
		aP[k]['E'] = aP[k]['E'] + f[k][L]*A[k]['E']
	# print aP
	return aP

#Calculate the emission probability of symbol s from state k given the training sequence X and forward and backward matrix of this sequence.
#Output: Emission probability matrix (in form of dictionary)

def emissionP(f,b,X,L):
	eP=dict()
	# initialise tP
	for l in emittingStates:
		eP[l] = dict()
		for s in emissionSymbols:
			eP[l][s]=0

	# iterate over sequence
	for l in emittingStates:
		for s in emissionSymbols:
			z = 0
			for i in range(1,L+1):

			# calculate probability symbol s at state k
				if s == X[i]:
					z += f[l][i]*b[l][i]
			eP[l][s] = z
	return eP



# returns probability given the forward matrix
def getProbabilityForwardX(f,L):
	return (f['E'][L+1])

# Baum-Welch algorithm, takes a set of training sequences setX as input
# Output: the new A matrix, new E matrix and the total sum of the log likelyhood, all in a single list
# usage example: (newA, newE, sumLL) = baumWelch(setX)

def baumWelch(setX, conv):
	# initialise emission counts matrix
	# eC[k][s] is the expected number of counts for emission symbol s
	# at state k
	iteration = 1
	VARIATION = 0.0001
	# set previous sumLL to do iterations
	pre_sumLL = 0.0

	while iteration <= len(setX):

		eC = dict()
		for k in emittingStates:
			eC[k] = dict()
			for s in emissionSymbols:
				# you may want to add pseudo counts here
				eC[k][s] = 0

		# initials transition count matrix
		# aC[k][l] is the expected number of transitions from
		# state k to state l
		aC = dict()
		for k in allStates:
			aC[k] = dict()
			for l in allStates:
				# you may want to add pseudo counts here
				aC[k][l] = 0
		# sum over log likelihood
		sumLL = 0.0

		# iterate over training sequences
		for X in setX:
			L = len(X) - 2
			f = forward(X, L)
			b = backward(X, L)
			# probability P(x)
			prob = getProbabilityForwardX(f, L)
			# the emission probability of symbol s from state k given the training sequence X
			eP = emissionP(f, b, X, L)
			# add emission counts
			for k in emittingStates:

				for s in emissionSymbols:
					eC[k][s] += (1 / prob) * eP[k][s]

			# the transition probability from state k to state l given the training sequence X
			aP = transitionP(f, b, X, L)
			# add transition counts
			for k in allStates:

				for l in allStates:
					aC[k][l] += (1 / prob) * aP[k][l]


			# add sum over log likelihood
			sumLL += math.log(prob)

		# calculate new transitions
		# initialisie new transition matrix newA
		newA = dict()
		for k in allStates:
			newA[k] = dict()
			sum_l = 0

			for l in allStates:
				sum_l += aC[k][l]

			for l in allStates:
				if sum_l != 0:
					newA[k][l] = aC[k][l] / sum_l
				else:
					newA[k][l] = 0

		# calculate new emissions
		# initialise new emission matrix newE
		newE = dict()
		for k in emittingStates:
			newE[k] = dict()
			sum_s = 0

			for s in emissionSymbols:
				sum_s += eC[k][s]

			for s in emissionSymbols:
				if sum_s != 0:
					newE[k][s] = eC[k][s] / sum_s
				else:
					newE[k][s] = 0

		# update the A and E matrices
		A = AEMatrices.setNewA(newA)
		E = AEMatrices.setNewE(newE)

		# if there is only one training sequence, do one iteration.
		if len(setX) == 1:
			break

		# get sumLL differences
		delta_sumLL = math.fabs( pre_sumLL - sumLL ) / math.fabs( sumLL )
		# update previous sumLL
		pre_sumLL = sumLL

		# check if it converges.
		if delta_sumLL <= VARIATION:
			break
		else:
			# update iteration
			iteration += 1

	return (A, E, iteration, delta_sumLL)


# finish BaumWelch
