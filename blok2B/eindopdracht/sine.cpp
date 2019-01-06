
#include "sine.hpp"

#include <iostream>
#include <math.h>

//-- Constructor --//
Sine::Sine(int samplerate) :
  Sine(samplerate, 1, 12) {}

Sine::Sine(int samplerate, double amplitude, int polyphony) :
  Oscillator(samplerate, amplitude, polyphony, 1) {
  calculate_wavetable();
}

//-- Destructor --//
Sine::~Sine() {std::cout << "~Sine" << std::endl;}

//-- Wavetable --//
void Sine::calculate_wavetable() {
  wavetable = new double[wavetable_length];
  double* wavetable_pointer = wavetable;

  double phase_ = 0;
  double phase_increment = 1 / double(wavetable_length);

  for(int i = 0; i < wavetable_length; i++) {
    *wavetable_pointer = sin(PI_2 * phase_);
    wavetable_pointer++;
    phase_ += phase_increment;
  }
}
