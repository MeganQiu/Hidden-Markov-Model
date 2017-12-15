#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""The module for Viterbi algorithm.

This script serves as the module that implements Viterbi algorithm.
This module will be called in the 'MainProgram.py'; before that, you need to
complete it.
"""

import AEMatrices
from AEMatrices import A, E, allStates, emittingStates, emissionSymbols
from BaumWelch import forward, getProbabilityForwardX
import math
from collections import Counter


# viterbi algorithm takes a sequence X as input
# It uses  A, E, allStates, emittingStates, emissionSymbols from AEMatrices
# Output: vi matrix and backtrace matrix (as a tuple),
# and the probability of most likely state sequence
# usage example: (vi,backtrace, probability) = viterbi(sequence)
# note: vi[k][i], viterbi of state k, at sequence position i
# note: that we count from 0,1,2...,L,L+1
# where 0 indicates the begin state and L+1 the end state
def viterbi(X):
    # initialise vi to '0' and backTrace to ""
    L = len(X)-2
    vi = dict()
    backTrace = dict()
    for k in AEMatrices.allStates:
        vi[k] = [0]*(L+2)
        backTrace[k] = ["-"]*(L+2)
    # initialise begin state
    vi['B'][0] = 1
    backTrace['B'][0] = "*"
    # iterate over sequence
    for i in range(1, L+1):
        for l in AEMatrices.emittingStates:
            # find maximum of vi[k][i-1]*A[k][l]
            maximum = 0
            statePointer = -1
            for k in AEMatrices.allStates:
                result = vi[k][i-1]*A[k][l]
                if(result > maximum):
                    maximum = result
                    statePointer = k
            vi[l][i] = maximum * E[l][X[i]]
            backTrace[l][i] = statePointer
    # calculate vi for End state at position L-1
    maximum = 0
    statePointer = -1
    for l in AEMatrices.emittingStates:
        result = vi[l][L]*A[l]['E']
        if(result > maximum):
            maximum = result
            statePointer = l
    vi['E'][L+1] = maximum
    backTrace['E'][L+1] = statePointer
    return (vi, backTrace, vi['E'][L+1])


# should be done tab separated, and with only 3 significant numbers
def writePathMatrix(M, X, filename):
    f = open(filename, "w")

    to_print = ['']
    for n in range(0, len(X)):
        to_print.append(str(n))
    print('\t'.join(to_print), file=f)
    to_print = ['']

    for i in X:
        if i == " ":
            to_print.append('-')
        else:
            to_print.append(str(i))
    print('\t'.join(to_print), file=f)

    for state in ['B', 'D', 'L', 'E']:
    # for state in allStates:
        to_print = []
        to_print.append(state)
        for i in range(0, len(X)):
            to_print.append(str(M[state][i]))
        print('\t'.join(to_print), file=f)

    print("written ", filename)


# Generate the most likely state sequence given according to the output of
# viterbi algorithm.
def generateStateSeq(backTrace, x):
    L = len(x)-2
    pi = [""]*(L+2)
    pi[L+1] = "E"
    pi[L] = backTrace["E"][L+1]
    for i in range(L, 0, -1):
        pi[i-1] = backTrace[pi[i]][i]
    # return the state sequence
    return pi


def viterbi_training(setX):
    # do iterations and the maximal iteration is the length of training set.
    iteration = 0
    pre_sumLL = 0.0

    while iteration <= len(setX):
        # Initialise some useful list
        state_paths = []
        transition = []
        emission = []
        # Initialise the sum of probabilities.
        sumLL = 0.0

        for X in setX:
            # get sum of log likelihood to judge convergence
            L = len(X) - 2
            f = forward(X, L)
            for_prob = getProbabilityForwardX(f, L)
            sumLL += math.log(for_prob)

            # get optimal path by Viterbi algorithm
            vi, backTrace, vi['E'][L + 1] = viterbi(X)
            state_path = generateStateSeq(backTrace, X)
            state_paths += state_path# store the path

            # store the transition from state i to j.
            transition += zip(state_path[:-1], state_path[1:])
            # store the emission symbols with the state.
            emission += zip(state_path[1:-1], X[:])

        # count the frequencies of aij, ai and ekb.
        count_state = Counter(state_paths)
        count_symbol = Counter(emission)
        count_transition = Counter(transition)

        # calculate new emission matrix
        newE = dict()
        for k in emittingStates:
            # initalise new emission matrix newE
            newE[k] = dict()
            for s in emissionSymbols:
                    if count_state[k] == 0:
                        newE[k][s] = 0
                    else:
                        newE[k][s] = count_symbol[(k, s)] / count_state[k]

        # calculate new transition matrix
        newA = dict()
        for k in allStates:
            # initialise new transition matrix newA
            newA[k] = dict()
            for l in allStates:
                if count_state[k] == 0:
                    newA[k][l] = 0
                else:
                    newA[k][l] = count_transition[(k, l)] / count_state[k]

        # update the matrix to continue iteration.
        A = AEMatrices.setNewA(newA)
        E = AEMatrices.setNewE(newE)

        ratio_of_change = math.fabs(sumLL - pre_sumLL) / math.fabs(sumLL)
        pre_sumLL = sumLL

        # determine whether the result converges or not.
        if ratio_of_change <= 0.0001:
            break
        else:
            iteration += 1

    return(A, E, iteration)


