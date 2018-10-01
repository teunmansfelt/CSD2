
#---------------------------- IMPORTS --------------------------#
import simpleaudio as sa
import time
from random import randint

#---------------------------- OBJECTS --------------------------#
samples = ["Dog2.wav", "Laser1.wav", "Pop.wav", "aSound.wav"] # list of samples
tempo = 120 # sets default tempo

#--------------------------- FUNCTIONS -------------------------#
def randomSample(samples_list): # Picks a random sample from a list of possible samples
	i = randint(0, len(samples_list) - 1) # Generates a random integer
	file_path = "audioFiles/" + samples_list[i] # Creates file_path
	return sa.WaveObject.from_wave_file(file_path) # Returns file_path

def durationsToTimestamps16th(durations): # Converts note-durations into sixteenth-note-timestamps
	timestamps16th = [0] # Initialize list of timestamps
	for i in range(len(durations)): # Loops through al durations
		timestamps16th.append(float(durations[i]) * 4 + timestamps16th[i])
	return timestamps16th

def timestamps16thToTimeValues(timestamps, tempo): # Converts sixteenth-note-timestamps to timevalues in seconds
	sixteenthNoteDuration = 15/tempo # Calculates the duration of a sixteenth note based on a specified tempo
	for i in range(len(timestamps)): # Loops through al timestamps
		timestamps[i] *= sixteenthNoteDuration
	return timestamps

def playSequence(sample, timestamps): #Plays a sample in a sequence
	timestamp = timestamps.pop(0) # retrieve first timestamp
	startTime = time.time() # retrieve the startime: current time

	keepPlaying = True
	while keepPlaying: # play the sequence
		currentTime = time.time() # retrieve current time
	  
		if(currentTime - startTime >= timestamp): # check if the timestamp's time is passed
			sample.play() # play sample
			if timestamps: # if there are timestamps left in the timestamps list
				timestamp = timestamps.pop(0) # retrieve the next timestamp
			else: # list is empty, stop loop
				keepPlaying = False 
		else: # wait for a very short moment
			time.sleep(0.001)

def isFloat(x): # Checks if an input is a float
	try:
		float(x)
		return True
	except ValueError:
		return False

#--------------------------- EXECUTION -------------------------#
print("This is a (very simple) sample-playback-program")
print("The default tempo is set to 120")

#---tempo input---#
print("Would you like to change the tempo? (Y/N)")

YesOrNo = False
while not YesOrNo: # Keeps asking for Yes or No if the input is neither
	insert = input(">> ")

	if(insert == 'y' or insert == 'Y'): # Checks if the user wants to change the tempo
		YesOrNo = True
		print("Please insert a tempo in BPM")

		valid_tempo = False
		while not valid_tempo: # Keeps asking for an input if the given input is invalid
			tempo = input(">> ")

			if(isFloat(tempo)): # Checks if the given input is an integer
				tempo = float(tempo)
				if(tempo >= 30 and tempo <= 500):	# Checks if the given input is within the bounds
					valid_tempo = True
				else: 
					print("Please insert a number from 30 to 500")
			else:
				print("Please insert anumber from 30 to 500")
	
	elif(insert == 'n' or insert == 'N'): # Breaks the loop if the user doesn't want to change the tempo
		YesOrNo = True
	
	else:
		print("I don't understand, please awnser with Y or N")

print("The Tempo is set to %d BPM" % (tempo))
print('')

#---rhythm input---#
print('Please insert a rhythm')
print('For rhythm-specifications type help')
		
valid_rhythm = False
while not valid_rhythm: # Keeps asking for an input if the given input is invalid
	rhythm = input('>> ')

	if(rhythm == 'help'): # A rhythm-specific helpfile
		print('A valid rhythm must be a string, containing note durations spaced with a blank space')
		print('0.25 is a 16th note, 0.5 is an 8th note, 1 is a 4th note, etc.')
		print('Note-values may range from 0.01 to 100')

	else:
		rhythm = rhythm.split(' ') # Splits the string into a list of distinct numbers
		try: # Removes any empty strings as a result of accidentally typing two consecutive spaces
			rhythm.remove('')
		except ValueError:
			break

		valid_rhythm = True
		for x in range(0, len(rhythm)): # Loops through every note of the rhythm
			if not isFloat(rhythm[x]): # Checks if the given rhythm is valid
				valid_rhythm = False
				print('Please insert a (valid) rhythm')
				print('For rhythm-specifications type help')
				break

#---playback---#
sample = randomSample(samples)
timestamps16th = durationsToTimestamps16th(rhythm)
timestamps = timestamps16thToTimeValues(timestamps16th, tempo)
playSequence(sample, timestamps)











