#-------------------- IMPORTS --------------------#
import simpleaudio as sa
import threading as t
import curses as c
import time, random, os, webbrowser

#--------------------- SETUP ---------------------#

#-------------------- CLASSES --------------------#
class rhythm_player_class:
	def __init__(self, audiofile, custom_grid=None):
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/{0}".format(audiofile))
		self.rhythm = rhythm_class(custom_grid)

	def play(self, start_time):
		timestamp = self.rhythm.get_timestamp()
		beat = 0
		while(start_time - time.time() > 0):
			time.sleep(0.0005)
		reference_time = time.time()
		while(self.playing):
			if(beat >= timestamp):
				self.audiofile.play()
				timestamp = self.rhythm.get_timestamp()
				if(self.rhythm.rhythm_index >= len(self.rhythm.rhythm)):
					self.rhythm.add_timestamps()
			else:
				time.sleep(0.0005)
				beat += (time.time() - reference_time) * tempo.bps
				reference_time = time.time()

	def play_once(self):
		self.audiofile.play()

	def start_playback(self, start_time):
		self.playing = True
		t.Thread(target=self.play, args=(start_time,)).start()
		if(self.rhythm.randomization > 0):
			self.rhythm.randomize()

	def stop_playback(self):
		self.playing = False

class rhythm_class:
	def __init__(self, custom_grid):
		self.rhythm_density = 5
		self.note_diversity = 1
		self.randomization = 2		
		self.reset(custom_grid)

	def create_rhythm(self):
		note_probability_distribution = create_probability_distribution(len(notes), self.rhythm_density, self.note_diversity)
		rhythm = []
		rhythm_length = 0

		for pulse in self.pulse_grid[1:len(self.pulse_grid)]:
			while(rhythm_length < pulse):
				note = pick_item(notes, note_probability_distribution)
				if(note + rhythm_length > pulse):
					note = pulse - rhythm_length
				rhythm_length += note
				rhythm.append(note)
		return rhythm

	def randomize(self): # Randomizes the notes
		randomizations = self.randomization
		tries = 0
		if(randomization_mode == "static"):
			while(randomizations > 0):											# The self.randomizations sets the amount of randomizations.
				option = random.randint(0,2)									# Determines what type of randomization should be applied.

				if(option == 0):
					index = random.randint(0, len(self.notes)-2)				# Picks a random element from the notes, excluding the last element.									
					while(tries < 3):											
						if(self.timestamps[index] in self.pulse_grid or self.notes[index] == self.notes[index + 1]):
							index = random.randint(0, len(self.notes)-2)
							tries += 1
						else:
							break					 
					notes_to_add = swap_notes(self.notes, index)					# Swaps two consecutive notes and stores the outputted list as a copy. 

				elif(option == 1):
					index = random.randint(0, len(self.notes)-2)				# Picks a random element from the notes, excluding the last element.										
					while(tries < 3):												
						if(self.timestamps[index + 1] in self.pulse_grid):
							index = random.randint(0, len(self.notes)-2)
							tries += 1
						else:
							break
					notes_to_add = glue_notes(self.notes, index)					# Glues two consecutive notes and stores the outputted list as a copy. 

				elif(option == 2):
					index = random.randint(0, len(self.notes)-1)				# Picks a random element from the notes.
					while(self.notes[index] == 0.25 and tries < 3):				# This while-loop makes sure the note is bigger than 0.25.
						index = random.randint(0, len(self.notes)-1)
						tries += 1
					notes_to_add = split_notes(self.notes, index)				# Splits two consecutive notes and stores the outputted list as a copy. 
				randomizations -= 1
			self.timestamps_to_add = notes_to_timestamps(notes_to_add)

		elif(randomization_mode == "evolve"):
			while(randomizations > 0):									# The self.randomizations sets the amount of randomizations.
				option = random.randint(0,2)							# Determines what type of randomization should be applied.

				if(option == 0):
					index1 = random.randint(0, len(self.notes)-2)		# Picks a random element from the notes, excluding the last element.
					self.notes = swap_notes(self.notes, index1, index2)	# Swaps two random notes

				elif(option == 1):
					index = random.randint(0, len(self.notes)-2)		# Picks a random element from the notes, excluding the last element.
					self.notes = glue_notes(self.notes, index)			# Glues two notes together.

				elif(option == 2):
					index = random.randint(0, len(self.notes)-1)		# Picks a random element from the notes.
					while(self.notes[index1] == 0.25 and tries < 3):	# This while-loop makes sure the note is bigger than 0.25.
						index = random.randint(0, len(self.notes)-1)
					self.notes = split_notes(self.notes, index)			# Splits a note.
				randomizations -= 1
			self.timestamps = notes_to_timestamps(self.notes)
			self.timestamps_to_add = self.timestamps.copy()

	def add_timestamps(self):
		for timestamp in self.timestamps_to_add:
			self.rhythm.append(timestamp + time_signature.measure_length * self.amount_of_measures)
		self.amount_of_measures += 1
		if(self.randomization > 0):
			self.randomize()

	def get_timestamp(self):
		timestamp = self.rhythm[self.rhythm_index]
		self.rhythm_index += 1
		return timestamp

	def set_rhtyhm_lists(self, custom_grid=None):
		if(custom_grid):
			self.pulse_grid = custom_grid
		else:
			self.pulse_grid = create_pulse_grid()
		self.notes = self.create_rhythm()
		self.timestamps = notes_to_timestamps(self.notes)
		self.timestamps_to_add = self.timestamps.copy()

	def reset(self, custom_grid):
		self.rhythm_index = 0
		self.amount_of_measures = 0
		self.set_rhtyhm_lists(custom_grid)
		self.rhythm = []
		self.add_timestamps()
		
class time_signature_class:
	def __init__(self, value):
		self.set(value)

	def set(self, value):
		self.value = value
		self.measure_length = int(value.split('/')[0])
		self.beat_length = int(value.split('/')[1])

		for i, player in enumerate(rhythm_players):
			if(i == 2):
				player.rhythm.set_rhtyhm_lists([0, self.measure_length])
			else:
				player.rhythm.set_rhtyhm_lists()

class tempo_class:
	def __init__(self, value):
		self.value = value
		self.bps = value / 60

	def set(self, value):
		self.value = value
		self.bps = value / 60

	def ramp(self, destination, duration):
		start = self.value
		increment = (destination - start) / duration
		for i in range(0, duration):
			self.value += increment
			self.bps = self.value / 60
			if not self.slide:
				return
			time.sleep(0.001)
		self.value = destination
		self.bps = self.value / 60
		

	def slide(self, destination, duration):
		self.slide = True
		t.Thread(target=self.ramp, args=(destination, duration)).start()

	def stopSlide(self):
		self.slide = False

#------------------- FUNCTIONS -------------------#
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
	if(centre - spread < 0):										# Checks if any elements from the probabilityDistribution list would exceed the left bound of the noteProbability list after mapping.
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

def create_pulse_grid():
	pulse_grid = [0, 3]
	grid_length = 3

	while(grid_length < time_signature.measure_length):
		if(time_signature.measure_length - grid_length >= 4):
			pulse = random.randint(1, 2) * 2
		else:
			pulse = time_signature.measure_length - grid_length
		
		pulse_grid.append(pulse + pulse_grid[-1])
		grid_length += pulse

	return pulse_grid

def pick_item(items, probabilities): # Returns a note from a list of possible notelengths according to probability
	x = round(random.uniform(0, 0.9999), 4)		
	for i, chance in enumerate(probabilities):	# The code inside this for-loop picks a note from the notes list at the index
		if x < chance:							# at which the probability is bigger than the randomly generated number.
			return items[i]

def notes_to_timestamps(notes):
	timestamps = [0]
	for i, note in enumerate(notes):
		timestamps.append(timestamps[i] + note)
	timestamps.pop(-1)
	return timestamps

#--randomization--#
def swap_notes(notes, index): # Swaps two notes
	notes_copy = notes.copy()
	temp = notes_copy[index]
	notes_copy[index] = notes_copy[index + 1]
	notes_copy[index + 1] = temp
	return notes_copy

def glue_notes(notes, index): # Glues two consecutive notes together.
	notes_copy = notes.copy()
	notes_copy[index] = notes_copy[index] + notes_copy[index + 1]
	del notes_copy[index + 1]
	return notes_copy

def split_notes(notes, index): # Splits a note into two smaller notes.
	notes_copy = notes.copy()
	note = notes_copy[index]
	note1 = note * 0.5
	note2 = note1

	if note % 0.5 != 0: # Makes sure the outputted notes are a multiple of 0.25.
		note1 += 0.125
		note2 -= 0.125

	notes_copy[index] = note1
	notes_copy.insert(index + 1, note2)
	return notes_copy

#-------------------- OBJECTS --------------------#
notes = [4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25]
rhythm_players = []

state = "main"
randomization_mode = "static"

#--------------------- MAIN ----------------------#
time_signature = time_signature_class("7/4")
tempo = tempo_class(120)

rhythm_players.append(rhythm_player_class("aSound.wav", [0, time_signature.measure_length]))

start_time = time.time() + 1

for player in rhythm_players:
	player.start_playback(start_time)


