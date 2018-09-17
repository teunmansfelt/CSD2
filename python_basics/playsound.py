import simpleaudio as sa

#--------------------------- FUNCTIONS -------------------------#

def loop(file_path, times) : # Plays an audiofile a specified number of times
	while(times > 0) :
		playFile(file_path)
		times -= 1

def playFile(file_path) : # Plays an audiofile
	wave_obj = sa.WaveObject.from_wave_file(file_path)
	play_obj = wave_obj.play()
	play_obj.wait_done()


#--------------------------- EXECUTION -------------------------#

print("Please specify how many times you want to play the audiofile ")
print("(must be a whole number from 1 to 10)")

valid = False

while not valid : # Keeps asking for an input if the given input is invalid
	insert = input(">> ")

	if(insert.isdigit()) : # Checks if the input is an integer
		insert = int(insert) # Converts a valid input-string to an int
		if(insert >= 1 and insert <= 10) : # Checks if the input lays from 1 to 10
			valid = True
			loop("GTKick.wav", insert)
		else :
			print("Please insert a whole number from 1 to 10") 
	else :
		print("Please insert a whole number from 1 to 10")