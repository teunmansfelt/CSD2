
#include <iostream>
#include <math.h>
#include "square_wavetable.hpp"

Square_Wavetable::Square_Wavetable(int samplerate) : Wavetable(samplerate * 2){
  this->wavetable = new double[this->wavetable_length];
  double* wavetable_p = this->wavetable;

  double phase = 0;
  double phase_increment = 1 / double(this->wavetable_length);

  for(int i = 0; i < this->wavetable_length; i++) {
    if(phase <= 0.5) {
      *wavetable_p = 1;
    } else {
      *wavetable_p = -1;
    }
    wavetable_p++;
    phase += phase_increment;
  }
}

Square_Wavetable::~Square_Wavetable() {}
