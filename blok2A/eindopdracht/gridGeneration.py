
# import random
# from random import randint

# def pickNote(notes, position, spread):
# 	probabilityDistribution = []
# 	n = spread + 1

# 	k = 1
# 	while k <= n:											# Initializes a list of harmonically scaled probability with a specified length (spread)
# 		probabilityDistribution.append(round(k/(n*n), 4))	# For example, if the spread was 3 the generated probability list would look as follows:
# 		k += 1												# [1/(3)^2, 2/(3)^2, 3/(3)^2, 2/(3)^2, 1/(3)^2]
# 	k -= 2													# The general output with a spread of n would look like this:
# 	while k > 0:											# [1/n^2, 2/n^2, 3/n^2, ..., n-1/n^2, n/n^2, n-1/n^2, ..., 3/n^2, 2/n^2, 1/n^2]
# 		probabilityDistribution.append(round(k/(n*n), 4))
# 		k -= 1

# 	outOfBounds = 0
# 	if position - spread < 0:								# Checks if the probabilityDistribution exceeds the lower bound of the list of possible notelengths (index < 0).
# 		for i in range(0, spread - position):				# Loops through al the probabilities which exceed the lower bound.
# 			outOfBounds += probabilityDistribution.pop(0)	# Adds up all the probabilities which exceed the lower bound.

# 	if position + spread > len(notes) - 1:					# Checks if the probabilityDistribution exceeds the upper bound of the list of possible notelengths (index > len(notes)).
# 		for i in range(0, spread):							# Loops through al the probabilities which exceed the upper bound.
# 			outOfBounds += probabilityDistribution.pop(-1)	# Adds all the probabilities which exceed the upper bound to the probabilities that exceeded the lower bound.

# 	for i, probability in enumerate(probabilityDistribution):								# Distributes all the probabilities which were out of bound evenly to the remaining probabilities.
# 		probabilityDistribution[i] = probability + outOfBounds/len(probabilityDistribution)	# This ensures all the probabilities will add up to 100%.

# 	print(probabilityDistribution)

# 	noteProbabilities = [0]*len(notes)												# Initializes a list with the same length as the list of possible notelengths.
# 	for i in range(0, len(probabilityDistribution)):								# Pastes the probabilityDistribution on the correct position
# 		if position - spread >= 0:													# in relation to the notelenghts.
# 			noteProbabilities[i + position - spread] = probabilityDistribution[i]
# 		else:
# 			noteProbabilities[i] = probabilityDistribution[i]

# 	for i, chance in enumerate(noteProbabilities):								# Loops through the probabilities and stacks them.
# 		try:																	# For example: [0, 0.25, 0.5, 0.25, 0, 0, 0, 0] gets turned
# 			noteProbabilities[i] = round(chance + noteProbabilities[i-1], 4)	# into [0, 0.25, 0.75, 1.0, 1.0, 1.0, 1.0, 1.0].
# 		except IndexError:
# 			pass

# 	x = round(random.uniform(0, 0.9999), 4)			# Generates a random float between 0 and 0.9999 which will determinewhich notelength is picked
# 	for i, chance in enumerate(noteProbabilities):
# 		if x < chance:
# 			return notes[i]
# 			break

# noteValues = [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]
# gridPulsePerMeasure = [0]
# gridNoteValues = []
# sumNoteValues = 0
# measureLength = int(input(">> "))

# gridPulsePerMeasure.append(3)		# The pulses per measure are defined by one smaller block of 3 counts and several smaller blocks with count 2 or 4.
# 									# Here the first block of 3 is added.
# gridLength = 3

# while gridLength < measureLength:		# Fills the remainig part of the grid of pulses with blocks of 2 or 4 untill the grid is full.
# 	if measureLength - gridLength > 2:
# 		i = (randint(0, 1) + 1) * 2
# 	else:
# 		i = 2
# 	print(i)
# 	gridPulsePerMeasure.append(i + gridPulsePerMeasure[-1]) 	# Makes sure the pulses are stacked. For example, [0, 3, 2, 2] gets turned into [0, 3, 5, 7]
# 	gridLength += i

# gridPulsePerMeasureCopy = gridPulsePerMeasure[1:len(gridPulsePerMeasure)]	# Copies the relevant part of the pulses per measure
# gridPulsePerMeasure.pop(-1)													# Gets rid of the last pulse since it is the same as the first of the next measure.
# print(gridPulsePerMeasure)
# print(gridPulsePerMeasureCopy)

# noteDensity = len(noteValues) - int(input(">> "))
# noteVariaty = int(input(">> "))

# while sumNoteValues < measureLength:			# Keeps adding notes untill the measure is completely filled.
# 	nextPulse = gridPulsePerMeasureCopy.pop(0)

# 	while True:									# Keeps adding notes untill a block of counts (the smaller blocks of 2, 3 or 4 counts) is filled.
# 		noteLength = pickNote(noteValues, noteDensity, noteVariaty)			# Picks a notelength

# 		if sumNoteValues + noteLength > nextPulse:		# Checks of the combined notelengths are longer than the next pulse.
# 			noteLength = nextPulse - sumNoteValues		# Adjusts the notelength so it won't exceed the next pulse if it would otherwise.

# 		sumNoteValues += noteLength
# 		gridNoteValues.append(noteLength)

# 		if sumNoteValues == nextPulse:					# Breaks the loop if a block of counts (the smaller blocks of 2, 3 or 4 counts) if full.
# 			break

# print(gridNoteValues)

mylist = [0, 1, 2, 3]
print(mylist[-1])

