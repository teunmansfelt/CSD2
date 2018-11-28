#---------------------------- IMPORTS --------------------------#

import simpleaudio as sa
import time


#---------------------------- OBJECTS --------------------------#

valid_sample = False
valid_rhythm = False
valid_tempo = False
valid_playback = False
running = True

state = 'main'


#--------------------------- FUNCTIONS -------------------------#

# def loop(file_path, times) : # Plays an audiofile a specified number of times
# 	while(times > 0) :
# 		playFile(file_path)
# 		times -= 1

def playRhythm(file_path, times, rhythm, tempo) :  # Plays an audiofile in a specific rhythm.
	while(times > 0) : 
		secPerBeat = 60/tempo # Converts BPM to seconds per beat

		for n in range(0, len(rhythm)) :
			lastSymbol = len(rhythm[n]) - 1
			if(rhythm[n][lastSymbol] == '.') : # Makes sure dotted notes get multiplied by 1.5
				note = float(rhythm[n]) / 1.5
			else :
				note = float(rhythm[n])
			
			amountOfBeats = 4 / note # Converts note-name to the amount of beats
			duration = amountOfBeats * secPerBeat # Calculates the time a note lasts in seconds

			playFile(file_path, duration)

		times -= 1

def playFile(file_path, duration) : # Plays an audiofile for a specified duration
	wave_obj = sa.WaveObject.from_wave_file(file_path)
	play_obj = wave_obj.play()
	time.sleep(duration)

def playWholeFile(file_path) : # Plays an audiofile entirely
	wave_obj = sa.WaveObject.from_wave_file(file_path)
	play_obj = wave_obj.play()
	play_obj.wait_done()

def isFloat(x) : # Checks if an input is a float
	try :
		float(x)
		return True
	except ValueError :
		return False

def validSample(x) : # Checks if a sample can be found/exists
	try :
		playWholeFile(x)
		return True
	except :
		return False	

#--------------------------- EXECUTION -------------------------#

#---startup---#
print("This is a (very simple) sample-playback-program")
print("If you haven't used this program before, please refer to the helpfile, by typing help for possible commands")

while running :
#---main---#
	if(state == 'main') :
		state = input('>> ')

#---quit program---#
	elif(state == 'quit') : # Exits the program
		running = False

#---helpfile---#
	elif(state == 'help') : # Gives a list of possible commands
		print('Possible commands: \n tempo \n rhythm \n sample \n play \n quit')
		state = 'main'

#---tempo input---#
	elif(state == 'tempo') : # Asks the user to input a tempo in BPM
		print('Please insert a tempo in BPM')
		
		valid_tempo = False
		while not valid_tempo : # Keeps asking for an input if the given input is invalid
			tempo = input('>> ')

			if(tempo == 'quit') : # Exits the program
				running = False
				break

			if(tempo.isdigit()) : # Checks if the given input is an integer
				tempo = int(tempo)
				if(tempo >= 30 and tempo <= 500) :	# Checks if the given input is within the bounds
					valid_tempo = True
				else : 
					print('Please insert a whole number from 30 to 500')
			else :
				print('Please insert a whole number from 30 to 500')

		state = 'main'

#---rhythm input---#
	elif(state == 'rhythm') :
		print('Please insert a rhythm')
		print('For rhythm-specifications type help')
		
		valid_rhythm = False
		while not valid_rhythm : # Keeps asking for an input if the given input is invalid
			rhythm = input('>> ')

			if(rhythm == 'quit') : # Exits the program
				running = False
				break

			if(rhythm == 'help') : # A rhythm-specific helpfile
				print('A valid rhythm must be a string, containing numbers spaced with a ","')
				print('"1" is a whole note, "2" is a half note, etc')
				print('Dotted notes can be inserted as an integer followed by a . ')
				print('Note-values may range from 0.25 to 64')
			
			else :
				rhythm = rhythm.split(',') # Splits the string into a list of distinct numbers
				
				valid_rhythm = True
				for x in range(0, len(rhythm)) : # Loops through every note of the rhythm
					rhythm[x] = rhythm[x].strip() # Gets rid of any spaces
					if not isFloat(rhythm[x]) : # Checks if the given rhythm is valid
						valid_rhythm = False
						print('Please insert a (valid) rhythm')
						print('For rhythm-specifications type help')
						break

		state = 'main'

#---sample input---#
	elif(state == 'sample') :
		print('Please insert a sample')
		print('For sample-specifications type help')
		
		valid_sample = False
		while not valid_sample : # Keeps asking for an input if the given input is invalid
			sample = input('>> ')

			if(sample == 'quit') : # Exits the program
				running = False
				break

			if(sample == 'help') : # A sample-specific helpfile
				print("The sample must be inside the resources folder")
				print("The sample can have a maximum bit-depth of 16")
			else :
				sample_path = 'resources/' + sample # Converts the sample to the correct file_path
				if(not validSample(sample_path)) : # Checks if the given sample is valid
					print('Please insert a valid sample')
					print('For sample-specifications type help')
				else :
					valid_sample = True

		state = 'main'

#---playback---#
	elif(state == 'play') :
		if(not valid_tempo) : # Checks if a tempo has been specified before sample-playback
			print('no tempo specified')
			state = 'tempo'
		elif(not valid_rhythm) : # Checks if a rhythm has been specified before sample-playback
			print('no rhythm specified')
			state = 'rhythm'
		elif(not valid_sample) : # Checks if a sample has been specified before sample-playback
			print('no sample specified')
			state = 'sample'
		else :
			print("Please specify how many times you want to repeat the rhythm ")
			print("(must be a whole number from 1 to 10)")

			valid_playback = False
			while not valid_playback : # Keeps asking for an input if the given input is invalid
				numPlaybackTimes = input('>> ')

				if(numPlaybackTimes == 'quit') : # Exits the program
					running = False
					break


				if(numPlaybackTimes.isdigit()) : # Checks if the input is an integer
					numPlaybackTimes = int(numPlaybackTimes) # Converts a valid input-string to an int
					if(numPlaybackTimes >= 1 and numPlaybackTimes <= 10) : # Checks if the input ranges from 1 to 10
						valid_playback = True
						#loop("resources/GTKick.wav", numPlaybackTimes)
						playRhythm(sample_path, numPlaybackTimes, rhythm, tempo) # Plays back the specified sample accordingly to the given inputs
					else :
						print("Please insert a whole number from 1 to 10") 
				else :
					print("Please insert a whole number from 1 to 10")

			state = 'main'

#---invalid command---#
	else :
		print('Invalid command')
		print('refer to the helpfile for possible commands')
		state = 'main'