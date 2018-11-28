
#include "string_instrument.hpp"

#include <iostream>
#include <array>

//--Constructor--//
String_Instrument::String_Instrument(std::string name, std::string sound, std::array<int,2> pitchRange) : Instrument(name, "String Instrument", sound, pitchRange){
  std::cout << "String_Instrument - Constructor\n";
}

//--Destructor--//
String_Instrument::~String_Instrument(){
  std::cout << "String_Instrument - Destructor\n";
}
