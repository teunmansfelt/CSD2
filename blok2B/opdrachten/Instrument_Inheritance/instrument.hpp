
#ifndef INSTRUMENT_H
#define INSTRUMENT_H

#include <iostream>
#include <array>

class Instrument {
protected:
//--Constructor/Destructor--//
  Instrument(std::string name, std::string type, std::string sound, std::array<int,2> pitchRange);
  ~Instrument();

public:
//--Methods--//
  void play(std::string pitch);

//--Getters & Setters--//
  std::string getName();
  int getLowestNote();
  int getHighestNote();

private:
//--Fields--//
  std::string name;
  std::string type;
  std::string sound;
  int lowest_note;
  int highest_note;
};

#endif
