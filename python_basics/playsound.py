import simpleaudio as sa

#--------------------------- FUNCTIONS -------------------------#

def loop(file_path, times) :
	while(times > 0) :
		playFile(file_path)
		times -= 1

def playFile(file_path) :
	wave_obj = sa.WaveObject.from_wave_file(file_path)
	play_obj = wave_obj.play()
	play_obj.wait_done()


#--------------------------- EXECUTION -------------------------#

print("Please specify how many times you want to play the audiofile ")
print("(must be a whole number from 1 to 10)")

valid = False

while not valid :
	insert = input(">> ")

	if(insert.isdigit()) :
		insert = int(insert)
		if(insert >= 1 and insert <= 10) :
			valid = True
			loop("geluid.wav", insert)
		else :
			print("Please insert a whole number from 1 to 10") 
	else :
		print("Please insert a whole number from 1 to 10")