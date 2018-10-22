#-------------------- IMPORTS --------------------#
import simpleaudio as sa
import threading as t
import time
import random


#-------------------- OBJECTS --------------------#
state = "main"
entry = "user input"
threads = ['playlaag', 'playmid', 'playhoog', 'tempo']		# A list to keep track of al the threads. The strings inside corresponds to the function of each thread.
noteValues = [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]				# A list of possible notelengths.
samples = ["Kick.wav", "Kick.wav", "Kick.wav"]						# A list to store the three samplenames.

#--default settings--#
tempo = 120

timeSignature = "5/4"
measureLength = 5
pulseLength = 4

noteDensity = [2, 3, 1]
noteLengthVariaty = [2, 1, 3]

#--error messages--#
sampleNotInAudioFilesFolder = "Sample not available. \nPlease make sure the sample name is spelled correctly and in the audioFiles folder"
fileNotInSavesFolder = "File not available. \nPlease make sure the file name is spelled correctly and in the saves folder."
helpfileMissing = "The helpfile could not be found. \nPlease make sure you also downloaded the resources folder and put it in the same directory as the script."


#------------------- FUNCTIONS -------------------#
def playOnce(sample): # Plays a sample exactly once.
	file_path = "resources/audioFiles/" + sample
	s = sa.WaveObject.from_wave_file(file_path)
	s.play()

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
			break

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
	gridNoteValues = []
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
			gridNoteValues.append(noteLength)

			if sumNoteValues == nextPulse:				# Breaks the loop if a block of counts (the smaller blocks of 2, 3 or 4 counts) if full.
				break

	return gridNoteValues

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

def tempoSlide(start, end, milliseconds): # Let's the tempo slide from a start value to an end value in a specified amount of milliseconds.
	global tempo
	tempo = start
	for i in range(0, milliseconds):
		tempo += ((end - start) / milliseconds)
		time.sleep(0.001)
		if getattr(threads[3], "kill", False):
			break
	tempo = end

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
						tempo = entry[1]
						state = "main"
					elif isFloat(entry[1]):	# Checks if the input is a number.
						entry[2] = int(entry[2])

						try:	# Terminates the tempo slide thread if it is still running.
							threads[3].kill
							threads[3],join()				
						except AttributeError:
							pass

						threads[3] = t.Thread(target=tempoSlide, args=(tempo, entry[1], entry[2])) # Initializes a thread to handle the tempo slide.
						threads[3].start()
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
							state = "main"

					else:	# Directs the user to the helpfile if the command is used incorrectly.
						goToHelp("noteVariaty")

			else:	# Directs the user to the helpfile if the command is used incorrectly.
				goToHelp("noteVariaty")

#--start playback--#
	

#--stop playback--#
