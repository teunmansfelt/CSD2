
def isFloat(x) : # Checks if an input is a float
	try :
		float(x)
		return True
	except ValueError :
		return False

rhythm = input()
rhythm = rhythm.split(',') 

BPM = float(input())
secPerBeat = 60/BPM

for n in range(len(rhythm)) :
	lastSymbol = len(rhythm[n]) - 1
	if(rhythm[n][lastSymbol] == '.') :
		note = float(rhythm[n]) * 1.5
	else :
		note = float(rhythm[n])

	amountOfBeats = 4 / note # Converts note-name to the amount of beats
	duration = amountOfBeats * secPerBeat # Calculates the time a note lasts in seconds

	print(amountOfBeats)
	print(duration)

# if(isFloat(insert)) :
# 	print('hoi')