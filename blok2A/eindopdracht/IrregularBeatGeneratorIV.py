#!/usr/bin/Python3

#-------------------- IMPORTS --------------------#
import simpleaudio as sa 					# Sample playback module
from threading import Thread 				# Multithreading module
from midiutil import MIDIFile 	 			# Write to midifile module
import pygui								# Terminal Gui module
import time, random, math, os, webbrowser	# Miscellaneous modules

#-------------------- OBJECTS --------------------#
sample_player = []
notelist = [4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25]  # Notevalues as amount of beats.

#-------------------- CLASSES --------------------#
class SamplePlayer(object):
	"""Handles the rhythmic playback of a specified audiofile.

	Plays a 16-bit wavefile according to a pseudo randomly generated rhythm. The rhythm
	generation, randomization and storage are handled by a Rhythm()-object. Global events
	like tempo-syncing, and timesignature information are accessed via a reference to an
	event_Handler() class. Audioplayback is automatically run on a seperate thread.

	Attributes:
		self.events 	: Reference to a global event_handler.
		self.sample 	: Sample name.
		self.audiofile 	: Simpleaudio object to store the wavefile.
		self.rhythm 	: Rhythm generator object.
		self.playing	: Boolean to track if audio is playing.
	"""
	def __init__(self, event_handler, audiofile, grid_type=1):
		global sample_player
		if grid_type < 1 or grid_type > 3:
			raise ValueError("Grid_type must be between 1 and 3, given:{0}".format(grid_type))
		self.events = event_handler			
		self.sample = audiofile
		self.audiofile = sa.WaveObject.from_wave_file(audiofile)
		self.rhythm = Rhythm(event_handler, grid_type)
		self.playing = False

		sample_player.append(self)  # Add itself to a global list for easy access.

	def _play(self):
		timestamp = self.rhythm.buffer.get_timestamp()  # Initial timestamp.
		while(self.playing):
			if(self.events.beats_passed > timestamp):  # Check if the timestamp is passed.
				self.audiofile.play()
				end_of_buf = self.rhythm.buffer.tick()  # tick()-function returns True at end of buffer.
				if(end_of_buf):
					self.rhythm.update()  # Generate more rhythm.
				timestamp = self.rhythm.buffer.get_timestamp()  # Get a new timestamp.
			else:
				time.sleep(0.0005)  # Wait a little as to not overload the processor.

	def start_playback(self):
		self.rhythm.initialize()
		self.playing = True
		Thread(target=self.play,).start()

	def stop_playback(self, midifile_name=None):
		self.playing = False
		if(midifile_name):
			create_midifile(midifile_name)
		self.rhythm.clear()			

	def play_once(self):
		self.audiofile.play()

	#__SETTERS/GETTERS__#
	def set_rhythm_density(self, value):
		global notelist
		if(value < 0 or value > len(notelist - 1)):
			raise ValueError("Value must be between 0 and {0}, given: {1}".format(len(notelist - 1), value))
		self.rhythm.density = value

	def set_note_diversity(self, value):
		if(value < 0 or value > 10):
			raise ValueError("Value must be between 0 and 10, given: {0}".format(value))
		self.rhythm.note_diversity = value

	def set_randomizations(self, value):
		if(value < 0 or value > 2):
			raise ValueError("Value must be between 0 and 2, given: {0}".format(value))
		self.rhythm.randomizations = value


class Rhythm(object):
	"""Generates, randomizes and stores a rhythm.
	
	Pseudo randomly generates a rhythm based on rhythm density, note diversity and a pulsegrid. 
	The pulsegrid keeps track of where the pulses are in the rhythm (points that always contain
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
		self.density 		 : Density of the rhythm. (amount of notes)
		self.note_diversity  : Diversity of notevalues.
		self.randomizations  : Amount of randomizations per itteration.
	"""
	def __init__(self, event_handler, grid_type):
		self.events = event_handler
		self.base_rhythm = [[], []]
		self.buffer = TimestampBuffer(event_handler)
		self.pulse_grid = []
		self.pulse_grid_type = grid_type
		self.density = 0
		self.note_diversity = 0
		self.randomizations = 0

	def _create(self):
		pass

	def _randomize(self):
		"""Applies a user set amount of randomizations to the base rhythm.

		"""

	def initialize(self):
		self.pulse_grid = create_pulse_grid(self.pulse_grid_type)
		self.base_rhythm[0] = self._create()
		self.base_rhythm[1] = notes_to_timestamps(self.base_rhythm[0])

	def update(self):
		if(self.randomizations > 0):  # Check if the base_rhythm should be randomized.
			timestamps_to_add = self._randomize()
		else:
			timestamps_to_add = self.base_rhythm[1]
		self.buffer.add_timestamps(timestamps_to_add)  # Adds new rhythm to the buffer.

	def clear(self):
		self.buffer.reset()

class TimestampBuffer(object):
	"""Simple expandable timestamp buffer.

	Attributes:
		self.buffer 	: List of buffer contents.
		self.read_index : Readposition in the buffer.
		self.offset 	: Offset given to new
	"""
	def __init__(self):
		self.buffer = []
		self.read_index = 0
		self.offset = 0

	def tick(self):  
		"""Updates the read_index.

		Returns:
			True 	: If the end of the buffer is reached.
			False 	: If the above doesn't apply.
		"""
		self.read_index += 1
		if(self.read_index <= len(self.buffer)):  # Check if the end of the buffer is reached.
			return True
		else:
			return False

	def get_timestamp(self):  
		"""Retrieves a timestamp from the buffer."""
		return self.buffer[self.read_index]

	def add_timstamps(self, timestamps):  
		"""Adds a list of timestamps to the buffer.
		
		Args:
			timestamps 	: A list of relative timestamps (meaning a 0 gets interpreted as the
						  value stored in self.offset). The last value in the list gets
						  interpreted as the next offset and won't be added to the buffer.
		"""
		if(len(timestamps) < 2):
			raise IndexError("Timestamps listsize must be at least 2")
		offset = self.offset  # Save offset in a temporary variable
		self.offset = timestamps.pop(-1)  # Set offset for next function-call.
		for timestamp in timestamps:
			self.buffer.append(timestamp + offset)  # Add the timestamps plus a required offset.
		

	def reset(self):
		"""Resets the buffer to its initial state."""
		self.buffer = []
		self.read_index = 0
		self.offset = 0

