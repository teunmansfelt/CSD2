
#ifndef STRING_INSTRUMENT_H
#define STRING_INSTRUMENT_H

#include "instrument.hpp"

#include <iostream>
#include <array>

class String_Instrument : public Instrument {
public:
//--Constructor/Destructor--//
  String_Instrument(std::string name, std::string sound, std::array<int,2> pitchRange);
  ~String_Instrument();
};

#endif
