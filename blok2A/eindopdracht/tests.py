import time

#--- MAIN ---#
while True:
	insert = input('>>> ')

	if insert == 'quit':
		break

	if insert == 'multiprocessing':
#------------ MULTIPROCESSING ------------#
		# Bij multiprocessing wordt er voor ieder nieuw proces een nieuwe instance van python opgestart.
		# Ieder proces wordt toegewezen aan een core in de CPU. Multiprocessing loopt dus daadwerkenlijk
		# parallel. 

		# De voordelen t.o.v. multithreading:
			# 1. Multiprocessing loopt parallel. Het is dus alsof er meerdere python programma's tegelijk
			# bezig zijn. Bij zwaardere scripts is dit dus ook sneller.

		# De nadelen t.o.v. multithreading: 
			# 1. Een proces opstarten kost meer tijd dan een thread starten.
			# 2. Ieder proces heeft zijn eigen memory (staat later in meer detail uitgelegd)

		import multiprocessing as mp

		arr = [2,3,4,5,6]
								
		def multiply(numbers, multiplier):
			for n in numbers:
				print('multiply  ' + str(n * multiplier.value))
				time.sleep(3)

		def devide(numbers, multiplier):
			for n in numbers:
				print('devide  ' + str(n / multiplier.value))
				time.sleep(3)

		def showValue(value):
			print(multiplier.value)
			print(type(multiplier.value))

		if __name__ == "__main__": 		# Het main proces, ook wel parent genoemd. Ieder nieuw
										# proces moet hierin worden geïnitialiseerd.
		
			multiplier = mp.Value('i', 3)

			p1 = mp.Process(target=multiply, args=(arr, multiplier))
			p2 = mp.Process(target=devide, args=(arr, multiplier))
			p1.start()
			p2.start()

			# p3 = mp.Process(target=showValue, args=(multiplier,))
			# p3.start()

			# multiplier = float(input())	# Deze input heeft geen effect op de functies, omdat 
											# ieder proces zijn eigen memory heeft. Het veranderen
											# van de variabele heeft dus alleen effect op de main 
											# en niet op de individuele processen.

			multiplier.value = int(input())

			p1.join()
			p2.join()
			# p3.join()

			print("done")

	if insert == 'multithreading':
#------------ MULTITHREADING ------------#
		# Bij multithreading worden er meerdere functies sequencieel afgewisseld op het moment dat een
		# functie vertraging heeft. (De CPU doet dan niks en kan dus andere functies uitvoeren)  

		# De voordelen t.o.v. multiprocessing:
			# 1. Multithreading loopt binnen één proces en iedere thread kan dus per direct communiceren
			# met iedere andere thread.
			# 2. Voor lichte scripts is het efficienter een nieuwe thread te starten dan een nieuw proces

		# De nadelen t.o.v. multiprocessing: 
			# 1. Threads lopen elkaar altijd sequencieel af wanneer een andere niks doet. Dit betekent ook
			# Dat bepaalde processen 'out-of-sync' kunnen gaan lopen.
			# 2. Multithreading heeft alleen zin als het programma ergens op moet wachten. Als het programma
			# nergens op hoeft te wachten, dan is multithreading niet sneller/efficienter.

		import threading as t

		arr = [2,3,4,5,6]
		multiplier = 3

		def multiply(numbers):
			global multiplier
			for n in numbers:
				print('multiply  ' + str(n * multiplier))
				time.sleep(3)

		def devide(numbers):
			global multiplier
			for n in numbers:
				print('devide  ' + str(n / multiplier))
				time.sleep(3)

		t1 = t.Thread(target=multiply, args=(arr,))
		t2 = t.Thread(target=devide, args=(arr,))
		t1.start()
		t2.start()

		multiplier = float(input())		# In tegenstelling tot multiprocessing kunnen threads wel
										# direct met globale variabele werken.

		t1.join()
		t2.join()