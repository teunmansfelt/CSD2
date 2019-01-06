
#ifndef SINE_H
#define SINE_H

#include <iostream>
#include "oscillator.hpp"
#include "sine_wavetable.hpp"

class Sine : public Oscillator{
public:
  Sine(int samplerate);
  Sine(int samplerate, int polyphony);
  ~Sine();

  Sine() = delete;
};

#endif
