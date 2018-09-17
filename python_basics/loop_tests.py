
# This file is a testfile, for learning and trying out various functionalities within python
# The following are included in this file so far:
#	lists
#	(for)loops

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

#--------------LISTS--------------#
	if(insert == 'lists') :

		#1initializing a list
		list_1 = []
		print('#1)', list_1)

		#2adding to a list
		list_1.append('hoi')
		print('#2)', list_1)

		#duplicating a list
		list_1 *= 5
		print('#3)', list_1)

		#changing the list at a certain index
		list_1[1] = 'doei'
		list_1[2] = 'hallo'
		list_1[3] = 'blabla'
		list_1[4] = 'koe'
		print('#4)', list_1)

		list_2 = ['schaap', 'varken']
		
		#joining lists
		list_1 += list_2
		print('#5)', list_1)

		#length of a list
		print('#6)', len(list_1))

		#section of a list
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