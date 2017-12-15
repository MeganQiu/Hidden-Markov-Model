import random
import AEMatrices
'''
This function is used to generate n sequences with random lengths for a given HMM
(predefined emission and transition matrices, named EmissionPriorE1 and TransPriorA1 respectively)
'''

# n is the number of sequences in this set.
# l is the length of each sequence.
def seqGenerator():
	# initialise n and iteration number.
	n = random.randint(1, 300)
	iteration = 1
	# initialise thesequence set.
	setX = []
	symbols = ['H', 'P', 'C']
	# generate sequences.
	while iteration <= n:
		# initialise the sequence length and sequence
		l = random.randint(1, 20)
		seq = ''

		i = 0
		while i < l:
			seq += random.choice(symbols)
			i += 1

		# add sequence to setX.
		setX.append(seq)
		#update iteration
		iteration += 1

	return setX

def writesetX(setX, filename):
	'''write the setX in a file with a head '>seq i' for each sequence'''
	f = open(filename, 'w')

	for index, seq in enumerate(setX):
		# add a header
		print('> seq %d' % index, file = f)
		print(seq, file = f)

	f.close()

	print('Sequence set has saved in file.')

setX = seqGenerator()
for i in setX:
	print(i)
writesetX(setX, 'setX.txt')
