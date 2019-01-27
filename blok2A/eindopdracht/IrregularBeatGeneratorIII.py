#-------------------- IMPORTS --------------------#
import simpleaudio as sa 					# Sample playback 
import threading as t 						# Multithreading module
from midiutil import MIDIFile 	 			# Write to midifile
import time, random, math, os, webbrowser	# Miscellaneous libraries

#-------------------- CLASSES --------------------#
class rhythm_player_class:  # Class to handle the playback of a rhythm.
	def __init__(self, audiofile, custom_grid=None):
		self.sample = audiofile
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/{0}".format(audiofile))    # Sample (playback) object.
		self.rhythm = rhythm_class()    # Object to handle rhythm generation and rhythm storage.
		self.pulse_grid = custom_grid
		self.beat = 0    # Variable to keep track of how many beats have passed.

	def set_sample(self, audiofile):
		self.sample = audiofile
		self.audiofile = sa.WaveObject.from_wave_file("resources/audioFiles/{0}".format(audiofile))

	def play(self, start_time):    # sample playback function.
		timestamp = self.rhythm.get_timestamp()   
		while(start_time - time.time() > 0):    # Check if the start time is passed (makes sure all rhythms play in sync).
			time.sleep(0.0005)
		reference_time = time.time()    # Set a reference time.
		while(self.playing):    # Keep looping until playback is stopped.
			if(self.beat >= timestamp):    # Check if the timestamp is passed.
				self.audiofile.play()
				timestamp = self.rhythm.get_timestamp()    # Retrieve a new timestamp.
				if(self.rhythm.rhythm_index >= len(self.rhythm.rhythm)):    # Check if the end of the rhythm is reached.
					self.rhythm.add_timestamps()    # Add the buffered timestamps to the rhythm.
			else:
				time.sleep(0.0005)    # Wait a bit (prevents cpu overload).
				self.beat += (time.time() - reference_time) * tempo.bps    # Add the amount of beats passed since last check.
				reference_time = time.time()    # Reset the reference time.

	def play_once(self):
		self.audiofile.play()

	def start_playback(self, start_time):
		self.rhythm.reset(self.pulse_grid)
		self.playing = True     # Keep the playback going.
		t.Thread(target=self.play, args=(start_time,)).start()    # Start a thread to handle the playback function.
		if(self.rhythm.randomization > 0):    # Check if the rhythm should be randomized.
			self.rhythm.timestamps_to_add = []
			self.rhythm.randomize()    # Initial rhythm randomization.

	def stop_playback(self):
		self.playing = False    # Break the loop in the playback function. (kills the playback thread)
		self.beat = 0

	def set_rhythm_density(self, value):
		self.rhythm.rhythm_density = value
		if(gui.playback):
			self.rhythm.create_rhythm()
			self.rhythm.timestamps = notes_to_timestamps(self.rhythm.notes)
			self.rhythm.timestamps_to_add = self.rhythm.timestamps.copy()

	def set_note_diversity(self, value):
		self.rhythm.note_diversity = value
		if(gui.playback):
			self.rhythm.create_rhythm()
			self.rhythm.timestamps = notes_to_timestamps(self.rhythm.notes)
			self.rhythm.timestamps_to_add = self.rhythm.timestamps.copy()

	def set_randomization(self, value):
		self.rhythm.randomization = value

class rhythm_class:  # Class to handle rhythm generation and rhythm storage.
	def __init__(self):
		self.rhythm_density = 4    # Variable to set the rhythm density.
		self.note_diversity = 2    # Variable to set the diversity in note_lengths.
		self.randomization = 1	   # Variable to set the number of randomizations.

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
				timestamp_ = timestamp * 4 / time_signature.beat_length    # Adjust the timestamp according to the beat_length.
				self.rhythm.append(timestamp_ + offset)    # Add the timestamp + an offset as a result of the measure number.
		except IndexError:
			for timestamp in self.timestamps_to_add:
				timestamp_ = timestamp * 4 / time_signature.beat_length    # Adjust the timestamp according to the beat_length.
				self.rhythm.append(timestamp_)    # Add the timestamp + the offset as a result of the measure number.
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
		self.measure_length = num_of_pulses    # Amount of beats in a bar.
		self.beat_length = pulse_length    # Duration of a single beat.
		self.events = [[0, self.measure_length, int(math.log(self.beat_length,2))]]
		self.value = "{0}/{1}".format(num_of_pulses, pulse_length)

	def set(self, num_of_pulses, pulse_length):
		self.measure_length = num_of_pulses
		self.beat_length = pulse_length
		if(gui.playback):
			self.events.append([rhythm_players[0].rhythm.rhythm[-1], self.measure_length, int(math.log(self.beat_length,2))])
		else:
			self.reset_events(				)
		self.value = "{0}/{1}".format(num_of_pulses, pulse_length)

		for i, player in enumerate(rhythm_players):    # Regenerate the rhythms of every rhythm player.
			if(i == 2):
				player.rhythm.set_rhythm_lists([0, self.measure_length])
			else:
				player.rhythm.set_rhythm_lists()

	def reset_events(self):
		self.events = [[0, self.measure_length, int(math.log(self.beat_length,2))]]

class tempo_class:  # Class to handle the tempo.
	def __init__(self, value):
		self.value = value    # Tempo in beats per minute.
		self.bps = value / 60    # Beats per second.
		self.events = [[0, self.value]]

	def set(self, value):
		self.value = value
		self.bps = value / 60
		if(gui.playback):
			self.events.append([rhythm_players[0].beat, self.value])
		else:
			self.reset_events()

	def ramp(self, destination, duration):    # Function to make the tempo slide.
		self.events.append([rhythm_players[0].beat, destination])
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

	def reset_events(self):
		self.events = [[0, self.value]]

class gui_class:  # Class to handle the user interface.
	def __init__(self):
		self.bar = "_"
		self.line = 0    # Variable to keep track of which line the curser is on.
		self.playback = False    # Boolean to check if playback has started.

	def init(self):    # Initialize the gui.	
		print("\nIrregular Beat Generator III   -   by: Teun Mansfelt")
		print("{0}\noverview:".format(self.bar*53))
		print("  Time signature     : {0}\n  Tempo              : {1}\n  Randomization mode : {2}".format(time_signature.value, tempo.value, randomization_mode))
		for i, player in enumerate(rhythm_players):
			print("\n  Layer{0}:\n  - Sample         : {1}\n  - Rhythm density : {2}\n  - Note diversity : {3}\n  - Randomization  : {4}"
			.format(i+1, player.sample, player.rhythm.rhythm_density, player.rhythm.note_diversity, player.rhythm.randomization)) 
		print("{0}\ncommand execution:\n".format(self.bar*53))

	def go_up(self, x, mode=None):    # Make the curser go up x lines.
		for i in range(0, x):
			print("\033[F", end="")    # Go up a line
			if(mode == "delete"):
				print("\033[K", end="")    # Clear up a line

	def go_down(self, x):    # Make the curser go down x lines.
		for i in range(0, x):
			print("\033[B", end="")    # Go down a line

	def get_input(self):    # Handle user input.
		self.go_down(13 - self.line)    # Go to the command line.
		print("\033[K", end="")
		self.go_up(2)
		command = input("{0}\ncommand line:\n  >>> ".format(self.bar*53))    # Ask for usser input.
		self.go_up(3)
		self.go_up(11, "delete")    # Clear previous command.
		self.line = 0
		return command

	def unknown_command(self, command):    # Proces unknown user input.
		print("!! Unknown command : '{0}'".format(command))
		self.line += 1

	def set_tempo(self):    # Set or slide the tempo.
		print("\n  - Duration: ")
		self.go_up(2)
		value = -1	
		self.line += 1
		while(value == -1):    # Keep looping until a valid input is given.
			self.line -= 1
			print("\033[K", end="")
			value = input("  - Value: ")    # Ask for usser input.
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

		duration = input("  - Duration: ")    # Ask for usser input.
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
		self.go_up(27)
		print("  Tempo              : {0}".format(value))
		self.line -= 24

	def set_timesignature(self):    # Set the time signature.
		print("\n  - Pulse length:")
		self.go_up(2)
		value1 = -1
		self.line += 1
		while(value1 == -1):    # Keep looping until a valid input is given.
			self.line -= 1
			print("\033[K", end="")
			value1 = input("  - Number of pulses: ")    # Ask for usser input.
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
		while(value2 == -1):    # Keep looping until a valid input is given.
			self.line -= 1
			print("\033[K", end="")
			value2 = input("  - Pulse length: ")    # Ask for usser input.
			self.line += 1
			if(value2 == "exit"):    # Exit the loop.
				return
			try:
				value2 = int(value2)    # Make sure the input is an integer.
				if(value2 < 1):    # Check the bounds.
					print("\n\033[K", end="!! Minimum pulse length : 1.")
					self.go_up(2)
					value2 = -1
				if(not math.log(value2, 2).is_integer()):    # Make sure the input is a power of 2.
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
		self.go_up(28)
		print("  Time signature     : {0}".format(time_signature.value))
		self.line -= 25

	def set_samples(self):    # Set the audiofiles used for playback.
		self.sample_list = []    # Initialize a list for all available samples.
		for root, dirs, files in os.walk("resources/audioFiles"):    # Loop throu the files in de audiofiles directory.
			for file in files:
				if(file.endswith(".wav")):    # Check if the file is a '.wav' file.
					self.sample_list.append(file)    # Add the file to the list.
		num_of_pages = math.ceil(len(self.sample_list) / 8)    # Calculate the number of needed pages.
		self.show_sample_page(1, num_of_pages)    # Display the first page.

		print("\n  - Sample 2 :")
		print("  - Sample 3 :")
		self.go_up(3)
		samples = []

		for i, player in enumerate(rhythm_players):    # Loop through all rhythm players.
			sample = None
			self.line += 1
			while(True):    # Keep looping until a valid input is given.
				self.line -= 1
				print("\033[K", end="")
				sample = input("  - Sample {0} : ".format(i + 1))
				self.line += 1
				if(sample == "exit"):    # Exit the loop.
					self.go_down(25 - self.line)
					self.go_up(13, "delete")
					self.go_up(12 - self.line)
					return
				elif(sample == ""):    # Skip this element.
					if(i == 2):    # Clear the terminal after the last rhythm player.
						self.go_down(25 - self.line)
						self.go_up(13, "delete")
						self.go_up(12 - self.line)
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
					self.go_up(20 - 5 * i)
					print("  - Sample         : {0}".format(sample))
					self.go_down(22 - 6 * i)
					print("\033[K", end="Sample {0} set succesfully.".format(i + 1))
					self.go_up(3 - i)
					if(i == 2):    # Clear the terminal after the last rhythm player.
						self.go_down(25 - self.line)
						self.go_up(13, "delete")
						self.go_up(12 - self.line)
					break
				else:
					self.go_down(3 - i)
					print("\033[K", end="!! Invalid sample : {0}".format(sample))
					self.go_up(4 - i)

	def edit_layer(self, layer):    # Sets the parameters of a rhythm player.
		try:
			layer = int(layer)    # Make sure the layer is valid.
			if(layer < 1 or layer > 3):
				int('a')
		except ValueError:
			print("!! Invalid layer : {0}".format(layer))
			return

		print("\n  - Note diversity :")
		print("  - Randomization  :")
		self.go_up(3)

		parameters = [["Rhythm density", len(notes) - 1, "set_rhythm_density({0})"], # List to store parameter names, bounds and function setters.
					  ["Note diversity", 100, "set_note_diversity({0})"], 
					  ["Randomization " , 2, "set_randomization({0})"]]

		for i in range(0, 3):
			value = -1
			self.line += 1
			while(value == -1):    # Keep looping until a valid input is given.
				self.line -= 1
				print("\033[K", end="")
				value = input("  - {0} : ".format(parameters[i][0]))    # Ask for usser input.
				self.line += 1
				if(value == "exit"):    # Exit the loop.
					return
				if(value == ""):    # Skip this element.
					break
				try:
					value = int(value)    # Make sure the input is an integer.
					if(value < 0 or value > parameters[i][1]):    # Check the bounds.
						self.go_down(3)
						print("!! {0} can range from 0 to {1}".format(parameters[i][0], parameters[i][1]))
						self.go_up(5)
						value = -1
				except ValueError:
					self.go_down(4 - self.line)
					print("!! {0} must be an integer.".format(parameters[i][0]))
					self.go_up(6 - self.line)
					value = -1
			if(value != ""):    # Set the parameter if it isn't skipped.
				exec("rhythm_players[{0}].{1}".format(layer - 1, parameters[i][2].format(value)))    # Set the parameter.
				self.go_down(4 - self.line)
				print("{0} set succesfully.".format(parameters[i][0]))
				self.go_up(30 - 6 * layer - self.line)
				print("  - {0} : {1}".format(parameters[i][0], value))
				self.go_down(24 - 6 * layer)

	def set_randomization_mode(self):    # Sets the type of randomization.
		mode = None
		self.line += 1
		while(not mode):    # Keep looping until a valid input is given.
			self.line -= 1
			mode = input("  - Randomization mode : ")    # Ask for usser input.
			self.line += 1
			if(mode == "exit"):    # Exit the loop.
				return
			elif(mode == "static" or mode == "evolve"):    # Check if the input is valid.
				randomization_mode = mode    # Set randomization.
				print("\nRandomization mode set to : {0}".format(mode))
				self.go_up(25)
				print("  Randomization mode : {0}".format(mode))
				self.line -= 22
			else:
				print("\n!! Invalid randomization mode. \n  - Valid modes: 'static', 'evolve'")
				mode = None
				self.go_up(4)

	def show_sample_page(self, page, num_of_pages):    # Show all available samples.
		self.go_down(27 - self.line)
		self.go_up(12, "delete")
		print("\033[K", end="{0}\nAvailable samples : page {1} of {2}".format(self.bar*53, page, num_of_pages))
		count = 0
		for i in range(8 * page - 8, 8 * page):
			try:
				print("\n\033[K", end="  {0}".format(self.sample_list[i]))
				count += 1
			except IndexError:
				break
		self.go_up(16 - self.line + count)

	def create_midi(self):    # Create a midi export.
		self.line += 3
		while(True):
			midi = input("  Would you like to save the generated rhythm as a midifile? (y/n)\n  - Note: Unsaved rhythms will be lost forever\n  >>> ")    # Ask if midi export should be made.
			if(midi.lower() == "y"):
				if(not os.path.exists("./resources/saves")):    # Check if saves directory exists.
					os.mkdir("./resources/saves")    # Create saves directory.
				file_exists = True
				while(file_exists):
					file_exists = False    # Assume filename doesn't exist yet.
					print("\n\033[K", end="")
					name = input("  - filename : ")    # Ask for user input.
					for root, dirs, files in os.walk("resources/saves"):
						if("{0}.mid".format(name) in files):    # Check if filename already exists.
							while(True):
								overwrite = input("\n!! This filename already exists. Overwrite '{0}.mid'? (y/n)\n  >>> ".format(name))    # Ask to overwrite the original file.
								if(overwrite.lower() == "y"):
									self.go_down(3)
									self.go_up(6, "delete")
									break
								elif(overwrite.lower() == "n"):
									file_exists = True
									self.go_down(3)
									self.go_up(8, "delete")
									break
								else:
									print("\n!! Unknown command : {0}".format(overwrite))
									self.go_up(2)
									self.go_up(3, "delete")						
				make_midifile(name)    # Create midi export.
				print("\n{0}.mid saved succesfully.".format(name))
				self.line += 4
				break
			elif(midi.lower() == "n"):
				break
			else:
				print("\n!! Unknown command : {0}".format(midi))
				self.go_up(2)
				self.go_up(3, "delete")

	def toggle_playback(self, mode):    # Toggle rhythm playback.
		if(mode == "on"):
			self.playback = True
			start_time = time.time() + 0.1    # Set a time to start playing.
			for player in rhythm_players:    # Start playback for all rhythm players.
				player.start_playback(start_time)

		elif(mode == "off"):
			self.playback = False
			for player in rhythm_players:    # Stop playback for all rhythm players.
				player.stop_playback()

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

#--miscellaneous--#
def valid_sample(sample):  # Checks if a sa.WaveObject kan be created from the input.
	try:
		sa.WaveObject.from_wave_file("resources/audioFiles/{0}".format(sample))
		return True
	except FileNotFoundError:
		return False

def check_files_and_directories():    # Checks if all the necessary files and directories are present.
	while(True):
		missing_files = []
		if(not os.path.exists("./resources")):
			missing_files.append("/resources")
		else:
			if(not os.path.exists("./resources/audioFiles")):
				missing_files.append("/resources/audioFiles")
			else:
				for root, dirs, files in os.walk("resources/audioFiles"):
					for file in necessary_wavefiles:
						if(file not in files):
							missing_files.append("resources/audioFiles/{0}".format(file))
			# if(not os.path.exists("./resources/helpfile.txt")):
			# 	missingFiles.append("/resources/helpfile.txt")
		if(len(missing_files) <= 0):
			break

		print("\nIrregular Beat Generator III   -   by: Teun Mansfelt")
		print("{0}\n!! OOPS! It seems some files are missing!\n\n  Missing files and directories:".format(gui.bar*53))
		for file in missing_files:
			print("  - {0}".format(file))

		while(True):
			download = input("\nWould you like to download the missing files? (y/n)\n>>> ")
			if(download.lower() == 'y'):
				webbrowser.open("https://github.com/teunmansfelt/CSD2/tree/master/blok2A/eindopdracht", new=0, autoraise=True)
				input("\n  - Press the return key to continue.")
				break
			elif(download.lower() == 'n'):
				entry = input("\n  - Press the return key to continue\n  - or type 'quit' to exit the program\n\n")
				if(entry == "quit"):
					print("\n  Thank you for using my software!\n  - Goodbye\n")
					time.sleep(1)
					clear()
					exit()
				else:
					gui.go_up(8, "delete")
			else:
				print("\n!! Unknown command : {0}".format(download))
				gui.go_up(2)
				gui.go_up(3, "delete")
		clear()

def make_midifile(name):    # Export the rhythms as a midifile.
	filename = 'resources/saves/{0}.mid'.format(name)
	midifile = MIDIFile(1)    # Midifile with 1 track.
	for event in tempo.events:    # Add tempo events.
		midifile.addTempo(0, event[0], event[1])
	for event in time_signature.events:    # Add timesignature events.
		midifile.addTimeSignature(0, event[0], event[1], event[2], 24)
	for i, player in enumerate(rhythm_players):   # Add the note events.
		for timestamp in player.rhythm.rhythm:
			midifile.addNote(0, 0, 36+3*i, timestamp, 0.25, 100)
	with open(filename, 'wb') as output_file:    # Open/create midifile with desired name.
		midifile.writeFile(output_file)    # Write to midifile.

#-------------------- OBJECTS --------------------#
notes = [4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25]    # List to store all possible note lengths.
rhythm_players = []    # List to store the rhythm players.
necessary_wavefiles = ["Default_kick.wav", "Default_snare.wav", "Default_hihat.wav"]

state = "main"
randomization_mode = "static"

clear = lambda: os.system('clear')    # Clears the console.

#--initialization--#
time_signature = time_signature_class(7, 8)
tempo = tempo_class(120)
gui = gui_class()

clear()
check_files_and_directories()

rhythm_players.append(rhythm_player_class("Default_kick.wav"))
rhythm_players.append(rhythm_player_class("Default_snare.wav"))
rhythm_players.append(rhythm_player_class("Default_hihat.wav", [0, time_signature.measure_length]))

#--------------------- MAIN ----------------------#
gui.init()

while(True):
	command = gui.get_input()
	if(command == "quit"):
		if(gui.playback):
			gui.toggle_playback("off")
			gui.create_midi()
		tempo.stop_slide()
		gui.go_down(14 - gui.line)
		print("\n  Thank you for using my software!\n  - Goodbye\n")
		time.sleep(1)
		clear()
		break
	
	elif(command.startswith("set tempo")):
		gui.set_tempo()
	
	elif(command.startswith("set timesignature")):
		gui.set_timesignature()
	
	elif(command.startswith("set samples")):
		gui.set_samples()

	elif(command.startswith("edit layer ")):
		layer = command.split(' ')[2]
		gui.edit_layer(layer)

	elif(command.startswith("set randomization mode")):
		gui.set_randomization_mode()
	
	elif(command.startswith("start playback")):
		gui.toggle_playback("on")
		time.sleep(0.1)
		clear()    # Clear any warnings possibly produced by the audio library.
		gui.init()    
	
	elif(command.startswith("stop playback")):
		gui.toggle_playback("off")
		gui.create_midi()
		tempo.reset_events()    # Reset the list of tempo events.
		time_signature.reset_events()    # Reset the list of timesignature events.
	
	else:
		gui.unknown_command(command)
