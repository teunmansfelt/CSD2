
#include "instrument.hpp"
#include "note_converter.hpp"

#include <iostream>
#include <array>

//--Constructor--//
Instrument::Instrument(std::string name, std::string type, std::string sound, std::array<int,2> pitchRange) {
  std::cout << "Instrument (BaseClass) - Constructor\n";
  this->name = name;
  this->type = type;
  this->sound = sound;
  this->lowest_note = pitchRange[0];
  this->highest_note = pitchRange[1];
}

//--Destructor--//
Instrument::~Instrument(){
  std::cout << "Instrument (BaseClass) - Destructor\n";
}


//--Methods--//
void Instrument::play(std::string pitch){

}


//--Getters--//
std::string Instrument::getName(){
  return name;
}

int Instrument::getLowestNote(){
  return lowest_note;
}

int Instrument::getHighestNote(){
  return lowest_note;
}
