
#ifndef SAW_H
#define SAW_H

#include <iostream>
#include <vector>
#include "oscillator.hpp"
#include "saw_wavetable.hpp"

class Saw : public Oscillator{
public:
  Saw(int samplerate);
  Saw(int samplerate, int polyphony);
  ~Saw();

  Saw() = delete;
};

#endif
