
def isFloat(x) : # Checks if an input is a float
	try :
		float(x)
		return True
	except ValueError :
		return False

insert = input()
insert = 'resources/' + insert

print(insert)

# if(isFloat(insert)) :
# 	print('hoi')