
#include <iostream>
#include <math.h>
#include "sine_wavetable.hpp"

Sine_Wavetable::Sine_Wavetable(int samplerate) : Wavetable(samplerate * 2){
  this->wavetable = new double[this->wavetable_length];
  double* wavetable_p = this->wavetable;

  double phase = 0;
  double phase_increment = 1 / double(this->wavetable_length);

  for(int i = 0; i < this->wavetable_length; i++) {
    *wavetable_p = sin(PI_2 * phase);
    wavetable_p++;
    phase += phase_increment;
  }
}

Sine_Wavetable::~Sine_Wavetable() {}
