#!/usr/bin/Python3

#-------------------- IMPORTS --------------------#
import simpleaudio as sa 					# Sample playback module
from threading import Thread 				# Multithreading module
from midiutil import MIDIFile 	 			# Write to midifile module
import pygui								# Terminal Gui module
import time, random, math, os, webbrowser	# Miscellaneous modules

#-------------------- OBJECTS --------------------#
sample_players = []
notelist = [4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25]  # Notevalues as amount of beats. !NOTE: List must be in strict desending order for the algorithms to work properly!
midi_notes = [36, 38, 42]  # Midinotes used on export.

#-------------------- CLASSES --------------------#
class SamplePlayer(object):
	"""Handles the rhythmic playback of a specified audiofile.

	Plays a 16-bit wavefile according to a pseudo randomly generated rhythm. The rhythm
	generation, randomization and storage are handled by a Rhythm()-object. Global events
	like tempo-syncing, and timesignature information are accessed via a reference to an
	event_Handler() class. Audioplayback is automatically run on a seperate thread.

	Attributes:
		self.events    : Reference to a global event_handler.
		self.sample    : Sample name.
		self.audiofile : Simpleaudio object to store the wavefile.
		self.rhythm    : Rhythm generator object.
		self.playing   : Boolean to track if audio is playing.
	"""
	def __init__(self, event_handler, audiofile, pulse_grid_type=0):
		global sample_player
		self.events = event_handler			
		self.sample = audiofile
		self.audiofile = sa.WaveObject.from_wave_file(audiofile)
		self.rhythm = Rhythm(event_handler, pulse_grid_type)
		self.playing = False

		sample_player.append(self)  # Adds itself to a global list for easy access.

	def _play(self):
		"""Rhythmic playback of the audiofile."""
		timestamp = self.rhythm.buffer.get_timestamp()  # Initial timestamp.
		while(self.playing):
			if(self.events.beats_passed > timestamp):  # Checks if the timestamp is passed.
				self.audiofile.play()
				end_of_buf = self.rhythm.buffer.tick()  # tick()-function returns True at end of buffer.
				if(end_of_buf):
					self.rhythm.update()  # Generates more rhythm.
				timestamp = self.rhythm.buffer.get_timestamp()  # Gets a new timestamp.
			else:
				time.sleep(0.0005)  # Waits a little as to not overload the processor.

	def start_playback(self):
		"""Starts the playback on a seperate thread."""
		self.rhythm.initialize()
		self.playing = True
		Thread(target=self.play,).start()

	def stop_playback(self):
		"""Stops the playback thread.

		Returns:
			The entire generated rhythm.
		"""
		self.playing = False
		rhythm = self.rhythm.buffer.get_rhythm()
		self.rhythm.clear()
		return rhythm		

	def play_once(self):
		"""Plays the audiofile once."""
		self.audiofile.play()

	#__SETTERS/GETTERS__#
	def set_rhythm_density(self, value):
		"""Sets the rhythm-object density.

		Raises:
			ValueError : if the input is not between 0 and one less than the notelists size.
		"""
		global notelist
		if(value < 0 or value > len(notelist - 1)):
			raise ValueError("Value must be between 0 and {0}, given: {1}".format(len(notelist - 1), value))
		self.rhythm.density = value

	def set_note_diversity(self, value):
		"""Sets the rhythm-object note_diversity.
		
		Raises:
			ValueError : if the input is not between 0 and 10.
		"""
		if(value < 0 or value > 10):
			raise ValueError("Value must be between 0 and 10, given: {0}".format(value))
		self.rhythm.note_diversity = value

	def set_randomizations(self, value):
		"""Sets the rhythm-object randomizations.
		
		Raises:
			ValueError : if the input is not between 0 and 2.
		"""
		if(value < 0 or value > 2):
			raise ValueError("Value must be between 0 and 2, given: {0}".format(value))
		self.rhythm.randomizations = value


class Rhythm(object):
	"""Generates, randomizes and stores a rhythm.
	
	Semi-randomly generates a rhythm based on rhythm density, note diversity and a pulse grid. 
	The pulse grid keeps track of where the pulses are in the rhythm (points that always contain
	a note). The density determines the average notevalue and therefore ultimatly the amount of 
	notes in the rhythm. The note diversity determines how much the notevalues may differ from 
	the average.

	When the rhythm is initialzed an one-measure-long base rhythm is created and stored as 
	notevalues and timestamps. The timestamps also get added to the buffer. When the end of the
	buffer is reached, the base_rhythm gets randomized and the resulting timestamps get added
	to the buffer.

	Attributes:
		self.events 		 : Reference to a global event_handler.
		self.base_rhythm 	 : 2D-list to store the base rhythm as notevalues and timestamps.
		self.buffer 		 : Generated rhythm buffer.
		self.pulse_grid 	 : List of pulses in the rhythm.
		self.pulse_grid_type : Determines the pulse_grid generation algorithm.
		self.density 		 : Density of the rhythm (amount of notes).
		self.note_diversity  : Diversity of notevalues.
		self.randomizations  : Amount of randomizations per itteration (rhythm update).
	"""
	def __init__(self, event_handler, pulse_grid_type=0):
		self.events = event_handler
		self.base_rhythm = [[], []]
		self.buffer = TimestampBuffer(event_handler)
		self.pulse_grid = []
		self.pulse_grid_type = grid_type
		self.density = 0
		self.note_diversity = 0
		self.randomizations = 0

	def _create(self):
		"""Generates a new rhtyhm.

		Generates a semi-random list of notes with respect to a predetermined grid of pulses.

		Retruns:
			list of notevalues.
		"""
		global notelist
		note_probabilities = create_note_probabilities(len(notelist), self.density, self.note_diversity)
		rhythm = []
		start = self.pulse_grid[0]
		rhythm_length = start  # Sum of the notevalues in the rhythm.
		for pulse in self.pulse_grid:
			while(rhythm_length < pulse):
				note = pick_item(notelist, note_probabilities)  # picks a new note.
				if(note + rhythm_length > pulse):  # Checks if the picked notevalue exceeds the pulse.
					note = pulse - rhythm_length  # Adjust notevalue accordingly.
				rhythm.append(note)
				rhythm_length += note
		return rhythm

	def _randomize(self):
		"""Randomizes the base rhythm.

		Applies a user-set amount of randomizations to the base rhythm, using one of two
		possible modi. Static mode doesn't alter the pulses in the grid, nor the original 
		base rhythm. Evolve (evolutionairy) mode discards the pulses and overwrites the
		original base rhythm, which over time will result in the transition to a completely
		different rhythm.

		Every time an index is picked, it might result in a faulty randomization. After picking
		three false indecis, no randomization gets applied. This adds on some extra randomness.

		Returns:
			A list of (altered) timestamps.
		"""
		global notelist
		randomizations = self.randomizations  # Number of randomizations to be applied.
		if(self.events.randomization_mode == "static"):  # Checks the randomization mode.
			rhythm_rand = self.base_rhythm.copy()
			while(randomizations > 0):
				option = random.randint(0,2)  # Picks a randomization type.
				tries = 0

				if(option == 0):  # Swaps two consecutive notes.
					index = random.randint(0, len(rhythm_rand[0])-2)  # Picks an index, excluding the last.
					while(tries < 3):
						if(rhythm_rand[1][index + 1] not in self.pulse_grid and rhythm_rand[0][index] != rhythm_rand[0][index + 1]):  # Checks if the index is valid.
							swap_notes(rhythm_rand[0], index)  # Swaps two notes.
						else:
							index = random.randint(0, len(rhythm_rand[0])-2)  # Picks a new index.
							tries += 1

				elif(option == 1):  # Glues two consecutive notes together.
					index = random.randint(0, len(rhythm_rand[0])-2)  # Picks an index, excluding the last.
					while(tries < 3):
						if(rhythm_rand[1][index + 1] not in self.pulse_grid):  # Checks if the index is valid.
							glue_notes(rhythm_rand[0], index)  # Glues two notes.
						else:
							index = random.randint(0, len(rhythm_rand[0])-2)  # Picks a new index.
							tries += 1

				elif(option == 2):  # Splits a note into two smaller notes. 
					index = random.randint(0, len(rhythm_rand[0])-1)  # Picks an index.
					while(tries < 3):
						if(rhythm_rand[0][index] != notelist[-1]):  # Checks if the index is valid.
							split_notes(rhythm_rand[0], index)  # Splits a note.
						else:
							index = random.randint(0, len(rhythm_rand[0])-1)  # Picks a new index.
							tries += 1

				rhythm_rand[1] = notes_to_timestamps(rhythm_rand[0], self.pulse_grid[0])  
			return rhythm_rand[1]

		if(self.events.randomization_mode == "evolve"):  # Checks the randomization mode.
			while(randomizations > 0):
				option = random.randint(0,2)  # Picks a randomization type.
				tries = 0

				if(option == 0):  # Swaps two consecutive notes.
					index = random.randint(0, len(self.base_rhythm[0])-2)  # Picks an index, excluding the last.
					while(tries < 3):
						if(self.base_rhythm[0][index] != self.base_rhythm[0][index + 1]):  # Checks if the index is valid.
							swap_notes(self.base_rhythm[0], index)  # Swaps two notes.
						else:
							index = random.randint(0, len(self.base_rhythm[0])-2)  # Picks a new index.
							tries += 1

				elif(option == 1):  # Glues two consecutive notes together.
					index = random.randint(0, len(self.base_rhythm[0])-2)  # Picks an index, excluding the last.
					glue_notes(self.base_rhythm[0], index)  # Glues two notes.

				elif(option == 2):  # Splits a note into two smaller notes. 
					index = random.randint(0, len(self.base_rhythm[0])-1)  # Picks an index.
					while(tries < 3):
						if(self.base_rhythm[0][index] != notelist[-1]):  # Checks if the index is valid.
							split_notes(self.base_rhythm[0], index)  # Splits a note.
						else:
							index = random.randint(0, len(self.base_rhythm[0])-1)  # Picks a new index.
							tries += 1

				self.base_rhythm[1] = notes_to_timestamps(self.base_rhythm[0], self.pulse_grid[0])
			return self.base_rhythm[1]

	def initialize(self, new_grid=True):
		"""Initialize the rhythm.

		Args:
			new_grid : Determines if a new pulsegrid should be generated.
		"""
		if(new_grid):
			self.pulse_grid = create_pulse_grid(events.time_signature.measure_length, self.pulse_grid_type)
		self.base_rhythm[0] = self._create()
		self.base_rhythm[1] = notes_to_timestamps(self.base_rhythm[0], self.pulse_grid[0])
		self.buffer.add_timestamps(self.base_rhythm[1])

	def update(self):
		"""Add a new part to the buffer."""
		if(self.randomizations > 0):  # Checks if the base_rhythm should be randomized.
			timestamps_to_add = self._randomize()
		else:
			timestamps_to_add = self.base_rhythm[1]
		self.buffer.add_timestamps(timestamps_to_add)  # Adds new rhythm to the buffer.

	def clear(self):
		"""Reset the rhythm to its default state."""
		self.pulse_grid = []
		self.base_rhythm = [[], []]
		self.buffer.reset()

class TimestampBuffer(object):
	"""Simple expandable timestamp buffer.

	Attributes:
		self.events		: Reference to a global event_handler.
		self.buffer 	: List of buffer contents.
		self.read_index : Readposition in the buffer.
		self.offset 	: Offset given to new
	"""
	def __init__(self, event_handler):
		self.events = event_handler
		self.buffer = []
		self.read_index = 0
		self.offset = 0

	def tick(self):  
		"""Updates the read_index.

		Returns:
			True  : If the end of the buffer is reached.
			False : If the above doesn't apply.
		"""
		self.read_index += 1
		if(self.read_index <= len(self.buffer)):  # Checks if the end of the buffer is reached.
			return True
		else:
			return False

	def get_timestamp(self):  
		"""Retrieves a timestamp from the buffer."""
		return self.buffer[self.read_index]

	def add_timstamps(self, timestamps):  
		"""Adds a list of timestamps to the buffer.

		Args:
			timestamps : A list of positive, relative timestamps (meaning a 0 gets interpreted
						 as the value stored in self.offset) with a size of at least 1. The
						 last value in the list gets interpreted as the next offset and won't 
						 be added to the buffer.
		
		Raises:
			IndexError : If the inputed list contains fewer than 2 elements.
			ValueError : If the inputed list contains negative values.
		"""
		if(len(timestamps) < 2):
			raise IndexError("Timestamps listsize must be at least 2")
		for value in timestamps:
			if(value < 0):
				raise ValueError("Timestamps list must not contain negative values")

		offset = self.offset  # Saves offset in a temporary variable
		self.offset = timestamps.pop(-1)  # Sets offset for next function-call.
		for timestamp in timestamps:
			adjusted_timestamp = timestamp * 4 / events.time_signature.beat_length + offset  # Adjust the timestamp according to global parameters and an offset.
			self.buffer.append(adjusted_timestamp)  # Adds the adjusted timestamp.
	
	def get_rhythm(self):
		"""Returns the entire buffer contents"""
		return self.buffer

	def reset(self):
		"""Resets the buffer to its default state."""
		self.buffer = []
		self.read_index = 0
		self.offset = 0

#------------------- FUNCTIONS -------------------#
def create_note_probabilities(length, centre, spread):
	"""Creates a list of related probabilities.
	
	Creates a list of stacked probabilities according to the following function:
	1/n^2, 2/n^2, 3/n^2, ..., (n-1)/n^2, n/n^2, (n-1)/n^2, ..., 3/n^2, 2/n^2, 1/n^2.
	All the terms in this series will always add up to 1. If the length of the series exceed
	the desired length, all out of bound terms get distributed evenly over the remaining terms, 
	to still get a sum of 1 in the end. The final list will be stacked, meaning a list like: 
	[0.2, 0.3, 0.45, 0.05] gets turned into [0.2, 0.5, 0.95, 1].

	Args:
		length : Desired list length.
		centre : Index of the highest probability (n/n^2) (Must be smaller than the length). 
		spread : Amount of non-zero probabilities next to the centre (n-1).

	Raises:
		ValueError : If the centre value is not between 0 and the length.

	Returns:
		List of stacked probabilities.
	"""
	if(centre < 0 or centre >= length):
		raise ValueError("Centre must be between 0 and lenght ({0}), given: {1}".format(lenght, centre))

	probability_series = []  # Function as described in the docstring.
	n = spread + 1
	k = 1													
	while(k <= n):											
		probability_series.append(round(k/(n*n), 4))	   
		k += 1												
	k -= 2													
	while(k > 0):											
		probability_series.append(round(k/(n*n), 4))
		k -= 1

	out_of_bounds = 0  # Sum of out of bound terms.									
	if(centre - spread < 0):  # Checks the left bound with respect to the centre index.
		for i in range(0, spread - centre):						
			out_of_bounds += probability_series.pop(0)
	if(centre + spread > length - 1):  # Checks the right bound with respect to the centre index.						
		for i in range(0, spread):
			out_of_bounds += probability_series.pop(-1)	
	for i, value in enumerate(probability_series):  # Distributes the out of bound value evenly over the remaining terms.
		probability_series[i] = value + out_of_bounds/len(probability_series)

	probabilities = [0]*length  # Initializes a list of the desired length.
	for i, value in enumerate(probability_series):  # The code inisde this loop maps the probability series to the correct indecis (according to the centre index).
		if(centre - spread >= 0):													
			probabilities[i + centre - spread] = value
		else:
			probabilities[i] = value

	for i, value in enumerate(probabilities):  # The code inside this for-loop stacks the noteProbabilities.
		if(i > 0):														
			probabilities[i] = round(value + probabilities[i-1], 4)
		else:
			probabilities[i] = round(value, 4)
	
	return probabilities

def create_pulse_grid(length, grid_type):
	"""Generates a grid of pulses.
	
	Generates a list of timestamps (designated as pulses) of a set length, using one of three
	algorithms. For grid lengths bigger than 3, type 1 and 2 start with [0, 3] and [1, 4] 
	respectively, after which timestamps of length 2 or 4 are added untill the desired length
	is reached. For a grid length of exactly 3, a type 2 grid the resulting list will look like 
	[1, 3]. A type 3 grid will always result in a grid of the form [0, length]. The first and 
	last timestamp in the grid will mark the startpoint end endpoint of the rhythm.

	Args:
		length 	  : Desired grid_length (must be bigger than or equal to 3).
		grid_type : Determines the algorithm to be implemented (must be between 0 and 2).
	
	Raises:
		ValueError : If length is smaller than 3.
		ValueError : If grid_type is not between 0 and 2.
	
	Returns:
		List of timestamps (to be used as a pulse grid).
	"""
	if(length < 3):
		raise ValueError("Length must be at least 3, given:{0}".format(length))
	if(grid_type < 0 or grid_type > 2):
		raise ValueError("Grid_type must be between 0 and 2, given:{0}".format(grid_type))
	
	pulse_grid = []  # Initial pulse.
	grid_length = 0  # Sum of the pulses in the grid.

	if(grid_type == 0):  # Switch to determine the algorithm.
		pulse_grid.append(0, 3)
		grid_length = 3
	elif(grid_type == 1):
		pulse_grid.append(1)
		grid_length = 1
		if(length > 3):
			pulse_grid.append(4)
			pulse_grid = 4
	elif(grid_type == 2):
		pulse_grid.append(0, length)
		grid_length = length

	while(grid_length < length):  # Keeps adding pulses until the desired length is reached.
		if(length - grid_length >= 4):
			pulse = random.randint(1, 2) * 2  # Adds a pulse of length 2 or 4.
		else:
			pulse = length - grid_length  # Makes sure the grid length doesn't exceed the desired length.	
		pulse_grid.append(pulse + pulse_grid[-1])
		grid_length += pulse
	
	return pulse_grid

def notes_to_timestamps(notes, startvalue):
	"""Converts notevalues to timestamps.
	
	Args:
		notes 	   : Notevalues to be converted
		startvalue : First timestamp value.
	"""
	timestamps = [startvalue]
	for note in notes:
		timestamps.append(timestamps[-1] + note)
	return timestamps

def swap_notes(notes, index):
	"""Swaps two notes."""
	temp = notes[index]
	notes[index] = notes[index + 1]
	notes[index + 1] = temp

def glue_notes(notes, index):
	"""Glues two consecutive notes together."""
	notes[index] = notes[index] + notes[index + 1]
	del notes[index + 1]

def split_notes(notes, index):  
	"""Splits a note into two smaller notes."""
	global notelist
	note = notes[index]
	note1 = note * 0.5
	note2 = note1

	if note1 % notelist[-1] != 0:  # Checks sure the splitted notes are a multiple of the smallest notevalue.
		note1 += notelist[-1] * 0.5  # Adjusts the notevalue to be a multiple of the smallest notevalue.
		note2 -= notelist[-1] * 0.5  #                              ''

	notes[index] = note1
	notes.insert(index + 1, note2)

def create_midifile(name, tempo_events, time_signature_events, rhythms, midi_notes):
	"""Creates a midifile and saves it in the resources/saves/ directory.
	
	Args:
		name 				  : name of the midifile.
		tempo.events 		  : 2D-list of tempo changes with corresponding timestamps.
		time_signature_events : 2D-list of timesignature changes with corresponding timestamps.
		rhythms 			  : 2D-list of all the generated rhythms.
		midi_notes 			  : midinotevalue used per rhythm on export.
	"""
	filename = 'resources/saves/{0}.mid'.format(name)
	midifile = MIDIFile(1)    # Midifile with 1 track.
	for event in tempo_events:    # Add tempo events.
		midifile.addTempo(0, event[0], event[1])
	for event in time_signature_events:    # Add timesignature events.
		midifile.addTimeSignature(0, event[0], event[1], event[2], 24)
	for i, rhythm in enumerate(rhythms):   # Add note events.
		for timestamp in rhythm:
			midifile.addNote(0, 0, midi_notes[i], timestamp, 0.25, 100)
	with open(filename, 'wb') as output_file:    # Open/create midifile with desired name.
		midifile.writeFile(output_file)    # Write to midifile.



