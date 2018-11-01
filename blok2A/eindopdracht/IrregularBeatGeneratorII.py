
#-------------------- IMPORTS --------------------#
import threading as t
import time
import random

#------------------- FUNCTIONS -------------------#
#--rhythm generation--#
def createProbabilityDistribution(length, centrePosition, spread): # Returns a list of harmonically scaled probabilities
	#----#
	# This function returns a list, with a specified length, of probabilities according to a harmonic distribution.
	# The distrubution is dependant on a centreposition and a spread. The centreposition determines where the highest
	# probability in the list is. The spread determines how many non-zero probabilities are in the list.
	#----#

	probabilityDistribution = []
	n = spread + 1

	k = 1													
	while k <= n:											# The code inside these two while-loops will create a list of harmonically scaled probabilities with a specified length n (spread).
		probabilityDistribution.append(round(k/(n*n), 4))	# The created list will have the following form:
		k += 1												# [1/n*n,  2/n*n,  3/n*n,  ...,  (n-1)/n*n,  n/n*n,  (n-1)/n*n,  ...,  3/n*n,  2/n*n,  1/n*n].
	k -= 2													# The term n/n*n will correspond to the highest probability and will therefore be on the centreposition when 
	while k > 0:											# the probabilityDistribution list is mapped onto the noteProbability list. Since the noteProbability list will have a fixed length,
		probabilityDistribution.append(round(k/(n*n), 4))	# some elements of the probabilityDistribution list will exceed the bounds of the noteProbability list after mapping.
		k -= 1

	outOfBounds = 0											
	if centrePosition - spread < 0:							# Checks if any elements from the probabilityDistribution list would exceed the left bound of the noteProbability list after mapping.
		for i in range(0, spread - centrePosition):			# Loops through all the elements which exceed the left bound.
			outOfBounds += probabilityDistribution.pop(0) 	# Adds the value of all the elements which exceed the left bound to the outOfBounds variable and removes them from the probabilityDistribution list.

	if centrePosition + spread > length - 1: 				# Checks if any elements from the probabilityDistribution list would exceed the right bound of the noteProbability list after mapping.					
		for i in range(0, spread):							# Loops through all the elements which exceed the right bound.
			outOfBounds += probabilityDistribution.pop(-1)	# Adds the value of all the elements which exceed the right bound to the outOfBounds variable and removes them from the probabilityDistribution list.

	for i, probability in enumerate(probabilityDistribution):								# Distributes the outOfBounds value evenly over the remaining probabilities.
		probabilityDistribution[i] = probability + outOfBounds/len(probabilityDistribution)	# This ensures all the probabilities will add up to 100% (1.0).

	noteProbabilities = [0]*length								# Initializes the noteProbability list with the default probability of each element set to 0.					
	for i, probability in enumerate(probabilityDistribution):	# The code inside this for-loop maps the probabilityDistribution list onto the noteProbability list.
		if centrePosition - spread >= 0:													
			noteProbabilities[i + centrePosition - spread] = probability
		else:
			noteProbabilities[i] = probability

	for i, chance in enumerate(noteProbabilities):								# The code inside this for-loop stacks the noteProbabilities.
		if i > 0:																# For example: [0, 0.25, 0.5, 0.25, 0, 0, 0, 0] gets turned
			noteProbabilities[i] = round(chance + noteProbabilities[i-1], 4)	# into [0, 0.25, 0.75, 1.0, 1.0, 1.0, 1.0, 1.0].
		else:
			noteProbabilities[i] = round(chance, 4)
	return noteProbabilities

def pickNote(notes, probabilities): # Returns a note from a list of possible notelengths according to probability
	x = round(random.uniform(0, 0.9999), 4)		# This random number will determine which notelength is picked.
	for i, chance in enumerate(probabilities):	# The code inside this for-loop picks a note from the notes list at the index
		if x < chance:							# at which the probability is bigger than the randomly generated number.
			return notes[i]

def generatePulseGrid(measureLength): # Returns a grid of pulses according to the timesignature. 
	#----#
	# This function will return a grid of pulses according to the timesignature (length of a measure). The pulses
	# are determined by stacking blocks. The first block always has length 3 and is the followed by blocks of length
	# 2 or 4 until the measure is completely filled.
	#----#

	gridPulsePerMeasure = [0]

	gridPulsePerMeasure.append(3)			# Adds the first block (with a length of 3)
	gridLength = 3
	
	while gridLength < measureLength:		# The code inside this while-loop fills the remainig part of the
		if measureLength - gridLength > 2:	# grid of pulses with blocks of length 2 or 4, until the grid is full.
			i = (randint(0, 1) + 1) * 2
		else:
			i = 2
		gridPulsePerMeasure.append(i + gridPulsePerMeasure[-1])	# Stacks the pulses. For example, [0, 3, 2, 2] gets turned into [0, 3, 5, 7].
		gridLength += i

	return gridPulsePerMeasure

def generateNoteGrid(pulseGrid, noteProbabilities): # Returns a list of notelengths according to the pulses in the measure, note density and variety of possible note lenghts.
	gridNoteLengths = []
	sumNoteValues = 0	
	gridPulsePerMeasure = pulseGrid[1:len(pulseGrid)]	# Copies the relevant part of the pulses per measure.

	measureLength = pulseGrid[-1]						# The last value in the pulseGrid corresponds to the length of the measure
	while sumNoteValues < measureLength:				# The code inside this while-loop makes sure notes are being added, until the measure is completely filled.
		nextPulse = gridPulsePerMeasure.pop(0)

		while sumNoteValues < nextPulse:				# Keeps adding notes until the next pulse is reached.
			noteLength = pickNote(noteLengths, noteProbabilities) # Picks a notelength

			if sumNoteValues + noteLength > nextPulse:	# Checks if the combined notelengths have passed the next pulse.
				noteLength = nextPulse - sumNoteValues	# Adjusts the notelength so it won't exceed the next pulse if it would otherwise.

			sumNoteValues += noteLength
			gridNoteLengths.append(noteLength)			# Stores all the picked notes in a list

	return gridNoteLengths

def noteLengthsToNoteTimestamps(noteLengths): # Converts a lis of notelenghts into a list of relative timestamps.
	gridNoteTimestamps = []

	for i, noteLength in enumerate(noteLengths):
		try:
			gridNoteTimestamps.append(gridNoteTimestamps[i - 1] + noteLength)
		except IndexError:
			gridNoteTimestamps.append(noteLength)

	return gridNoteTimestamps


#-------------------- CLASSES --------------------#
class sampleLayerClass:	# Handles the playback of a sample and keeps track of all the playback-properties. 	
	def __init__(self, name, customPulseGrid, noteDensity, noteLengthVariety, randomization):
		self.name = name
		self.file_path = 'resources/audioFiles/' + name
		self.noteDensity = noteDensity
		self.noteLengthVariety = noteLengthVariety
		self.randomization = randomization

		# Initializes the pulseGrid and the noteGrid 
		self.noteProbabilities = createProbabilityDistribution(len(noteLengths), self.noteDensity, self.noteLengthVariety)
		if not customPulseGrid:
			self.pulseGrid = generatePulseGrid(timeSignature.measureLength)
		else:
			self.pulseGrid = customPulseGrid
		self.noteGrid = generateNoteGrid(self.pulseGrid, self.noteProbabilities)

	def setSample(self, name): # sets sample and creates a corresponding file_path.
		self.name = name
		self.file_path = 'resources/audioFiles/' + name

	def setNoteDensity(self, value): # sets the noteDensity and regenerates the noteGrid.
		self.noteDensity = value
		self.noteProbabilities = createProbabilityDistribution(len(noteLengths), self.noteDensity, self.noteLengthVariety)
		self.noteGrid = generateNoteGrid(self.pulseGrid, self.noteProbabilities)

	def setNoteLengthVariety(self, value): # sets the noteLengthVariety and regenerates the noteGrid.
		self.noteDensity = value
		self.noteProbabilities = createProbabilityDistribution(len(noteLengths), self.noteDensity, self.noteLengthVariety)
		self.noteGrid = generateNoteGrid(self.pulseGrid, self.noteProbabilities)

	def generateGrids(self, customPulseGrid): # regenerates
		if not customPulseGrid:
			self.pulseGrid = generatePulseGrid(timeSignature.measureLength)
		else:
			self.pulseGrid = customPulseGrid
		self.noteGrid = generateNoteGrid(self.pulseGrid, self.noteProbabilities)

class timeSignatureClass: # Stores the timesignature information and handles timesignature changes
	def __init__(self, value):
		self.value = value
		self.measureLength = int(value.split('/')[0])
		self.pulseLength = int(value.split('/')[1])

	def set(self, value):
		self.value = value
		self.measureLength = int(value.split('/')[0])
		self.pulseLength = int(value.split('/')[1])

		# Regenerates the pulseGrids and  the noteGrids of all the layers
		for i in range(0, 3):
			if i == 2:	# the third sampleLayer will get a custom pulseGrid
				sampleLayers[i].generateGrids([0, self.measureLength])
			else:
				sampleLayers[i].generateGrids(False)

#-------------------- OBJECTS --------------------#
noteLengths = [4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25]
sampleLayers = [] # a list to store the sample layer classes.

#--default settings--#
tempo = 120
timeSignature = timeSignatureClass("5/4")
randomizationMode = "regular"

#--initialization--#
sampleLayers.append(sampleLayerClass("Kick.wav", False, 5, 2, 0))

#--------------------- MAIN ----------------------#








