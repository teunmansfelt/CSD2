
import random
from random import randint

def pickNote(notes, position, spread):
	probabilityDistribution = []
	n = spread + 1

	k = 1
	while k <= n:
		probabilityDistribution.append(round(k/(n*n), 4))
		k += 1
	k -= 2
	while k > 0:
		probabilityDistribution.append(round(k/(n*n), 4))
		k -= 1

	outOfBounds = 0
	if position - spread < 0:
		for i in range(0, spread - position):
			outOfBounds += probabilityDistribution.pop(0)

	if position + spread > len(notes) - 1:
		for i in range(0, spread):
			outOfBounds += probabilityDistribution.pop(-1)

	for i, probability in enumerate(probabilityDistribution):
		probabilityDistribution[i] = probability + outOfBounds/len(probabilityDistribution)
		probabilityDistribution[i] = round(probabilityDistribution[i], 4)

	noteProbabilities = [0]*len(notes)
	for i in range(0, len(probabilityDistribution)):
		if position - spread >= 0:
			noteProbabilities[i + position - spread] = probabilityDistribution[i]
		else:
			noteProbabilities[i] = probabilityDistribution[i]

	for i, chance in enumerate(noteProbabilities):
		try:
			noteProbabilities[i] = round(chance + noteProbabilities[i-1], 4)
		except IndexError:
			pass

	x = round(random.uniform(0, 0.9999), 4)
	for i, chance in enumerate(noteProbabilities):
		if x < chance:
			return notes[i]
			break

noteValues = [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]
gridMain = [0]
gridNoteValues = []
sumNoteValues = 0
measureLength = int(input(">> "))

gridMain.append(3)
gridLength = 3

while gridLength < measureLength:
	if measureLength - gridLength > 2:
		i = (randint(0, 1) + 1) * 2
	else:
		i = 2
	print(i)
	gridMain.append(i + gridMain[-1])
	gridLength += i

gridMainCopy = gridMain[1:len(gridMain)]
gridMain.pop(-1)
print(gridMain)
print(gridMainCopy)

noteDensity = len(noteValues) - int(input(">> "))
noteVariation = int(input(">> "))

while sumNoteValues < measureLength:
	nextPulse = gridMainCopy.pop(0)

	while True:
		noteLength = pickNote(noteValues, noteDensity, noteVariation)

		if sumNoteValues + noteLength > nextPulse:
			noteLength = nextPulse - sumNoteValues

		sumNoteValues += noteLength
		gridNoteValues.append(noteLength)

		if sumNoteValues == nextPulse:
			break

print(gridNoteValues)