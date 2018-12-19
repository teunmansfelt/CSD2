
#include "sine.hpp"

#include <iostream>
#include <math.h>

//-- Constructor --//
Sine::Sine(int samplerate, float frequency) :
  Sine(samplerate, frequency, 0, 1) {}

Sine::Sine(int samplerate, float frequency, float phase, double amplitude) :
  Oscillator(samplerate, frequency, phase, amplitude) {
  calculate_wavetable();
}

//-- Destructor --//
Sine::~Sine() {std::cout << "~Sine" << std::endl;}

//-- Wavetable --//
void Sine::calculate_wavetable() {
  wavetable = new double[wavetable_length];
  double phase_ = 0;
  double phase_increment = 1 / double(wavetable_length);

  for(int i = 0; i < wavetable_length; i++) {
    wavetable[i] = sin(PI_2 * phase_);
    phase_ += phase_increment;
  }
}
