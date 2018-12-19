
#ifndef SINE_H
#define SINE_H

#include "oscillator.hpp"

#include <iostream>
#include <array>
#define PI_2 6.28318530717959

class Sine : public Oscillator {
public:
  //-- Constructor Destructor  --//
  Sine(int samplerate, float frequency);
  Sine(int samplerate, float frequency, float phase, double amplitude);
  ~Sine();

  Sine() = delete;

private:
  //-- Wavetable --//
  void calculate_wavetable() override;
};

#endif
