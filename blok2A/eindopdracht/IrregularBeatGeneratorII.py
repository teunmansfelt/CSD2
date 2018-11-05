
#-------------------- IMPORTS --------------------#
import simpleaudio as sa
import threading as t
import time, random
from math import inf

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

def generateNoteList(pulseGrid, noteProbabilities): # Returns a list of notelengths according to the pulses in the measure, note density and variety of possible note lenghts.
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
		if i > 0:
			gridNoteTimestamps.append(gridNoteTimestamps[i - 1] + noteLength)
		else:
			gridNoteTimestamps.append(noteLength)

	return gridNoteTimestamps

#--randomization--#
def swapNotes(notes, index): # Swaps two consecutive notes
	note1 = notes[index]
	note2 = notes[index + 1]

	notes[index] = note2
	notes[index + 1] = note1

	return notes

def glueNotes(notes, index): # Glues two consecutive notes together.
	notes[index] = notes[index] + notes[index + 1]
	del notes[index + 1]

	return notes

def splitNotes(notes, index): # Splits a note exactly in half.
	note = notes[index]
	note1 = note * 0.5
	note2 = note1

	if note % 0.5 != 0:
		note1 += 0.125
		note2 -= 0.125

	notes[index] = note1
	notes.insert(index + 1, note2)

	return notes

#--input validation--#
def fileAvailable(file_path, error_message): # Checks if a given file can be found/exist.	
	try:
		f = open(str(file_path), "r")
		f.close()
		return True
	except FileNotFoundError:
		print(error_message)
		return False

def sampleAvailable(file_path, error_message): # Checks if a given sample can be found/exist.
	try:
		s = sa.WaveObject.from_wave_file(file_path)
		return True
	except FileNotFoundError:
		print(error_message)
		return False

def validSignature(timeSignature): # Checks if a given timeSignature is valid.
	if not isinstance(timeSignature, str):
		return False
	
	if not timeSignature[1] == '/':
		return False
	
	timeSignature = timeSignature.split('/')
	try:
		int(timeSignature[0])
		if int(timeSignature[0]) % 2 == 0:		# Checks if first number is odd
			return False
	except ValueError:
		return False
	
	try:
		int(timeSignature[1])
		if not int(timeSignature[1]) % 4 == 0:	# Checks if second number is devisible by 4
			return False
	except ValueError:
		return False

	return True

#--misc. functions--#
def clock(): # A clock that updates the global current time every millisecond
	global currentTime

	while not getattr(mainClock, "kill", False):	# Keeps looping, untill the thread gets killed.
		currentTime = time.time()
		time.sleep(0.001)


#-------------------- CLASSES --------------------#
class sampleLayerClass:	# Handles the note generation, note randomization and playback of a sample and keeps track of all the playback-properties. 	
	def __init__(self, name, customPulseGrid, noteDensity, noteLengthVariety, randomization):
		self.name = name
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/" + name)
		self.noteDensity = noteDensity
		self.noteLengthVariety = noteLengthVariety
		self.randomization = randomization
		
		self.rhythm = [0] # This list will store the entire generated rhythm.
		self.rhythmIndex = 0
		self.playing = False

		# Initializes the pulseGrid, the noteList and the timestampList.
		self.noteProbabilities = createProbabilityDistribution(len(noteLengths), self.noteDensity, self.noteLengthVariety)
		self.generateGrids(customPulseGrid)

	def setSample(self, name): # Sets sample and creates a corresponding file_path.
		self.name = name
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/" + name)

	def setNoteDensity(self, value): # Sets the noteDensity and regenerates the noteList.
		self.noteDensity = value
		self.noteProbabilities = createProbabilityDistribution(len(noteLengths), self.noteDensity, self.noteLengthVariety)
		self.noteList = generateNoteList(self.pulseGrid, self.noteProbabilities)

	def setNoteLengthVariety(self, value): # Sets the noteLengthVariety and regenerates the noteList.
		self.noteDensity = value
		self.noteProbabilities = createProbabilityDistribution(len(noteLengths), self.noteDensity, self.noteLengthVariety)
		self.noteList = generateNoteList(self.pulseGrid, self.noteProbabilities)

	def generateGrids(self, customPulseGrid): # Generates the pulseGrid, the noteList and the timestampList
		if not customPulseGrid:
			self.pulseGrid = generatePulseGrid(timeSignature.measureLength)
		else:
			self.pulseGrid = customPulseGrid
		self.noteList = generateNoteList(self.pulseGrid, self.noteProbabilities)
		self.timestampList = noteLengthsToNoteTimestamps(self.noteList)

	def randomize(self): # Randomizes the noteList
		if randomizationMode == "static":
			for i in range(0, self.randomization):								# The self.randomizations sets the amount of randomizations.
				option = random.randint(0,2)									# Determines what type of randomization should be applied.

				if option == 0:
					index = random.randint(0, len(self.noteList)-2)				# Picks a random element from the noteList, excluding the last element.		
					for pulse in self.pulseGrid:								# The code inside this for-loop makes sure the notes that are about to be
						while True:												# swaped, won't effect the original grid of pulses and don't have the same value.
							if self.timestampList[index] == pulse or self.noteList[index] == self.noteList[index + 1]:
								index = random.randint(0, len(self.noteList)-2)
							else:
								break					 
					self.noteListCopy = swapNotes(self.noteList, index)			# Swaps two consecutive notes and stores the outputted list as a copy. 
					self.timestampListCopy = noteLengthsToNoteTimestamps(self.noteListCopy)	

				elif option == 1:
					index = random.randint(0, len(self.noteList)-2)				# Picks a random element from the noteList, excluding the last element.		
					for pulse in self.pulseGrid:								# The code inside this for-loop makes sure the notes that are about to be
						while True:												# glued, won't effect the original grid of pulses.
							if self.timestampList[index + 1] == pulse:
								index = random.randint(0, len(self.noteList)-2)
							else:
								break
					self.noteListCopy = glueNotes(self.noteList, index)			# Glues two consecutive notes and stores the outputted list as a copy. 
					self.timestampListCopy = noteLengthsToNoteTimestamps(self.noteListCopy)

				elif option == 2:
					index1 = random.randint(0, len(self.noteList)-1)			# Picks a random element from the noteList.
					while self.noteList[index1] == 0.25:						# This while-loop makes sure the note is bigger than 0.25.
						index1 = random.randint(0, len(self.noteList)-1)
					self.noteListCopy = splitNotes(self.noteList, index1)		# Splits a note and stores the outputted list as a copy.
					self.timestampListCopy = noteLengthsToNoteTimestamps(self.noteListCopy)

		elif randomizationMode == "evolve":
			for i in range(0, self.randomization):								# The self.randomizations sets the amount of randomizations.
				option = random.randint(0,2)									# Determines what type of randomization should be applied.

				if option == 0:
					index1 = random.randint(0, len(self.noteList)-2)			# Picks a random element from the noteList, excluding the last element.
					self.noteList = swapNotes(self.noteList, index1, index2)	# Swaps two notes.

				elif option == 1:
					index1 = random.randint(0, len(self.noteList)-2)			# Picks a random element from the noteList, excluding the last element.
					self.noteList = glueNotes(self.noteList, index1)			# Glues two notes together.

				elif option == 2:
					index1 = random.randint(0, len(self.noteList)-1)			# Picks a random element from the noteList.
					while self.noteList[index1] == 0.25:						# This while-loop makes sure the note is bigger than 0.25.
						index1 = random.randint(0, len(self.noteList)-1)
					self.noteList = splitNotes(self.noteList, index1)			# Splits a note.

	def play(self): # Plays the sample according to the rhythm stored in self.rhythm.		
		beatDuration = (240 / (timeSignature.beatLength * tempo)) 	# Calculates the duration of a single beat.
		timestamp = self.rhythm[self.rhythmIndex]					# Picks a timestamp from the stored rhythm.
		timestamp *= beatDuration									# Converts the reletave timestamp to an absolute timestamp.

		while self.playing:
			if tempoChange:	# If the tempo is changing, the beat duration and the absolute timestamp get calculated live.					
				beatDuration = (240 / (timeSignature.beatLength * tempo))
				timestamp *= beatDuration

			if currentTime - startTime >= timestamp:		# Checks if the timestamp has passed.
				self.audiofile.play()
				self.rhythmIndex += 1
				timestamp = self.rhythm[self.rhythmIndex]	# Picks a new timestamp from the stored rhythm.
				timestamp *= beatDuration					# Converts the reletave timestamp to an absolute timestamp.
			else:
				time.sleep(0.001)

	def startPlayback(self): # Starts the playback of the sample
		self.playing = True
		self.playback = t.Thread(target = self.play)
		self.playback.start()

	def stopPlayback(self): # Stops the playback of the sample
		self.playing = False
		self.playback.join()
		
class timeSignatureClass: # Stores the timesignature and handles timesignature changes
	def __init__(self, value):
		self.value = value
		self.measureLength = int(value.split('/')[0])
		self.beatLength = int(value.split('/')[1])

	def set(self, value):
		self.value = value
		self.measureLength = int(value.split('/')[0])
		self.beatLength = int(value.split('/')[1])

		for i in range(0, 3): # The code inside this for-loop regenerates the pulseGrids and the noteLists of all the layers.
			if i == 2:	# The third sampleLayer will get a custom pulseGrid.
				sampleLayers[i].generateGrids([0, self.measureLength])
			else:
				sampleLayers[i].generateGrids(False)


#-------------------- OBJECTS --------------------#
noteLengths = [4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25]
sampleLayers = [] # A list to store the sample layer classes.
currentTime = 0 # A global variable to keep track of the current time.
startTime = inf # A global variable to keep track of the start time. (Defaults to infinity to prevent premature playback)

#--default settings--#
tempo = 120
timeSignature = timeSignatureClass("5/4")
randomizationMode = "static"

#--initialization--#
sampleLayers.append(sampleLayerClass("Kick.wav", False, 5, 2, 1))

#--error messages--#
sampleNotInAudioFilesFolder = "Sample not available. \nPlease make sure the sample name is spelled correctly and in the audioFiles folder"
fileNotInSavesFolder = "File not available. \nPlease make sure the file name is spelled correctly and in the saves folder."
helpfileMissing = "The helpfile could not be found. \nPlease make sure you also downloaded the resources folder and put it in the same directory as the script."

#--misc. variables--#
tempoChange = False

#--------------------- MAIN ----------------------#

sampleLayers[0].startPlayback()
time.sleep(1)
sampleLayers[0].stopPlayback()


