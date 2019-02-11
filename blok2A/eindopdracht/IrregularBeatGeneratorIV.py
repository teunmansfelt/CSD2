
#-------------------- IMPORTS --------------------#
import simpleaudio as sa 					# Sample playback module
import threading as t 						# Multithreading module
from midiutil import MIDIFile 	 			# Write to midifile module
import pygui								# Terminal Gui module
import time, random, math, os, webbrowser	# Miscellaneous modules

#-------------------- OBJECTS --------------------#
sample_player = []


#-------------------- CLASSES --------------------#
class sample_player_class:
	"""
	Handles the rhythmic playback of a specified audiofile.
	The playback is threaded, so it won't interfere with code on the main thread.

	self.sample 		: Stores the samplename.
	self.audiofile 		: Object which stores the samplefile. (only 16-bit .wav)
	pulse_grid			: Determines whether or not the rhythm generation/randomization takes 
	                      rhythmic pulses into account. (0 or 1)
	self.rhythm 		: Object to store and handle rhythm generation/randomization.
	"""
	def __init__(self, audiofile, pulse_grid=1):
		global sample_player
		self.sample = audiofile
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/{0}".format(audiofile))
		self.rhythm = rhythm_class()

		sample_player.append([self, pulse_grid])

	def set_sample(self, audiofile): # Sets the sample.
		self.sample = audiofile
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/{0}".format(audiofile))

	def _play(self): # Sample playback function.
		"""

		NOTE: This function should not be called manually, but only through the start_playback() function.
		"""
		pass

	def start_playback(self):
		"""
		"""
		pass

	def play_once(self): # Play the sample once.
		self.audiofile.play()


#------------------- FUNCTIONS -------------------#

#--------------------- MAIN ----------------------#
pygui.init()
pygui.edit_mode() # !TEMPORARY
input() # !TEMPORARY
exit() # !TEMPORARY