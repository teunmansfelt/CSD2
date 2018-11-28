#-------------------- IMPORTS --------------------#
import simpleaudio as sa
import threading as t
import time
import random
from random import randint


#-------------------- OBJECTS --------------------#
pulseGrids = [[], [], []]		# A two dimensional list which keeps track of all three pulseGrids.
noteGrids = [[], [], []]		# A two dimensional list which keeps track of all three noteLengthGrids.
rhythms = [[0], [0], [0]]		# A two dimensional list which keeps track of all three rhythms.
rhythmIndecis = [0, 0, 0]		# A list to keep track of where to start in the rhythm per sample.

state = "main"
entry = "user input"
threads = ['playlow', 'playmid', 'playhigh', 'clock', 'tempo', 'timer']	# A list to keep track of al the threads. The strings inside corresponds to the function of each thread.
noteValues = [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]		# A list of possible notelengths.
currentTime = 0		# A global variable to keep track of the time.

#--default settings--#
samples = ["Kick.wav", "Dog2.wav", "Pop.wav"]		# A list to store the three samplenames.

tempo = 120

timeSignature = "5/4"
measureLength = 5
pulseLength = 4

noteDensity = [2, 2, 2]
noteLengthVariaty = [2, 2, 2]
randomization = [0, 0, 0]
randomizationMode = 'regular'

#--error messages--#
sampleNotInAudioFilesFolder = "Sample not available. \nPlease make sure the sample name is spelled correctly and in the audioFiles folder"
fileNotInSavesFolder = "File not available. \nPlease make sure the file name is spelled correctly and in the saves folder."
helpfileMissing = "The helpfile could not be found. \nPlease make sure you also downloaded the resources folder and put it in the same directory as the script."

#--misc. variables--#
playbackStarted = False
tempoChange = False


#------------------- FUNCTIONS -------------------#

#--sample playback--#
def playOnce(sample): # Plays a sample exactly once.
	file_path = "resources/audioFiles/" + sample
	s = sa.WaveObject.from_wave_file(file_path)
	s.play()

def playRhythm(sample_type, startTime, rhythmIndex): # Handels the playback of the 'low', 'mid' and 'high' sample.
	global currentTime

	print(currentTime)

	if sample_type == "low":	# Checks if the  low sample should be played.
		sampleIndex = 0
	elif sample_type == "mid":	# Checks if the  mid sample should be played.
		sampleIndex = 1
	elif sample_type == "high":	# Checks if the  high sample should be played.
		sampleIndex = 2

	pulseDuration = (15 * pulseLength) / tempo		# Calculates the duration of a pulse.
	timeStamp = rhythms[sampleIndex][rhythmIndex]	# Picks a timestamp from the global rhythm list. (sampleIndex determines for what sample, rhythmIndex determines where to start in the rhythm).	
	timeStamp *= pulseDuration 	# Converts reletave timestamp to absolute timestamp

	while not getattr(threads[sampleIndex], "kill", False):	# Keeps looping, untill the thread gets killed.
		if tempoChange:		# If the tempo is changing, the quarternote duration and timestamp gets calculated live.
			pulseDuration = (15 * pulseLength) / tempo		
			timeStamp = rhythms[sampleIndex][rhythmIndex]
			timeStamp *= pulseDuration

		if currentTime - startTime >= timeStamp:	# Checks if the timestamp is passed.
			playOnce(samples[sampleIndex])
			rhythmIndex += 1
			timeStamp = rhythms[sampleIndex][rhythmIndex]
			timeStamp *= pulseDuration
		else:
			time.sleep(0.001)

	return rhythmIndex

#--rhythm generation--#
def pickNote(notes, position, spread): # Returns a note from a list of possible notelengths according to probability
	probabilityDistribution = []
	n = spread + 1

	k = 1													
	while k <= n:											# Initializes a list of harmonically scaled probability with a specified length (spread)
		probabilityDistribution.append(round(k/(n*n), 4))	# For example, if the spread was 3 the generated probability list would look as follows:
		k += 1												# [1/(3)^2, 2/(3)^2, 3/(3)^2, 2/(3)^2, 1/(3)^2]
	k -= 2													# The general output with a spread of n would look like this:
	while k > 0:											# [1/n^2, 2/n^2, 3/n^2, ..., n-1/n^2, n/n^2, n-1/n^2, ..., 3/n^2, 2/n^2, 1/n^2]
		probabilityDistribution.append(round(k/(n*n), 4))
		k -= 1

	outOfBounds = 0											
	if position - spread < 0:								# Checks if the probabilityDistribution exceeds the lower bound of the list of possible notelengths (index < 0).
		for i in range(0, spread - position):				# Loops through al the probabilities which exceed the lower bound.
			outOfBounds += probabilityDistribution.pop(0)	# Adds up all the probabilities which exceed the lower bound.

	if position + spread > len(notes) - 1:					# Checks if the probabilityDistribution exceeds the upper bound of the list of possible notelengths (index > len(notes)).
		for i in range(0, spread):							# Loops through al the probabilities which exceed the upper bound.
			outOfBounds += probabilityDistribution.pop(-1)	# Adds all the probabilities which exceed the upper bound to the probabilities that exceeded the lower bound.

	for i, probability in enumerate(probabilityDistribution):								# Distributes all the probabilities which were out of bound evenly to the remaining probabilities.
		probabilityDistribution[i] = probability + outOfBounds/len(probabilityDistribution)	# This ensures all the probabilities will add up to 100%.

	noteProbabilities = [0]*len(notes)												# Initializes a list with the same length as the list of possible notelengths.
	for i in range(0, len(probabilityDistribution)):								# Pastes the probabilityDistribution on the correct position
		if position - spread >= 0:													# in relation to the notelengths.
			noteProbabilities[i + position - spread] = probabilityDistribution[i]
		else:
			noteProbabilities[i] = probabilityDistribution[i]

	for i, chance in enumerate(noteProbabilities):								# Loops through the probabilities and stacks them.
		try:																	# For example: [0, 0.25, 0.5, 0.25, 0, 0, 0, 0] gets turned
			noteProbabilities[i] = round(chance + noteProbabilities[i-1], 4)	# into [0, 0.25, 0.75, 1.0, 1.0, 1.0, 1.0, 1.0].
		except IndexError:
			pass

	x = round(random.uniform(0, 0.9999), 4)				# Generates a random float between 0 and 0.9999 which will determinewhich notelength is picked.
	for i, chance in enumerate(noteProbabilities):
		if x < chance:
			return notes[i]

def generatePulseGrid(measureLength): # Returns a grid of pulses according to the timesignature. 
	gridPulsePerMeasure = [0]

	gridPulsePerMeasure.append(3)			# The pulses per measure are defined by one smaller block of 3 counts and several smaller blocks with count 2 or 4.
											# Here the first block of 3 is added.
	gridLength = 3
	while gridLength < measureLength:		# Fills the remainig part of the grid of pulses with blocks of 2 or 4 untill the grid is full.
		if measureLength - gridLength > 2:
			i = (randint(0, 1) + 1) * 2
		else:
			i = 2
		gridPulsePerMeasure.append(i + gridPulsePerMeasure[-1])	# Makes sure the pulses are stacked. For example, [0, 3, 2, 2] gets turned into [0, 3, 5, 7].
		gridLength += i

	return gridPulsePerMeasure

def generateNoteGrid(pulseGrid, noteDensity, noteVariaty): # Returns a grid of notelengths according to the pulses in the measure, note density and variaty of possible note lenghts.
	gridNoteLengths = []
	sumNoteValues = 0	
	gridPulsePerMeasure = pulseGrid[1:len(pulseGrid)]	# Copies the relevant part of the pulses per measure.

	measureLength = pulseGrid[-1]						# The last value in the pulseGrid corresponds to the length of the measure
	while sumNoteValues < measureLength:				# Keeps adding notes untill the measure is completely filled.
		nextPulse = gridPulsePerMeasure.pop(0)

		while True:										# Keeps adding notes untill a block of counts (the smaller blocks of 2, 3 or 4 counts) is filled.
			noteLength = pickNote(noteValues, noteDensity, noteVariaty)		# Picks a notelength

			if sumNoteValues + noteLength > nextPulse:	# Checks of the combined notelengths are longer than the next pulse.
				noteLength = nextPulse - sumNoteValues	# Adjusts the notelength so it won't exceed the next pulse if it would otherwise.

			sumNoteValues += noteLength
			gridNoteLengths.append(noteLength)

			if sumNoteValues == nextPulse:				# Breaks the loop if a block of counts (the smaller blocks of 2, 3 or 4 counts) if full.
				break

	return gridNoteLengths

def noteLengthsToNoteTimestamps(noteLengths): # Converts a lis of notelenghts into a list of relative timestamps.
	gridNoteTimestamps = []

	for i, noteLength in enumerate(noteLengths):
		try:
			gridNoteTimestamps.append(gridNoteTimestamps[i - 1] + noteLength)
		except IndexError:
			gridNoteTimestamps.append(noteLength)

	return gridNoteTimestamps

#--randomization--#
def swapNotes(notes, index1, index2): # Swaps to notes in a list on the specified indecis.
	note1 = notes[index1]
	note2 = notes[index2]

	notes[index1] = note2
	notes[index2] = note1

	return notes

def glueNotes(notes, index): # Glues two consecutive notes together.
	notes[index] = notes[index] + notes[index + 1]
	del notes[index + 1]

	return notes

def splitNotes(notes, index): # splits a note exactly in half.
	note = notes[index]
	note *= 0.5

	notes[index] = note
	notes.insert(index + 1, note)

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

def sampleAvailable(sample, error_message): # Checks if a given sample can be found/exist.
	file_path = "resources/audioFiles/" + sample
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

	while not getattr(threads[3], "kill", False):	# Keeps looping, untill the thread gets killed.
		currentTime = time.time()
		time.sleep(0.001)

def tempoSlide(start, end, milliseconds): # Let's the tempo slide from a start value to an end value in a specified amount of milliseconds.
	global tempo, tempoChange
	tempoChange = True
	tempo = start
	for i in range(0, milliseconds):
		tempo += ((end - start) / milliseconds)
		time.sleep(0.001)
		if getattr(threads[3], "kill", False):
			break
	tempo = end
	time.sleep(0.003)
	tempoChange = False

def isFloat(x): # Checks if an input is a float.
	try :
		float(x)
		return True
	except ValueError :
		return False

def goToHelp(subject): # Directs the user to a specified subject in the helpfile.
	global state
	print("invalid Argument")
	state = "help"
	entry[1] = subject


#---------------------- MAIN ---------------------#

#--startup--#
print("This is an Irregular Beat Generator. It will generate rhythms with an odd time signature.")
print("If you haven't used this program before, please refer to the helpfile, by typing help for possible commands.")

for i in range(0, 3):
	if i == 2:
		pulseGrids[i] = [0, measureLength]
	else:
		pulseGrids[i] = generatePulseGrid(measureLength)
	noteGrids[i] = generateNoteGrid(pulseGrids[i], noteDensity[i], noteLengthVariaty[i])

while True:
#--main--#
	if state == "main":
		entry = input(">> ")					# Entry is the command inputted by the user.
		entry = entry.split(' ')				# Turns an input consisting of multiple commands (words) into a list of individual commands.
		for i, command in enumerate(entry):		# Removes all empty strings, if the user accidentally typed multiple spaces between commands.
			if command == '':
				del entry[i]
		
		if len(entry) < 3:						# Makes sure the entry is always a list of length 3 to								
			for i in range(0, 3-len(entry)):	# prevent 'list index out of range'-errors further in
				entry.append(False)				# the code.

		state = entry[0]	# Directs the user to the correct sub-menu.

#--quit program--#
	elif state == "quit":
		for thread in threads:	# Kills all the threads which are still running before quiting the program.
			try:
				thread.kill = True
				thread.join()
			except AttributeError:
				pass
		break

#--help file--#	
	elif state == "help":	# A helpfile.txt is included in the resources folder
		if fileAvailable("resources/helpfile.txt", helpfileMissing): # Checks if the helpfile is available
			helpfile = open("resources/helpfile.txt", "r")

			while True:													# Reads through the entire helpfile line by line until a line matches the user entry.
				line = helpfile.readline().replace('\n', '').split(' ') # Cleans up the lines in the helpfile.

				if line[0] == entry[1] or not entry[1]:					# Checks if a line matches the user entry.
					while True:											# Reads out and prints all the lines from the point at which a line matches the user entry until the stop mark.
						line = helpfile.readline().replace('\n', '') 			
						if line[0] == "#":								# Checks if the stopmark has been reached.
							break
						print(line)
					break	
				elif line[0] == "###":									# Checks if the end of the helpfile has been reached
					print("No helpfile available for command: %s." % entry[1])
					break

		helpfile.close()
		state = "main"

#--tempo input--#
	elif state == "tempo":
		if not entry[1]:	# Checks if the user wants to view or change the tempo.							
			print("The tempo is currently set to %d BPM" % tempo)
			state = "main"
		else:
			if isFloat(entry[1]):	# Checks if the input is a number.
				entry[1] = float(entry[1])
				if entry[1] < 30:	# Checks the input's lower bound.
					print("The tempo minimum is 30")
					state = "main"
				elif entry[1] > 500:	# Checks the input's upper bound.
					print("The tempo maximum is 500")
					state = "main"
				else:
					if not entry[2]:	# Checks if the user wants the tempo to jump or slide to the next value.
						tempoChange = True
						tempo = entry[1]
						time.sleep(0.003)
						tempoChange = False
						state = "main"
					elif isFloat(entry[1]):	# Checks if the input is a number.
						entry[2] = int(entry[2])

						try:	# Terminates the tempo slide thread if it is still running.
							threads[4].kill
							threads[4],join()				
						except AttributeError:
							pass

						threads[4] = t.Thread(target=tempoSlide, args=(tempo, entry[1], entry[2])) # Initializes a thread to handle the tempo slide.
						threads[4].start()
						state = "main"		
			else:	# Directs the user to the helpfile if the command is used incorrectly.
				goToHelp("tempo")

#--time signature input--#
	elif state == "timeSignature":
		if not entry[1]:	# Checks if the user wants to view or change the timesignature.
			print("The time signature is curently set to %s" % timeSignature)
			state = "main"
		else:
			if validSignature(entry[1]):	# Checks if the input is in the correct format.
				timeSignature = entry[1]
				measureLength = int(timeSignature.split('/')[0])	# If the timesignature is X/Y, this will equal X.
				pulseLength = int(timeSignature.split('/')[1])	# If the timesignature is X/Y, this will equal Y.
				
				for i in range(0, 3):
					if i == 2:
						pulseGrids[i] = [0, measureLength]
					else:
						pulseGrids[i] = generatePulseGrid(measureLength)
					noteGrids[i] = generateNoteGrid(pulseGrids[i], noteDensity[i], noteLengthVariaty[i])

				state = "main"
			else:							# Directs the user to the helpfile if the command is used incorrectly.
				goToHelp("timeSignature")

#--sample choice--#
	elif state == "sample":
		if not entry[1]:	# Checks if the command is being used correctly.
			print("Please specify which sample must be viewed/altered")
			state = "main"
		else:
			validEntry = False
			if entry[1] == "low":		# Checks if the low sample should be viewed/altered.
				sampleListIndex = 0		
				validEntry = True
			elif entry[1] == "mid":		# Checks if the mid sample should be viewed/altered.
				sampleListIndex = 1		
				validEntry = True
			elif entry[1] == "high":	# Checks if the high sample should be viewed/altered.
				sampleListIndex = 2			
				validEntry = True
			
			if validEntry:	# Checks if the input is valid.
				if not entry[2]:	# Checks if the user wants to view/listen to or change a sample.
					if sampleAvailable(samples[sampleListIndex], sampleNotInAudioFilesFolder):	# Checks if the sample is in the correct folder and playable.
						playOnce(samples[sampleListIndex])	# Previews the sample to the user.
						print("The %s sample is currently set to %s" % (entry[1], samples[sampleListIndex]))						
					state = "main"
				else:
					if sampleAvailable(entry[2], sampleNotInAudioFilesFolder):	# Checks if the inputted sample is in the correct folder and playable.
						samples[sampleListIndex] = entry[2]	# Updates the list of sample
						playOnce(entry[2])	# Previews the sample to the user.
					state = "main"

			else:	# Directs the user to the helpfile if the command is used incorrectly.
				goToHelp("sample")

#--note density input--#
	elif state == "noteDensity":
		if not entry[1]:	# Checks if the command is being used correctly.
			print("Please specify for which sample the note density must be viewed/altered")
			state = "main"
		else:
			validEntry = False
			if entry[1] == "low":		# Checks if the note density of the low sample should be viewed/altered.
				noteDensityListIndex = 0	
				validEntry = True
			elif entry[1] == "mid":		# Checks if the note density of the mid sample should be viewed/altered.
				noteDensityListIndex = 1
				validEntry = True
			elif entry[1] == "high":	# Checks if the note density of the high sample should be viewed/altered.
				noteDensityListIndex = 2
				validEntry = True
			
			if validEntry:	# Checks if the input is valid.
				if not entry[2]:	# Checks if the user wants to view or change the noteDensity.
					print("The the note density for the %s sample is currently set to %s" % (entry[1], noteDensity[noteDensityListIndex]))
					state = "main"
				else:
					if isFloat(entry[2]):	# Checks if the input is a number.
						entry[2] = int(entry[2])
						if entry[2] < 1:	# Checks the input's lower bound.
							print("The note density minimum is 1")
							state = "main"
						elif entry[2] > 8:	# Checks the input's upper bound.
							print("The note density maximum is 8")
							state = "main"
						else:
							noteDensity[noteDensityListIndex] = len(noteValues) - entry[2] # Inverts the input so a lower number will correspond to a lower note density.
							
							idx = noteDensityListIndex
							noteGrids[idx] = generateNoteGrid(pulseGrids[idx], noteDensity[idx], noteLengthVariaty[idx])

							state = "main"

					else:	# Directs the user to the helpfile if the command is used incorrectly.
						goToHelp("noteDensity")

			else:	# Directs the user to the helpfile if the command is used incorrectly.
				goToHelp("noteDensity")

#--notelength variaty input--#
	elif state == "noteLengthVariaty":
		if not entry[1]:	# Checks if the command is being used correctly.
			print("Please specify for which sample the note variaty must be viewed/altered")
			state = "main"
		else:
			validEntry = False
			if entry[1] == "low":		# Checks if the notelength variaty of the low sample should be viewed/altered.
				noteLengthVariatyListIndex = 0	
				validEntry = True
			elif entry[1] == "mid":		# Checks if the notelength variaty of the mid sample should be viewed/altered.
				noteLengthVariatyListIndex = 1
				validEntry = True
			elif entry[1] == "high":	# Checks if the notelength variaty of the high sample should be viewed/altered.
				noteLengthVariatyListIndex = 2
				validEntry = True
			
			if validEntry:	# Checks if the input is valid.
				if not entry[2]:	# Checks if the user wants to view or change the noteVariaty.
					print("The the notelength variaty for the %s sample is currently set to %s" % (entry[1], noteVariaty[noteLengthVariatyListIndex]))
					state = "main"
				else:
					if isFloat(entry[2]):	# Checks if the input is a number.
						entry[2] = int(entry[2])
						if entry[2] < 1:	# Checks the input's lower bound.
							print("The notelength variaty minimum is 1")
							state = "main"
						elif entry[2] > 25:	# Checks the input's upper bound.
							print("The notelength variaty maximum is 25")
							state = "main"
						else:
							noteVariaty[noteLengthVariatyListIndex] = entry[2]
							
							idx = noteLengthVariatyListIndex
							noteGrids[idx] = generateNoteGrid(pulseGrids[idx], noteDensity[idx], noteLengthVariaty[idx])

							state = "main"

					else:	# Directs the user to the helpfile if the command is used incorrectly.
						goToHelp("noteVariaty")

			else:	# Directs the user to the helpfile if the command is used incorrectly.
				goToHelp("noteVariaty")

#--randomization input--#
	elif state == "randomization":
		if not entry[1]:	# Checks if the command is being used correctly.
			print("Please specify for which sample the randomization must be viewed/altered")
			state = "main"
		else:
			if entry[1] == "mode":				
				validEntry = False
				if entry[1] == "low":		
					randomizationListIndex = 0	
					validEntry = True
				elif entry[1] == "mid":		
					randomizationListIndex = 1
					validEntry = True
				elif entry[1] == "high":
					randomizationListIndex = 2
					validEntry = True

#--grid regeneration--#
	elif state == "regenerate":
		if not entry[1]:
			print("Please specify for which sample you want to regenerate the rhythm")
			state = "main"
		else:
			validEntry = False
			if entry[1] == "low":		# Checks if the rhythm of the low sample should be regenerated.
				regenerateIndex = 0		
				validEntry = True
			elif entry[1] == "mid":		# Checks if the rhythm of the mid sample should be regenerated.
				regenerateIndex = 1		
				validEntry = True
			elif entry[1] == "high":	# Checks if the rhythm of the high sample should be regenerated.
				regenerateIndex = 2			
				validEntry = True

			if validEntry:	# Checks if the input is valid.
				idx = regenerateIndex
				
				if not idx == 2:
					pulseGrids[idx] = generatePulseGrid(measureLength)
				noteGrids[idx] = generateNoteGrid(pulseGrids[idx], noteDensity[idx], noteLengthVariaty[idx])

			state = "main"

#--start playback--#
	elif state == "startPlayback":
		playbackStarted = True
		readyForPlayback = True 	# Assumes all samples are ready.
		for sample in samples:		# Checks if all samples are ready.
			if not sampleAvailable(sample, sampleNotInAudioFilesFolder):			
				readyForPlayback = False	# Stops playback if one of the samples is not available.
				break
		
		if readyForPlayback:		# Checks if the code is ready for playback.
			for i in range(0, 3):
				rhythms[i]+=noteLengthsToNoteTimestamps(noteGrids[i])	# Adds the first grid of notes to the global rhythm list.

			startTime = time.time() + 0.1	# Sets the starttime a little ahead so the code has time to start the threads.
			threads[0] = t.Thread(target=playRhythm, args=("low", startTime, rhythmIndecis[0]))	# playback threadfor low sample.
			threads[1] = t.Thread(target=playRhythm, args=("mid", startTime, rhythmIndecis[1]))	# playback threadfor mid sample.
			threads[2] = t.Thread(target=playRhythm, args=("high", startTime, rhythmIndecis[2]))	# playback threadfor high sample.
			threads[3] = t.Thread(target=clock)	# Starts global clock (sets current time)

			for i in range(0, 4):	# Starts all the threads.
				threads[i].start()

			time.sleep(0.15)	# Pauses the code to prevent blocking of the input() by a possible warning message.
								# (This warning message only occures on some computers, and it has to do with the 
								# SimpleAudio Library, not the code itself. This is a crude work around, but for now
								# it's the only solution I could find).
		else:
			pass
		state = "main"

#--stop playback--#
	elif state == "stopPlayback":
		if playbackStarted:
			for i in range(0, 4):	# Stop all the threads corresponding to playback.
				threads[i].kill = True
				rhythmIndecis[i] = threads[i].join()
		else:
			print("playback hasn't been started yet. (command: startPlayback)")

		playbackStarted = False
		state = "main"

#--pause--#
	elif state == "pause":
		if playbackStarted:
			for i in range(0, 4):	# Stop all the threads corresponding to playback.
				threads[i].kill = True
				rhythmIndecis[i] = threads[i].join()
		else:
			print("playback hasn't been started yet. (command: startPlayback)")

		state = "main"

#--unpause--#
	elif state == "unpause":
		if playbackStarted:
			startTime = time.time() + 0.1	# Sets the starttime a little ahead so the code has time to start the threads.
			threads[0] = t.Thread(target=playRhythm, args=("low", startTime, rhythmIndecis[0]))	# playback threadfor low sample.
			threads[1] = t.Thread(target=playRhythm, args=("mid", startTime, rhythmIndecis[1]))	# playback threadfor mid sample.
			threads[2] = t.Thread(target=playRhythm, args=("high", startTime, rhythmIndecis[2]))	# playback threadfor high sample.
			threads[3] = t.Thread(target=clock)	# Starts global clock (sets current time)

			for i in range(0, 4):	# Starts all the threads.
				threads[i].start()

			time.sleep(0.15)	# Pauses the code to prevent blocking of the input() by a possible warning message.
								# (This warning message only occures on some computers, and it has to do with the 
								# SimpleAudio Library, not the code itself. This is a crude work around, but for now
								# it's the only solution I could find).
		else:
			print("playback hasn't been started yet. (command: startPlayback)")

		state = "main"

#--unknown command--#
	else:
		print("Unknown command: %s" % entry[0])
		state = "help"
		entry[1] = False
