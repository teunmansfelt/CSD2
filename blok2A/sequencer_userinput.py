import simpleaudio as sa
import time
from random import randint

"""
An example project in which a rhythmical sequence (one measure, 1 sample) is played.
  - Sixteenth note is the smallest used note duration.
  - One meassure, time signature: 3 / 4
Instead of using steps to iterate through a sequence, we are checking the time.
We will trigger events based on a timestamp.
------ HANDS-ON TIPS ------
- Run the code, read the code and answer the following question:
  - This script transforms a list of 'sixteenth notes timestamps' into a list of
    regular timestamps.
    In the playback loop, the time difference (currentTime minus startTime)
    is compared to the upcomming timestamp.
    Why is this a more accurate method then the methods used in the examples
    "04_randomNoteDuration.py" and "05_oneSampleSequenceSteps.py"?
    Notate your answer below this line (Dutch is allowed)!

	By using the time.sleep() function, you are pausing the code on that thread.
	This will be accurate if playing the sample en pausing the code is the only thing happening.
	However, as soon as more code has to be run in between, more delay will be introduced.
	This means that in the long run, the sequencer will start to run out of sinc with the
	original tempo (and with other threads if those are also running)

- Alter the code:
  Currently one sample is played. Add another sample to the script.
  When a sample needs to be played, choose one of the two samples
  randomly.
  (See the hint about the random package in script "02_timedPlayback".)

- Alter the code:
  Currently the sequence is only played once.
  Alter the code to play it multiple times.
  hint: The timestamps list is emptied using the pop() function.
  (multiple possible solutions)
"""

# load 1 audioFile and store it into a list
# note: using a list taking the next step into account: using multiple samples


samples = ["Dog2.wav", "Laser1.wav", "Pop.wav", "aSound.wav"] # list of samples
i = randint(0, len(samples) - 1) # generates a random integer
file_path = "audioFiles/" + samples[i] # creates file-directory
sample = sa.WaveObject.from_wave_file(file_path) # sets sample

bpm = 120 # set bpm
quarterNoteDuration = 60 / bpm # calculate the duration of a quarter note
sixteenthNoteDuration = quarterNoteDuration / 4.0 # calculate the duration of a sixteenth note

timeSignature = 3/4 # set time signature
sixteenthNotePerBar = 16 * timeSignature # calculate the number of sixteenth notes in a bar.

timestamps = [] # create a list to hold the timestamps
timestamps16th = [0, 2, 4, 8, 11] # create a list with ‘note timestamps' in 16th at which we should play the sample

repeats = 3 # sets number of repeats
for r in range(0, repeats):
	for timestamp in timestamps16th: # transform the sixteenthTimestamps to a timestamps list with time values
		noteOffsetPerBar = r * sixteenthNotePerBar # calculates the offset for every bar
		timestamps.append((timestamp + noteOffsetPerBar) * sixteenthNoteDuration)
#print(timestamps)

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