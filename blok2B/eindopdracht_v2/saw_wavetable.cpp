
#include <iostream>
#include <math.h>
#include "saw_wavetable.hpp"

Saw_Wavetable::Saw_Wavetable(int samplerate) : Wavetable(samplerate * 2){
  this->wavetable = new double[this->wavetable_length];
  double* wavetable_p = this->wavetable;

  double phase = 0;
  double phase_increment = 1 / double(this->wavetable_length);

  for(int i = 0; i < this->wavetable_length; i++) {
    *wavetable_p = 2 * phase - 1;
    wavetable_p++;
    phase += phase_increment;
  }
}

Saw_Wavetable::~Saw_Wavetable() {}
