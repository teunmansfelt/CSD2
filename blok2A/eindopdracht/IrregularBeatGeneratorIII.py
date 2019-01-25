#-------------------- IMPORTS --------------------#
import simpleaudio as sa 				# Sample playback 
import threading as t 					# Multithreading module
import curses as c 						# User interface
import time, random, math, os			# Miscellaneous libraries

#-------------------- CLASSES --------------------#
class rhythm_player_class:  # Class to handle the playback of a rhythm.
	def __init__(self, audiofile, custom_grid=None):
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/{0}".format(audiofile))    # Sample (playback) object.
		self.rhythm = rhythm_class(custom_grid)    # Object to handle rhythm generation and rhythm storage.

	def set_sample(self, audiofile):
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/{0}".format(audiofile))

	def play(self, start_time):    # sample playback function.
		timestamp = self.rhythm.get_timestamp()
		beat = 0    # Variable to keep track of how many beats have passed.
		while(start_time - time.time() > 0):    # Check if the start time is passed (makes sure all rhythms play in sync).
			time.sleep(0.0005)
		reference_time = time.time()    # Set a reference time.
		while(self.playing):    # Keep looping until playback is stopped.
			if(beat >= timestamp):    # Check if the timestamp is passed.
				self.audiofile.play()
				timestamp = self.rhythm.get_timestamp()    # Retrieve a new timestamp.
				if(self.rhythm.rhythm_index >= len(self.rhythm.rhythm)):    # Check if the end of the rhythm is reached.
					self.rhythm.add_timestamps()    # Add the buffered timestamps to the rhythm.
			else:
				time.sleep(0.0005)    # Wait a bit (prevents cpu overload).
				beat += (time.time() - reference_time) * tempo.bps    # Add the amount of beats passed since last check.
				reference_time = time.time()    # Reset the reference time.

	def play_once(self):
		self.audiofile.play()

	def start_playback(self, start_time):
		self.playing = True     # Keep the playback going.
		t.Thread(target=self.play, args=(start_time,)).start()    # Start a thread to handle the playback function.
		if(self.rhythm.randomization > 0):    # Check if the rhythm should be randomized.
			self.timestamps_to_add = []
			self.rhythm.randomize()    # Initial rhythm randomization.

	def stop_playback(self):
		self.playing = False    # Break the loop in the playback function. (kills the playback thread)

class rhythm_class:  # Class to handle rhythm generation and rhythm storage.
	def __init__(self, custom_grid):
		self.rhythm_density = 0    # Variable to set the rhythm density.
		self.note_diversity = 0    # Variable to set the diversity in note_lengths.
		self.randomization = 0	   # Variable to set the number of randomizations.
		self.reset(custom_grid)    # Resets the class to default state.

	def create_rhythm(self):    # Rhythm creation function.
		note_probability_distribution = create_probability_distribution(len(notes), self.rhythm_density, self.note_diversity)    # list of probabilities that a certain note will be picked.
		rhythm = []
		rhythm_length = 0    # Variable to keep track of the sum of all note lengths.

		for pulse in self.pulse_grid[1:len(self.pulse_grid)]:    # Go through all pulses in the rhythm except the first.
			while(rhythm_length < pulse):    # Keep adding notes, until the next pulse is reached.
				note = pick_item(notes, note_probability_distribution)    # Pick a new note.
				if(note + rhythm_length > pulse):    # Check if the new note will exceed the next pulse.
					note = pulse - rhythm_length    # Adjust the note length.
				rhythm_length += note
				rhythm.append(note)
		
		return rhythm

	def randomize(self):     # Rhythm randomization function
		randomizations = self.randomization    # Variable to keep track of the number of randomizations left to do.
		if(randomization_mode == "static"):
			while(randomizations > 0):
				tries = 0    # Variable to keep track of how many times a false randomization was attempted.									
				option = random.randint(0,2)    # Determines what type of randomization should be applied.

				if(option == 0):    # Swap two consecutive notes.
					index = random.randint(0, len(self.notes)-2)    # Pick a random index in the rhythm, excluding the last index.									
					while(tries < 3):    # Stop trying after three false randomizations.
						if(self.timestamps[index + 1] in self.pulse_grid or self.notes[index] == self.notes[index + 1]): # Check if the randomization is valid.
							index = random.randint(0, len(self.notes)-2)    # Pick a new index.
							tries += 1
						else:
							break					 
					notes_to_add = swap_notes(self.notes, index)

				elif(option == 1):    # Glue two consecutive notes together.
					index = random.randint(0, len(self.notes)-2)    # Pick a random index in the rhythm, excluding the last index.											
					while(tries < 3):    # Stop trying after three false randomizations.										
						if(self.timestamps[index + 1] in self.pulse_grid):    # Check if the randomization is valid.
							index = random.randint(0, len(self.notes)-2)    # Pick a new index.
							tries += 1
						else:
							break
					notes_to_add = glue_notes(self.notes, index)

				elif(option == 2):    # Split a note in half.
					index = random.randint(0, len(self.notes)-1)    # Pick a random index in the rhythm.
					while(self.notes[index] == 0.25 and tries < 3):		# Check if the randomization is valid and stop trying after three false randomizations.
						index = random.randint(0, len(self.notes)-1)    # Pick a new index.
						tries += 1
					notes_to_add = split_notes(self.notes, index)
				randomizations -= 1
			self.timestamps_to_add = notes_to_timestamps(notes_to_add)

		elif(randomization_mode == "evolve"):
			while(randomizations > 0):
				option = random.randint(0,2)    # Determines what type of randomization should be applied.

				if(option == 0):    # Swap two consecutive notes.
					index1 = random.randint(0, len(self.notes)-2)    # Pick a random index in the rhythm, excluding the last index.
					self.notes = swap_notes(self.notes, index1, index2)	# Swaps two random notes

				elif(option == 1):    # Glue two consecutive notes together.
					index = random.randint(0, len(self.notes)-2)    # Pick a random index in the rhythm, excluding the last index.
					self.notes = glue_notes(self.notes, index)			# Glues two notes together.

				elif(option == 2):    # Split a note in half.
					index = random.randint(0, len(self.notes)-1)    # Pick a random index in the rhythm.
					while(self.notes[index1] == 0.25 and tries < 3):	# Check if the randomization is valid and stop trying after three false randomizations.
						index = random.randint(0, len(self.notes)-1)
					self.notes = split_notes(self.notes, index)
				randomizations -= 1
			self.timestamps = notes_to_timestamps(self.notes)    # Overwrite the original rhythm.
			self.timestamps_to_add = self.timestamps.copy()

	def add_timestamps(self):    # Function to add the buffered timestamps to the rhythm.
		try:
			offset = self.rhythm[-1]
			for timestamp in self.timestamps_to_add[1:len(self.timestamps_to_add)]:
				self.rhythm.append(timestamp + offset)    # Add the timestamp + an offset as a result of the measure number.
		except IndexError:
			for timestamp in self.timestamps_to_add:
				self.rhythm.append(timestamp)    # Add the timestamp + the offset as a result of the measure number.
		if(self.randomization > 0):    # Check if randomization should be aplied.
			self.randomize()

	def get_timestamp(self):    # Timestamp getter.
		timestamp = self.rhythm[self.rhythm_index]
		self.rhythm_index += 1
		return timestamp

	def set_rhythm_lists(self, custom_grid=None):    # Regenerates the rhythm and sets the buffer.
		if(custom_grid):
			self.pulse_grid = custom_grid    # Grid to keep track of the pulses in the rhythm.
		else:
			self.pulse_grid = create_pulse_grid()
		self.notes = self.create_rhythm()    # List to store the note lengths.
		self.timestamps = notes_to_timestamps(self.notes)    # List to store the timestamps of the original rhythm (self.notes)
		self.timestamps_to_add = self.timestamps.copy()    # List to buffer the timestamps which will be added next measure.

	def reset(self, custom_grid):    # Resets the class to default state.
		self.rhythm_index = 0    # Variable to keep track of what timestamp should be retrieved.
		self.set_rhythm_lists(custom_grid)    # Inits the rhythm and buffer.
		self.rhythm = []    # array to store the timestamps for playback.
		self.add_timestamps()
		
class time_signature_class:  # Class to handle the timesignature.
	def __init__(self, num_of_pulses, pulse_length):
		self.set(num_of_pulses, pulse_length)

	def set(self, num_of_pulses, pulse_length):
		self.measure_length = num_of_pulses    # Amount of beats in a bar.
		self.beat_length = pulse_length    # Duration of a single beat.
		self.value = "{0}/{1}".format(num_of_pulses, pulse_length)

		for i, player in enumerate(rhythm_players):    # Regenerate the rhythms of every rhythm player.
			if(i == 2):
				player.rhythm.set_rhythm_lists([0, self.measure_length])
			else:
				player.rhythm.set_rhythm_lists()

class tempo_class:  # Class to handle the tempo.
	def __init__(self, value):
		self.value = value    # Tempo in beats per minute.
		self.bps = value / 60    # Beats per second.

	def set(self, value):
		self.value = value
		self.bps = value / 60

	def ramp(self, destination, duration):    # Function to make the tempo slide.
		start = self.value
		increment = (destination - start) / duration    # Calculate tempo increment step.
		for i in range(0, duration):
			self.value += increment
			self.bps = self.value / 60
			if not self.slide:    # Return when the slide is stopped manually.
				return
			time.sleep(0.001)
		self.value = destination    # Elimenate rounding errors.
		self.bps = self.value / 60
		

	def start_slide(self, destination, duration):
		self.slide = True    # Keep the tempo slide goinig.
		t.Thread(target=self.ramp, args=(destination, duration)).start()    # Start a thread to handle the tempo slide.

	def stop_slide(self):
		self.slide = False    # Stop the tempo slide.

class gui_class:  # Class to handle the user interface.
	def __init__(self):
		self.bar = "_"
		self.line = 0    # Variable to keep track of which line the curser is on.

	def init(self):
		c.initscr()    # Inits a blank terminal screen.
		c.reset_shell_mode()	
		print("\nIrregular Beat Generator III   -   by: Teun Mansfelt")
		print("{0}\ncommand execution:".format(self.bar*53))

	def go_up(self, x, mode=None):    # Make the curser go up x lines.
		for i in range(0, x):
			print("\033[F", end="")    # Go up a line
			if(mode == "delete"):
				print("\033[K", end="")    # Clear up a line

	def go_down(self, x):    # Make the curser go down x lines.
		for i in range(0, x):
			print("\033[B", end="")    # Go down a line

	def get_input(self):    # Handle user input.
		self.go_down(10 - self.line)    # Go to the command line.
		print("\033[K", end="")
		self.go_up(2)
		command = input("{0}\ncommand line:\n  >>> ".format(self.bar*53))    # Ask for input.
		self.go_up(3)
		self.go_up(8, "delete")    # Clear previous command.
		self.line = 0
		return command

	def unknown_command(self, command):    # Proces unknown user input.
		print("!! Unknown command : {0}".format(command))
		self.line += 1

	def set_tempo(self):    # Set or slide the tempo.
		print("\n  - Duration: ")
		self.go_up(2)
		value = -1	
		self.line += 1
		while(value == -1):    # Keep looping untill a valid input is given.
			self.line -= 1
			print("\033[K", end="")
			value = input("  - Value: ")    # Ask for input.
			self.line += 1
			if(value == "exit"):    # Exit the loop.
				return
			try:
				value = int(value)    # Make sure the input is an integer.
				if(value < 50 or value > 300):    # Check the bounds.
					print("\n\n\033[K", end="!! Tempo value can range from 50 to 300.")
					self.go_up(3)
					value = -1
			except ValueError:
				print("\n\n\033[K", end="!! Tempo value must be an integer.")
				self.go_up(3)
				value = -1

		duration = input("  - Duration: ")    # Ask for input.
		self.line += 1
		if(duration == "exit"):    # Exit the loop.
			return
		tempo.stop_slide()    # Make sure there are no tempo slide threads running.
		print("\033[K", end="")
		try:
			duration = int(duration)    # Make sure the input is an integer.
			if(duration > 0):
				tempo.start_slide(value, duration)    # Slide to the new tempo.
				print("\nTempo slide started succesfully.")
			else:    # Set the tempo if the duration wasn't a non-zero positive integer.
				tempo.set(value)    # Set the new tempo.
				print("\nTempo value set to: {0}.".format(value))
		except ValueError:    # Set the tempo if the duration wasn't a non-zero positive integer.
			tempo.set(value)    # Set the new tempo.
			print("\nTempo value set to: {0}.".format(value))
		self.line += 2

	def set_timesignature(self):    # Set the time signature.
		print("\n  - Pulse length:")
		self.go_up(2)
		value1 = -1
		self.line += 1
		while(value1 == -1):    # Keep looping untill a valid input is given.
			self.line -= 1
			print("\033[K", end="")
			value1 = input("  - Number of pulses: ")    # Ask for input.
			self.line += 1
			if(value1 == "exit"):    # Exit the loop.
				return
			try:
				value1 = int(value1)    # Make sure the input is an integer.
				if(value1 < 3):    # Check the bounds.
					print("\n\n\033[K", end="!! Minimum number of pulses : 3.")
					self.go_up(3)
					value1 = -1
			except ValueError:
				print("\n\n\033[K", end="!! Number of pulses must be an integer.")
				self.go_up(3)
				value1 = -1

		value2 = -1
		self.line += 1
		while(value2 == -1):    # Keep looping untill a valid input is given.
			self.line -= 1
			print("\033[K", end="")
			value2 = input("  - Pulse length: ")    # Ask for input.
			self.line += 1
			if(value2 == "exit"):    # Exit the loop.
				return
			try:
				value2 = int(value2)    # Make sure the input is an integer.
				if(value2 < 1):    # Check the bounds.
					print("\n\033[K", end="!! Minimum pulse length : 1.")
					self.go_up(2)
					value2 = -1
				if(not (math.log(value2)/math.log(2)).is_integer()):    # Make sure the input is a power of 2.
					print("\n\033[K", end="!! Pulse length must be a power of 2.")
					self.go_up(2)
					value2 = -1
			except ValueError:
				print("\n\n\033[K", end="!! Pulse length must be an integer.")
				self.go_up(2)
				value2 = -1

		time_signature.set(value1, value2)    # Set the new time signature.
		print("\033[K", end="")
		print("\nTime signature set to : {0}.".format(time_signature.value))
		self.line += 2

	def set_samples(self):    # Set the audiofiles used for playback.
		self.sample_list = []    # Initialize a list for all available samples.
		for root, dirs, files in os.walk("resources/audioFiles"):    # Loop throu the files in de audiofiles directory.
			for file in files:
				if(file.endswith(".wav")):    # Check if the file is a '.wav' file.
					self.sample_list.append(file)    # Add the file to the list.
		num_of_pages = math.ceil(len(self.sample_list) / 10)    # Calculate the number of needed pages.
		self.show_sample_page(1, num_of_pages)    # Display the first page.

		print("\n  Sample 2 :")
		print("  Sample 3 :")
		self.go_up(3)
		samples = []

		for i, player in enumerate(rhythm_players):    # Loop through all rhythm players.
			sample = None
			self.line += 1
			while(True):    # Keep looping untill a valid input is given.
				self.line -= 1
				print("\033[K", end="")
				sample = input("  Sample {0} : ".format(i + 1))
				self.line += 1
				if(sample == "exit"):    # Exit the loop.
					self.go_down(24 - self.line)
					self.go_up(13, "delete")
					self.go_up(11 - self.line)
					return
				elif(sample == ""):    # Skip this element.
					if(i == 2):    # Clear the terminal after the last rhythm player.
						self.go_down(24 - self.line)
						self.go_up(13, "delete")
						self.go_up(11 - self.line)
					break
				elif(sample.startswith("page ")):    # Go to a different page of samples.
					try:
						page = int(sample.split(' ')[1])    # Make sure the page number is a positive integer. 
						if(page > num_of_pages):    # Make sure the page number is smaller than or equal to the number of pages.
							self.go_down(3 - i)
							print("\033[K", end="!! Maximum page number : {0}.".format(num_of_pages))
							self.go_up(4 - i)
						else:
							self.show_sample_page(page, num_of_pages)
							self.go_up(1)
					except ValueError:
						self.go_down(3 - i)
						print("\033[K", end="!! Invalid sample : {0}".format(sample))
						self.go_up(4 - i)
				elif(valid_sample(sample)):    # Check if the input is valid.
					player.set_sample(sample)    # Set the audiofile of the rhythm player to the sample.
					self.go_down(3 - i)
					print("\033[K", end="Sample {0} set succesfully.".format(i + 1))
					self.go_up(3 - i)
					if(i == 2):    # Clear the terminal after the last rhythm player.
						self.go_down(24 - self.line)
						self.go_up(13, "delete")
						self.go_up(11 - self.line)
					break
				else:
					self.go_down(3 - i)
					print("\033[K", end="!! Invalid sample : {0}".format(sample))
					self.go_up(4 - i)

	def show_sample_page(self, page, num_of_pages):    # Show all available samples.
		self.go_down(24 - self.line)
		self.go_up(12, "delete")
		print("\033[K", end="{0}\nAvailable samples : page {1} of {2}".format(self.bar*53, page, num_of_pages))
		count = 0
		for i in range(10 * page - 10, 10 * page):
			try:
				print("\n\033[K", end="  {0}".format(self.sample_list[i]))
				count += 1
			except IndexError:
				break
		self.go_up(13 - self.line + count)

#------------------- FUNCTIONS -------------------#
#--rhythm generation--#
def create_probability_distribution(length, centre, spread):
	#----#
	# This function returns a list, with a specified length, of probabilities according to a harmonic distribution.
	# The distrubution is dependant on a centreposition and a spread. The centreposition determines where the highest
	# probability in the list is. The spread determines how many non-zero probabilities are in the list.
	#----#

	probability_distribution = []
	n = spread + 1
	k = 1													
	while(k <= n):											# The code inside these two while-loops will create a list of harmonically scaled probabilities with a specified length n (spread).
		probability_distribution.append(round(k/(n*n), 4))	# The created list will have the following form:
		k += 1												# [1/n*n,  2/n*n,  3/n*n,  ...,  (n-1)/n*n,  n/n*n,  (n-1)/n*n,  ...,  3/n*n,  2/n*n,  1/n*n].
	k -= 2													# The term n/n*n will correspond to the highest probability and will therefore be on the centreposition when 
	while(k > 0):											# the probabilityDistribution list is mapped onto the noteProbability list. Since the noteProbability list will have a fixed length,
		probability_distribution.append(round(k/(n*n), 4))	# some elements of the probabilityDistribution list will exceed the bounds of the noteProbability list after mapping.
		k -= 1

	out_of_bounds = 0											
	if(centre - spread < 0):									# Checks if any elements from the probabilityDistribution list would exceed the left bound of the noteProbability list after mapping.
		for i in range(0, spread - centre):						# Loops through all the elements which exceed the left bound.
			out_of_bounds += probability_distribution.pop(0) 	# Adds the value of all the elements which exceed the left bound to the outOfBounds variable and removes them from the probabilityDistribution list.

	if(centre + spread > length - 1): 							# Checks if any elements from the probabilityDistribution list would exceed the right bound of the noteProbability list after mapping.					
		for i in range(0, spread):								# Loops through all the elements which exceed the right bound.
			out_of_bounds += probability_distribution.pop(-1)	# Adds the value of all the elements which exceed the right bound to the outOfBounds variable and removes them from the probabilityDistribution list.

	for i, probability in enumerate(probability_distribution):									# Distributes the outOfBounds value evenly over the remaining probabilities.
		probability_distribution[i] = probability + out_of_bounds/len(probability_distribution)	# This ensures all the probabilities will add up to 100% (1.0).

	probabilities = [0]*length									# Initializes the noteProbability list with the default probability of each element set to 0.					
	for i, probability in enumerate(probability_distribution):	# The code inside this for-loop maps the probabilityDistribution list onto the noteProbability list.
		if(centre - spread >= 0):													
			probabilities[i + centre - spread] = probability
		else:
			probabilities[i] = probability

	for i, chance in enumerate(probabilities):							# The code inside this for-loop stacks the noteProbabilities.
		if(i > 0):														# For example: [0, 0.25, 0.5, 0.25, 0, 0, 0, 0] gets turned
			probabilities[i] = round(chance + probabilities[i-1], 4)	# into [0, 0.25, 0.75, 1.0, 1.0, 1.0, 1.0, 1.0].
		else:
			probabilities[i] = round(chance, 4)
	return probabilities

def create_pulse_grid():  # Creates a grid of pulses for a rhythm.
	pulse_grid = [0, 3]    # Initial pulses.
	grid_length = 3    # Variable to keep track of the sum of the pulses.

	while(grid_length < time_signature.measure_length):    # Keep adding pulses until the grid has the length of a measure.
		if(time_signature.measure_length - grid_length >= 4):
			pulse = random.randint(1, 2) * 2    # Add a pulse of 2 or 4.
		else:
			pulse = time_signature.measure_length - grid_length    # Makes sure the grid length doesn't exceed the measure length.
		
		pulse_grid.append(pulse + pulse_grid[-1])
		grid_length += pulse

	return pulse_grid

def pick_item(items, probabilities):  # Returns a note from a list of possible notelengths according to probability.
	x = round(random.uniform(0.0000, 0.9999), 4)		
	for i, chance in enumerate(probabilities):    # Loop through the probabilities.
		if x < chance:    # Check if random number is passed.
			return items[i]
	return None    # Might only returns None if the probability list doesn't contain a 1 (100%)

def notes_to_timestamps(notes):  # Converts note lenghts to relative timestamps.
	timestamps = [0]
	for note in notes:
		timestamps.append(timestamps[-1] + note)
	return timestamps

#--randomization--#
def swap_notes(rhythm, index):  # Swaps two notes
	rhythm_copy = rhythm.copy()
	temp = rhythm_copy[index]
	rhythm_copy[index] = rhythm_copy[index + 1]
	rhythm_copy[index + 1] = temp
	return rhythm_copy

def glue_notes(rhythm, index):  # Glues two consecutive notes together.
	rhythm_copy = rhythm.copy()
	rhythm_copy[index] = rhythm_copy[index] + rhythm_copy[index + 1]
	del rhythm_copy[index + 1]
	return rhythm_copy

def split_notes(rhythm, index):  # Splits a note into two smaller notes.
	rhythm_copy = rhythm.copy()
	note = rhythm_copy[index]
	note1 = note * 0.5
	note2 = note1

	if note % 0.5 != 0: # Makes sure the outputted notes are a multiple of 0.25.
		note1 += 0.125
		note2 -= 0.125

	rhythm_copy[index] = note1
	rhythm_copy.insert(index + 1, note2)
	return rhythm_copy

#--input validation--#
def valid_sample(sample):
	try:
		sa.WaveObject.from_wave_file("resources/audioFiles/{0}".format(sample))
		return True
	except FileNotFoundError:
		return False

#-------------------- OBJECTS --------------------#
notes = [4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25]    # List to store all possible note lengths.
rhythm_players = []    # List to store the rhythm players.

state = "main"
randomization_mode = "static"

#--initialization--#
time_signature = time_signature_class(7, 8)
tempo = tempo_class(120)
rhythm_players.append(rhythm_player_class("aSound.wav"))
rhythm_players.append(rhythm_player_class("aSound.wav"))
rhythm_players.append(rhythm_player_class("aSound.wav", [0, time_signature.measure_length]))
gui = gui_class()

#--------------------- MAIN ----------------------#
gui.init()

while(True):
	command = gui.get_input()
	if(command == "quit"):
		for player in rhythm_players:
			player.stop_playback()
		tempo.stop_slide()
		gui.go_down(11)
		print("\n  Thank you for using my software!\n  - Goodbye\n")
		break
	
	elif(command == "set tempo"):
		gui.set_tempo()
	
	elif(command == "set timesignature"):
		gui.set_timesignature()
	
	elif(command == "set samples"):
		gui.set_samples()

	elif(command == "sample list"):
		gui.sample_list()
	
	elif(command == "start playback"):
		start_time = time.time() + 0.1
		for player in rhythm_players:
			player.start_playback(start_time)
		time.sleep(0.1)
		gui.init()
	
	elif(command == "stop playback"):
		for player in rhythm_players:
			player.stop_playback()
	
	else:
		gui.unknown_command(command)
