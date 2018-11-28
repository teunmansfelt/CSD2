
# This file is a testfile, for learning and trying out various functionalities within python
# The following are included in this file so far:
#	lists
#	(for)loops
#	strings

print('type help for all the insert options')
print('type quit to exit the program')

running = True
while running:
	insert = input('>> ')

	if(insert == 'quit') :
		running = False
		break

	if(insert == 'help') :
		print('lists')
		print('loops')
		print('strings')

#--------------LISTS--------------#
	if(insert == 'lists') :

		#1 initializing a list
		list_1 = []
		print('#1)', list_1)

		#2 adding to a list
		list_1.append('hoi')
		print('#2)', list_1)

		#3 duplicating a list
		list_1 *= 5
		print('#3)', list_1)

		#4 changing the list at a certain index
		list_1[1] = 'doei'
		list_1[2] = 'hallo'
		list_1[3] = 'blabla'
		list_1[4] = 'koe'
		print('#4)', list_1)

		list_2 = ['schaap', 'varken']
		
		#5 joining lists
		list_1 += list_2
		print('#5)', list_1)

		#6 length of a list
		print('#6)', len(list_1))

		#7 section of a list
		print('#7)', list_1[2:5])


#---------------LOOPS-------------#
	if(insert == 'loops') :
		
		#1 while loop
		print('#1)')
		x = 0
		while(x < 4) :
			print(x)
			x += 1
		print('')

		#2 for loop with range
		print('#2)')
		for x in range(0, 4) :
			print(x)
		print('')

		#3 breaking a loop
		print('#3)')
		for x in range(0, 4) :
			print(x)
			if(x == 1) :
				break
		print('')

		#4 nested loop
		print('#4')
		for x in range(0, 4) :
			for y in range(0, 3) :
				print('%d * %d = %d' % (x, y, x * y))
		print('')

		#5 loop through items in a lists
		print('#5')
		lst = ['a', 'b', 'c', 'd']
		for x in lst :
			print(x)
		print('')

#--------------STRINGS-------------#
	if(insert == 'strings') :

		#1 initializing string
		string_1 = "Dit is een zin"
		print('#1)', string_1)

		#2 position in a string
		print('#2)', string_1[3])

		#3 slice of a string
		print('#3)', string_1[2:8])

		#4 length of a string
		print('#4)', len(string_1))

		#5 replacing parts of a string
		print('#5)', string_1.replace("i", "o" ))

		#6 splitting a string by a devider
		devider = ' ' # <- spacebar
		print('#6.a)', string_1.split(devider))

		devider = 'i'
		print('#6.b)', string_1.split(devider))