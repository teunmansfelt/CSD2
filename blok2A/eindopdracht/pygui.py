
import atexit
from os import system

_init = False
_line_tracker = None

class line_tracker_class:
	"""
	Keeps track of which line the cursor is.
	The mode determines if the line numbers are printed (toggled on by including the edit_mode().)
	"""
	def __init__(self):
		self.line_index = 0
		self.mode = "display"

def init():
	"""
	Initialize the gui module.
	pygui.init(): return None

	Call the init function before using the module.
.
	It is safe to call this more than once.
	"""
	global _line_tracker, _init
	if not _init:
		_line_tracker = line_tracker_class()
		_init = True
		clear_screen()
		atexit.register(quit)

def quit():
	"""
	Uninitialize the gui module.
	pygui.quit(): return None

	Called automatically when the program exits if not called manually.

	It is safe to call this more than once.
	"""
	global _line_tracker, _init
	if _init:
		del _line_tracker
		_line_tracker = None
		_init = False
		clear_screen()

def _check_init(): # Check if the pygui module is initialized.
	global _init
	if not _init:
		raise RuntimeError("pygui not initialised.")

def clear_screen(): # clears the entire screen.
	system("clear")
	if(_line_tracker):
		if(_line_tracker.mode == "edit"):
			for i in range(0, 51):
				print(i)
			_line_tracker.line_index = 49
		else:
			_line_tracker.line_index = 0

def edit_mode():
	"""
	Set the module to edit mode (line numbers get printed).
	pygui.edit_mode(): return None

	To toggle off edit mode, remove the function from the script.
	"""
	_check_init()
	_line_tracker.mode = "edit"
	for i in range(0, 51):
			print(i)
	_line_tracker.line_index = 49

def _go_to_line(line_index): # Makes the cursor jump to the desired line.
	shift = line_index - _line_tracker.line_index # Number of lines to jump.
	if(shift >= 0):
		while(shift > 0):
			print("\033[B", end="") # Go down a line.
			shift -= 1
	else:
		while(shift <= 0):
			print("\033[F", end="") # Go up a line.
			shift += 1
	_line_tracker.line_index = line_index # Update the global line index.

def print_ln(message, line_index, line_indent=0, repeats=1): # Enhanced print function.
	"""
	pygui.print_ln(): return None
	
	message     : The message to be printed (can be anything).
	line_index  : On what line the message should be printed.
	Line_indent : The amount of spaces before the message.
	repeats     : How many times the message is repeated.
	"""
	_check_init()
	_go_to_line(line_index)
	message = "{0}".format(message) * repeats # Convert message input to a string and repeat it if necessary.
	indent = " "
	indent *= line_indent # Make the indentation string.
	if(_line_tracker.mode == "edit"):
		print("{0} \033[K".format(line_index + 1), end="") # Remove previous prints.
		print("\033[F", end="")
		if(line_index < 10):
			print("{0}  {1}{2}".format(line_index, indent, message))
		else:
			print("{0} {1}{2}".format(line_index, indent, message))
	else:
		print("\033[K", end="") # Remove previous prints.
		print("\033[F", end="")	
		print("{0}{1}".format(indent, message))
	
def clear_ln(start_index, end_index=None): # Clear a chunck of the console.
	"""
	pygui.clear_ln(): return None

	start_index : First line to be cleared.
	end_index   : Last line to be cleared.

	If the end_index is smaller than the start_index, nothing will happen.
	"""
	_check_init()
	if(end_index < start_index):
		return
	else:
		if(end_index == None):
			end_index = start_index
		_line_tracker.line_index -= 1
		for i in range(start_index, end_index + 1):
			print_ln(i, "")

def get_input(message, line_index, line_indent=0): # Take user input.
	"""
	pygui.get_input: return 'user input'

	message     : The input message to be printed (must be a string).
	line_index  : On what line the message should be printed.
	Line_indent : The amount of spaces before the message.
	"""
	_check_init()
	_go_to_line(line_index)
	_line_tracker.line_index -= 1
	indent = " "
	indent *= line_indent # Make the indentation string.
	if(_line_tracker.mode == "edit"):
		print("{0} \033[K".format(line_index + 1), end="") # Remove previous prints.
		print("\033[F", end="")
		if(line_index < 10):
			return input("{0}  {1}{2}".format(line_index, indent, message))
		else:
			return input("{0} {1}{2}".format(line_index, indent, message))		
	else:
		print("\033[K", end="") # Remove previous prints.
		print("\033[F", end="")	
		return input("{0}{1}".format(indent, message))
