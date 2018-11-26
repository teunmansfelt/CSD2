
#include <iostream>
#include "instrument.h"

Instrument::Instrument(std::string name, std::string sound){
	std::cout << "\nInstrument::Instrument - Constructor - " << name << std::endl;
	this->name = name;
	this->sound = sound;
}

void Instrument::makeSound(){
	std::cout << "\nThe " << name << " goes " << sound << std::endl;
}

void Instrument::roll(int repetitions){
	std::string newSound;
	for(int i = 0; i < repetitions; i++){
		newSound.append(" ").append(sound);
	}
	sound = newSound;
	makeSound();
}