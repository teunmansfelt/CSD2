
#include <iostream>

class Instrument{
public:
	// Constructor
	Instrument(std::string name, std::string sound);
	// Methods
	void makeSound();
	void roll(int repetitions);
	
private:
	// Fields
	std::string name;
	std::string sound;
};