
#-------------------- IMPORTS --------------------#
import simpleaudio as sa
import threading as t
import time, random, os, webbrowser


#--------------------- SETUP ---------------------#
filesMissing = "\nOops!, it seems some files are missing. \n-files missing:"

while True:
	missingFiles = []
	if not os.path.exists("./resources"):
		missingFiles.append("/resources")
	else:
		if not os.path.exists("./resources/audioFiles"):
			missingFiles.append("/resources/audioFiles")
		else:
			for i in range(0, 3):
				if not os.path.exists("./resources/audioFiles/Default" + str(i+1) + ".wav"):
					missingFiles.append("/resources/audioFiles/Default" + str(i+1) + ".wav")
		if not os.path.exists("./resources/helpfile.txt"):
			missingFiles.append("/resources/helpfile.txt")

	if len(missingFiles) > 0:
		print(filesMissing)
		for file in missingFiles:
			print(".   " + file)
		print("\nWould you like to download the missing files? (Y/N)\n(You will be directed to a github download page.)")

		while True:
			entry = input(">>> ")
			if entry.upper() == "Y":
				webbrowser.open("https://github.com/teunmansfelt/CSD2/tree/master/blok2A/eindopdracht", new=0, autoraise=True)
				input("Press the enter key to continue ")
				break
			elif entry.upper() == "N":
				entry = input("Press the enter key to continue or type 'quit' the exit the program\n>>> ")
				if entry == "quit":
					exit()
				break
			else:
				print("Unknown command: %s" % entry)
	else:
		break


#-------------------- CLASSES --------------------#
class sampleLayerClass:	# Handles the note generation, note randomization and playback of a sample and keeps track of all the playback-properties. 	
	def __init__(self, name, customPulseGrid, noteDensity, noteLengthVariety, randomization):
		self.name = name
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/" + name)
		self.noteDensity = noteDensity
		self.noteLengthVariety = noteLengthVariety
		self.randomization = randomization
		
		self.rhythm = rhythmClass() # This object will store the entire generated rhythm.
		self.playing = False

		# Initializes the pulseGrid, the noteList and the timestampList.
		self.noteProbabilities = createProbabilityDistribution(len(noteLengths), self.noteDensity, self.noteLengthVariety)
		self.generateGrids(customPulseGrid)
		self.addNotes()

	def setSample(self, name): # Sets sample and creates a corresponding file_path.
		self.name = name
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/" + name)

	def setNoteDensity(self, value): # Sets the noteDensity and regenerates the noteList.
		self.noteDensity = value
		self.noteProbabilities = createProbabilityDistribution(len(noteLengths), self.noteDensity, self.noteLengthVariety)
		self.noteList = generateNoteList(self.pulseGrid, self.noteProbabilities)
		self.timestampList = noteLengthsToNoteTimestamps(self.noteList)
		self.notesToStore = self.noteList.copy()

	def setNoteLengthVariety(self, value): # Sets the noteLengthVariety and regenerates the noteList.
		self.noteLengthVariety = value
		self.noteProbabilities = createProbabilityDistribution(len(noteLengths), self.noteDensity, self.noteLengthVariety)
		self.noteList = generateNoteList(self.pulseGrid, self.noteProbabilities)
		self.timestampList = noteLengthsToNoteTimestamps(self.noteList)
		self.notesToStore = self.noteList.copy()

	def generateGrids(self, customPulseGrid): # Generates the pulseGrid, the noteList and the timestampList.
		if not customPulseGrid:
			self.pulseGrid = generatePulseGrid(timeSignature.measureLength)
		else:
			self.pulseGrid = customPulseGrid
		self.noteList = generateNoteList(self.pulseGrid, self.noteProbabilities)
		self.timestampList = noteLengthsToNoteTimestamps(self.noteList)
		self.notesToStore = self.noteList.copy()
		self.timestampsToStore = self.timestampList.copy()

	def addNotes(self): # Adds the noteLengths and the timestamps to the rhythm
		offset = eventHandler.measureNumber * timeSignature.measureLength
		for timestamp in self.timestampsToStore:
			timestamp += offset
			self.rhythm.timestamps.append(timestamp)
		self.rhythm.noteLengths += self.notesToStore

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
					self.notesToStore = swapNotes(self.noteList, index, False)	# Swaps two consecutive notes and stores the outputted list as a copy. 

				elif option == 1:
					index = random.randint(0, len(self.noteList)-2)				# Picks a random element from the noteList, excluding the last element.		
					for pulse in self.pulseGrid:								# The code inside this for-loop makes sure the notes that are about to be
						while True:												# glued, won't effect the original grid of pulses.
							if self.timestampList[index + 1] == pulse:
								index = random.randint(0, len(self.noteList)-2)
							else:
								break
					self.notesToStore = glueNotes(self.noteList, index)			# Glues two consecutive notes and stores the outputted list as a copy. 

				elif option == 2:
					index = random.randint(0, len(self.noteList)-1)				# Picks a random element from the noteList.
					while self.noteList[index] == 0.25:							# This while-loop makes sure the note is bigger than 0.25.
						index = random.randint(0, len(self.noteList)-1)
					self.notesToStore = splitNotes(self.noteList, index)		# Splits two consecutive notes and stores the outputted list as a copy. 
			self.timestampsToStore = noteLengthsToNoteTimestamps(self.notesToStore)

		elif randomizationMode == "evolve":
			for i in range(0, self.randomization):								# The self.randomizations sets the amount of randomizations.
				option = random.randint(0,2)									# Determines what type of randomization should be applied.

				if option == 0:
					index1 = random.randint(0, len(self.noteList)-2)			# Picks a random element from the noteList, excluding the last element.
					self.noteList = swapNotes(self.noteList, index1, index2)	# Swaps two random notes

				elif option == 1:
					index = random.randint(0, len(self.noteList)-2)				# Picks a random element from the noteList, excluding the last element.
					self.noteList = glueNotes(self.noteList, index)				# Glues two notes together.

				elif option == 2:
					index = random.randint(0, len(self.noteList)-1)				# Picks a random element from the noteList.
					while self.noteList[index1] == 0.25:						# This while-loop makes sure the note is bigger than 0.25.
						index = random.randint(0, len(self.noteList)-1)
					self.noteList = splitNotes(self.noteList, index)			# Splits a note.

			self.notesToStore = self.noteList.copy()
			self.timestampList = noteLengthsToNoteTimestamps(self.notesToStore)
			self.timestampsToStore = self.timestampList.copy()

	def play(self, startTime): # Plays the sample according to the rhythm stored in self.rhythm.									
		note = 0											# The first not should be played instantly.											
		
		while self.playing:
			if tempo.change: # If the tempo is changing, the absolute timestamp is calculated live.					
				note = self.rhythm.getNote()
				note *= eventHandler.beatDuration

			if time.time() - startTime >= note:				# Checks if the duration of the note has passed.
				startTime = time.time()						# Resets the startTime to the current time. 
				s = self.audiofile
				s.play()
				self.rhythm.position += 1					# The first noteLength can be ignored, since it should be played instantly. (this is why the index gets incremented before the getNote() function)
				note = self.rhythm.getNote()				# Picks a new note from the stored rhythm.
				note *= eventHandler.beatDuration			# Converts the reletave noteLength to an absolute noteLength.
				time.sleep(0.0001)
			else:
				time.sleep(0.001)

	def startPlayback(self, startTime): # Starts the playback of the sample
		self.playing = True
		self.playbackThread = t.Thread(target = self.play, args = (startTime,))
		self.playbackThread.start()

	def stopPlayback(self): # Stops the playback of the sample
		self.playing = False
		try:
			self.playbackThread.join()
		except AttributeError:
			pass

	def playOnce(self): # Plays the sample once.
		s = self.audiofile
		s.play()
		
class eventHandlerClass: # Keeps track of the position in the measure and triggers certain events accordingly.
	def __init__(self):
		self.measureNumber = 0
		self.beatDuration = (240 / (timeSignature.beatLength * tempo.value)) 	# Calculates the duration of a single beat.

	def run(self, startTime): # Triggers events according to preprogrammed timestamps.
		beenRandomized = False
		
		while self.running:
			if tempo.change:	# If the tempo is changing, the beat duration is calculated live.					
				self.beatDuration = (240 / (timeSignature.beatLength * tempo.value))

			if time.time() - startTime >= self.measureNumber * timeSignature.measureLength * self.beatDuration and not beenRandomized: # This event gets triggered at the exact start of a measure.
				beenRandomized = True
				for layer in sampleLayers:
					layer.randomize()
			
			elif time.time() - startTime >= (timeSignature.measureLength + self.measureNumber * timeSignature.measureLength) * self.beatDuration - 0.01: # This event gets triggered 10 ms before the next measure.
				self.measureNumber += 1				
				for layer in sampleLayers:
					layer.addNotes()
				beenRandomized = False
			
			else:
				time.sleep(0.001)

	def start(self, startTime): # Starts the event handler.
		self.running = True
		self.eventHandlerThread = t.Thread(target = self.run, args = (startTime,))
		self.eventHandlerThread.start()

	def stop(self): # Stops the event handler.
		self.running = False
		try:
			self.eventHandlerThread.join()
		except AttributeError:
			pass

class timeSignatureClass: # Stores the timesignature and handles timesignature changes.
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

class rhythmClass: # Stores a rhythm in note lengths and timestamps and where to start the playback.
	def __init__(self):
		self.reset()

	def reset(self):
		self.noteLengths = []
		self.timestamps = [0]
		self.position = 0

	def getNote(self):
		return self.noteLengths[self.position]

class tempoClass: # Stores the tempo and handles temposlides.
	def __init__(self, value):
		self.value = value
		self.change = False

	def set(self, value):
		self.change = True
		self.value = value
		time.sleep(0.01)
		self.change = False

	def ramp(self, destination, duration):
		start = self.value
		increment = (destination - start) / duration
		for i in range(0, duration):
			self.value += increment
			time.sleep(0.001)
			if not self.change:
				return
		self.value = destination
		

	def slide(self, destination, duration):
		self.change = True
		self.tempoSlideThread = t.Thread(target = self.ramp, args = (destination, duration))
		self.tempoSlideThread.start()

	def stopSlide(self):
		self.change = False
		try:
			self.tempoSlideThread.join()
		except AttributeError:
			pass


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
def swapNotes(notes, index1, index2): # Swaps two notes
	notesCopy = notes.copy()
	note1 = notesCopy[index1]
	if not index2: # If the second index is false, the second index will be the one after the first index.
		note2 = notesCopy[index1 + 1]
	else:
		note2 = notesCopy[index2]

	notesCopy[index1] = note2
	if not index2:
		notesCopy[index1 + 1] = note1
	else:
		notesCopy[index2] = note1

	return notesCopy

def glueNotes(notes, index): # Glues two consecutive notes together.
	notesCopy = notes.copy()
	notesCopy[index] = notesCopy[index] + notesCopy[index + 1]
	del notesCopy[index + 1]

	return notesCopy

def splitNotes(notes, index): # Splits a note into two smaller notes.
	notesCopy = notes.copy()
	note = notesCopy[index]
	note1 = note * 0.5
	note2 = note1

	if note % 0.5 != 0: # Makes sure the outputted notes are a multiple of 0.25.
		note1 += 0.125
		note2 -= 0.125

	notesCopy[index] = note1
	notesCopy.insert(index + 1, note2)

	return notesCopy

#--input validation--#
def validSample(sample, error_message): # Checks if a given sample can be found/exist and if it's playable.
	try:
		file_path = "resources/audioFiles/" + sample
		s = sa.WaveObject.from_wave_file(file_path)
		return True
	except FileNotFoundError:
		print(error_message)
		return False

def validSignature(timeSignature): # Checks if a given timeSignature is valid.
	if not timeSignature[1] == '/':
		return False	
	timeSignature = timeSignature.split('/')

	try:
		int(timeSignature[0])
		if int(timeSignature[0]) % 2 == 0: # Checks if the first number is odd
			return False
	except ValueError:
		return False
	
	try:
		int(timeSignature[1])
		if not int(timeSignature[1]) % 4 == 0: # Checks if the second number is devisible by 4
			return False
	except ValueError:
		return False

	return True

def commandUsedCorrectly(commandName, lowerbound, upperbound): # Checks if the user input is valid for the following commands: note density, notelength variety and randomization amount
	global state
	global layerIndex

	if not command[1]: # Checks if the command has at least two arguments.
		print("Please specify for which sample layer the %s must be viewed/altered" % commandName)
		state = "main"
		return False
	else:
		validLayer = False # Checks if user inputted a valid sample layer.
		for i, name in enumerate(sampleLayerNames):
			if name == command[1]:
				layerIndex = i
				validLayer = True

		if validLayer:
			if not command[2]: # Checks if the user wants to view or change the command.
				print("The the %s for %s is currently set to %s" % (commandName, command[1], eval("sampleLayers[layerIndex].%s" % command[0])))
				state = "main"
				return False
			else:
				if isFloat(command[2]):
					command[2] = int(command[2])
					if command[2] < lowerbound: # Checks the input's lower bound.
						print("The %s minimum is %s" % (commandName, lowerbound))
						state = "main"
						return False
					elif command[2] > upperbound: # Checks the input's upper bound.
						print("The %s maximum is %s" % (commandName, upperbound))
						state = "main"
						return False
					else:
						state = "main"
						return True
				else:
					goToHelp(command[0])
					return False
		else:
			goToHelp(command[0])
			return False

def isFloat(x): # Checks if an input is a float.
	try :
		float(x)
		return True
	except ValueError :
		return False

#--Misc. functions--#
def goToHelp(subject): # Directs the user to a specified subject in the helpfile.
	global state
	print("invalid Argument")
	state = "help"
	command[1] = subject


#-------------------- OBJECTS --------------------#
noteLengths = [4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25]
sampleLayers = [] # A list to store the sample layer classes.
sampleLayerNames = ["layer1", "layer2", "layer3"]

#--default settings--#
tempo = tempoClass(120)
timeSignature = timeSignatureClass("5/4")
state = "main"
randomizationMode = "static"

#--initialization--#
eventHandler = eventHandlerClass()
sampleLayers.append(sampleLayerClass("Default1.wav", False, 5, 2, 1))
# sampleLayers.append(sampleLayerClass("Default2.wav", False, 5, 2, 0))
# sampleLayers.append(sampleLayerClass("Default3.wav", [0, 11], 5, 2, 0))

#--error messages--#
sampleNotValid = "\nSample not available. \nPlease make sure the sample name is spelled correctly and in the audioFiles folder. \n(For now the program only supports wavfiles with a maximum bitdepth of 16.)\n"
fileNotInSavesFolder = "\nFile not available. \nPlease make sure the file name is spelled correctly and in the saves folder."


#--------------------- MAIN ----------------------#


while True: # This while-loop handles the entire main script.
#--main--#
	if state == "main":
		entry = input(">>> ")
		command = entry.split(' ') 				# splits the input into a list of individual commands.
		for i, element in enumerate(command):	# Removes all empty strings (if the user accidentally typed multiple spaces between commands).
			if element == '':
				del command[i]

		if len(command) < 3:					# Makes sure the entry is always a list of length 3 to								
			for i in range(0, 3-len(command)):	# prevent 'list index out of range'-errors further in
				command.append(False)			# the code.

		state = command[0]						# Directs the user to the correct sub-menu.

#--quit program--#
	if state == "quit":	# Kills all the running threads.
		for layer in sampleLayers:				
			layer.stopPlayback()
		eventHandler.stop()						
		tempo.stopSlide()						
		break

#--helpfile--#
	elif state == "help": # A helpfile.txt is included in the resources folder
		helpfile = open("resources/helpfile.txt", "r")

		while True:													# Reads through the entire helpfile line by line until a line matches the user entry.
			line = helpfile.readline().replace('\n', '').split(' ') # Cleans up the lines in the helpfile.

			if line[0] == command[1] or not command[1]:				# Checks if a line matches the user entry.
				while True:											# Reads out and prints all the lines from the point at which a line matches the user entry until the stop mark.
					line = helpfile.readline().replace('\n', '') 			
					if line[0] == "#":								# Checks if the stopmark has been reached.
						break
					print(line)
				break	
			elif line[0] == "###":									# Checks if the end of the helpfile has been reached
				print("No helpfile available for command: %s." % command[1])
				break

		helpfile.close()
		state = "main"

#--overview--#
	elif state == "overview": 
		print("\nGeneral:")
		print(" - tempo: %s" % str(tempo.value))
		print(" - time signature: %s" % timeSignature.value)
		print(" - randomization mode: %s" % randomizationMode)

		for i, layer in enumerate(sampleLayers):
			print("\nSampleLayer %s:" % str(i+1))
			print(" - sample: %s" % layer.name)
			print(" - note density: %s" % str(layer.noteDensity))
			print(" - notelength variety: %s" % str(layer.noteLengthVariety))
			print(" - randomization amount: %s" % str(layer.randomization))

		state = "main"

#--tempo input--#
	elif state == "tempo":
		if not command[1]: # Checks if the user wants to view or change the tempo.
			print("The tempo is currently set to %d BPM" % tempo.value)
			state = "main"
		else:
			if isFloat(command[1]):
				command[1] = float(command[1])
				if command[1] < 30:	# Input lower bound.
					print("The tempo minimum is 30")
					state = "main"
				elif command[1] > 500:	# Input upper bound.
					print("The tempo maximum is 500")
					state = "main"
				else:
					if not command[2]: # Checks if the user wants the tempo to jump or slide.
						tempo.stopSlide() # Terminates the tempo slide thread if it is still running.
						tempo.set(command[1])
						state = "main"
					elif isFloat(command[2]):
						command[2] = int(command[2])
						tempo.stopSlide()
						tempo.slide(command[1], command[2])
						state = "main"
					else:
						goToHelp("tempo") 
			else:
				goToHelp("tempo")

#--timesignature input--#
	elif state == "timeSignature":
		if not command[1]: # Checks if the user wants to view or change the timesignature.
			print("The time signature is curently set to %s" % timeSignature)
			state = "main"
		else:
			if validSignature(command[1]):
				timeSignature.set(command[1])
			else:
				goToHelp("timeSignature")

#--sample choice--#
	elif state == "sample":
		if not command[1]: # Checks if the command is being used correctly.
			print("Please specify which sample layer must be viewed/altered")
			state = "main"
		else:
			validLayer = False
			for i, name in enumerate(sampleLayerNames):
				if name == command[1]:
					layerIndex = i
					validLayer = True

			if validLayer:
				if not command[2]:
					sampleLayers[layerIndex].playOnce()
					print("\nThe sample of %s is currently set to %s" % (command[1], sampleLayers[layerIndex].name))
					state = "main"
				else:
					if validSample(command[2], sampleNotValid):
						sampleLayers[layerIndex].setSample(command[2])
						sampleLayers[layerIndex].playOnce()
					state = "main"
			else:
				goToHelp("sample")

#--note density input--#
	elif state == "noteDensity":
		layerIndex = 0
		if commandUsedCorrectly("note density", 1, 8):
			sampleLayers[layerIndex].setNoteDensity(command[2])

#--notelength variety input--#
	elif state == "noteLengthVariety":
		layerIndex = 0
		if commandUsedCorrectly("notelength variety", 0, 25):
			sampleLayers[layerIndex].setNoteLengthVariety(command[2])

#--randomization input--#
	elif state == "randomization":
		if command[1] == "mode":
			if not command[2]:
				print("The current randomization mode is set to %s" % randomizationMode)
				state = "main"
			elif command[2] == "none" or command[2] == "static" or command[2] == "evolve":
				randomizationMode = command[2]
				state = "main"
			else:
				goToHelp(command[0])
		else:
			layerIndex = 0
			if commandUsedCorrectly("randomization", 0, 2):
				sampleLayers[layerIndex].randomization = command[2]

#--start playback--#
	elif state == "startPlayback":
		startTime = time.time() + 0.1
		for layer in sampleLayers:
			layer.startPlayback(startTime)
		eventHandler.start(startTime)
		time.sleep(0.5)
		state = "main"


